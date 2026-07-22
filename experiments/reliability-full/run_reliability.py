#!/usr/bin/env python3
"""Collect singles for the full reliability experiment: every model answers
every item once, batched, resumable, spend-capped.

Usage:
    python run_reliability.py --selftest
    python run_reliability.py --catalog models_catalog.json --items items/items.json \
        --out run/ --dry-run
    python run_reliability.py --catalog models_catalog.json --items items/items.json \
        --out run/ --max-usd 60

Answers land in run/singles.json as {model_short: {item_id: answer}}. Re-running
skips batches already present (resume after network failures is free).
"""
import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

API_BASE = "https://openrouter.ai/api/v1"
BATCH = 10
RETRIES = 3

SOLVE_PROMPT = (
    "Solve the following {n} independent problems carefully. Think each one through "
    "step by step; keep visible working brief. Do not use any tools - work everything "
    "out by hand.\n\n{questions}\n\nAfter all working, end your reply with EXACTLY {n} "
    "lines, one per problem, in this format and nothing after them:\n{final_lines}\n"
    "Answer format rules: every answer is a plain integer (no commas, no spaces)."
)


def real_chat(api_key, model, user, max_tokens):
    import requests
    last = None
    for attempt in range(RETRIES):
        try:
            resp = requests.post(
                f"{API_BASE}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}",
                         "HTTP-Referer": "https://github.com/archplg/cm-rg",
                         "X-Title": "CM-RG reliability"},
                json={"model": model, "temperature": 0.0, "max_tokens": max_tokens,
                      "messages": [{"role": "user", "content": user}]},
                timeout=300)
            if resp.status_code in (429, 500, 502, 503):
                last = f"HTTP {resp.status_code}"
                time.sleep(3 ** (attempt + 1))
                continue
            resp.raise_for_status()
            data = resp.json()
            msg = ((data.get("choices") or [{}])[0].get("message") or {})
            content = msg.get("content") or ""
            if not content.strip():
                # reasoning models (deepseek-r1, kimi-thinking, ...) sometimes
                # leave `content` empty and put the answer (incl. FINAL lines)
                # in the `reasoning` field - salvage it before giving up
                content = msg.get("reasoning") or ""
            usage = data.get("usage") or {}
            if not content.strip():
                last = "empty content"
                time.sleep(3 ** (attempt + 1))
                continue
            return content, int(usage.get("prompt_tokens", 0)), int(usage.get("completion_tokens", 0))
        except Exception as e:
            last = str(e)
            time.sleep(3 ** (attempt + 1))
    raise RuntimeError(f"{model}: {RETRIES} attempts failed ({last})")


def fetch_pricing(api_key):
    try:
        import requests
        resp = requests.get(f"{API_BASE}/models",
                            headers={"Authorization": f"Bearer {api_key}"} if api_key else {},
                            timeout=30)
        resp.raise_for_status()
        out = {}
        for m in resp.json().get("data", []):
            pr = m.get("pricing") or {}
            try:
                out[m["id"]] = (float(pr.get("prompt", 0)), float(pr.get("completion", 0)))
            except (TypeError, ValueError):
                pass
        return out
    except Exception as e:
        print(f"  [warn] catalog unavailable ({e}) - no slug validation / cost estimates")
        return {}


def parse_finals(content, n):
    got = {}
    for m in re.finditer(r"FINAL\s+(\d+)\s*:\s*([^\n]+)", content):
        i = int(m.group(1))
        if 1 <= i <= n:
            got[i] = m.group(2).strip().rstrip(".").replace(",", "").replace(" ", "")
    return got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalog")
    ap.add_argument("--items")
    ap.add_argument("--out")
    ap.add_argument("--max-usd", type=float, default=60.0)
    ap.add_argument("--models", help="optional comma-separated subset of short names")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if not (args.catalog and args.items and args.out):
        ap.error("--catalog, --items and --out are required (or --selftest)")

    catalog = json.loads(Path(args.catalog).read_text())
    if args.models:
        wanted = set(args.models.split(","))
        catalog = [c for c in catalog if c["short"] in wanted]
    items = json.loads(Path(args.items).read_text())
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    singles_path = out / "singles.json"
    singles = json.loads(singles_path.read_text()) if singles_path.exists() else {}

    batches = [items[i:i + BATCH] for i in range(0, len(items), BATCH)]
    todo = [(c, bi, b) for c in catalog for bi, b in enumerate(batches)
            if any(it["id"] not in singles.get(c["short"], {}) for it in b)]

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    pricing = fetch_pricing(api_key)
    est_in = 250 + BATCH * 60
    est_out = 250 + BATCH * 120
    est = sum(est_in * pricing.get(c["slug"], (0, 0))[0] +
              est_out * pricing.get(c["slug"], (0, 0))[1] for c, _, _ in todo)
    print(f"Models: {len(catalog)} | items: {len(items)} | calls to make: {len(todo)} "
          f"(resume skips {len(catalog) * len(batches) - len(todo)})")
    print(f"Estimated cost: ${est:.2f}" if pricing else "Estimated cost: unknown (no catalog)",
          f"| cap ${args.max_usd:.2f}")
    if pricing:
        missing = [c["slug"] for c in catalog if c["slug"] not in pricing]
        if missing:
            print("  [warn] not in live catalog (will fail):", ", ".join(missing))
    if args.dry_run:
        print("Dry run - nothing sent.")
        return 0
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set.")
        return 1

    spent = 0.0
    for k, (c, bi, batch) in enumerate(todo, 1):
        if spent >= args.max_usd:
            print(f"STOPPED at cap ${spent:.2f} - re-run the same command to resume the rest.")
            break
        qs = "\n\n".join(f"{i+1}. {it['question']}" for i, it in enumerate(batch))
        finals = "\n".join(f"FINAL {i+1}: <answer>" for i in range(len(batch)))
        prompt = SOLVE_PROMPT.format(n=len(batch), questions=qs, final_lines=finals)
        # reasoning models spend most of their token budget on the hidden
        # chain-of-thought; give them far more room or they never reach the
        # FINAL lines (verified: gpt-5-mini / gpt-5.5 raw output is all reasoning)
        is_reasoning = any(t in c["slug"].lower() for t in (
            "r1", "-thinking", "thinking", "reasoning", "qwq", "o1", "o3", "o4",
            "gpt-5", "grok-4", "qwen3", "magistral", "deepseek-r"))
        max_out = (4000 + len(batch) * 2000) if is_reasoning else (400 + len(batch) * 350)
        try:
            content, tin, tout = real_chat(api_key, c["slug"], prompt, max_out)
            got = parse_finals(content, len(batch))
            if len(got) < len(batch):
                content2, t2, o2 = real_chat(
                    api_key, c["slug"],
                    prompt + "\n\nYour previous reply was missing FINAL lines. Reply again "
                             "with ALL FINAL lines.", max_out)
                tin += t2
                tout += o2
                got = {**parse_finals(content2, len(batch)), **got} if len(
                    parse_finals(content2, len(batch))) > len(got) else got
            p = pricing.get(c["slug"], (0, 0))
            spent += tin * p[0] + tout * p[1]
            singles.setdefault(c["short"], {})
            for i, it in enumerate(batch):
                singles[c["short"]][it["id"]] = got.get(i + 1)  # None = unanswered
            (out / "raw").mkdir(exist_ok=True)
            (out / "raw" / f"{c['short']}_b{bi}.txt").write_text(content, encoding="utf-8")
            singles_path.write_text(json.dumps(singles, indent=2), encoding="utf-8")
            ok = sum(v is not None for v in (singles[c["short"]][it["id"]] for it in batch))
            print(f"[{k}/{len(todo)}] {c['short']} batch {bi}: {ok}/{len(batch)} parsed | "
                  f"est spent ${spent:.2f}")
        except RuntimeError as e:
            print(f"[{k}/{len(todo)}] {c['short']} batch {bi}: FAILED ({e}) - "
                  f"left for resume")
    print(f"\nDone. singles.json has {len(singles)} models. Est spent ${spent:.2f}.")
    print("Next: python analyze_reliability.py --run", out)
    return 0


def selftest():
    import random as _r
    print("Selftest: generating tier-1 items and simulating a 5-model run offline...")
    import subprocess
    subprocess.run([sys.executable, "items_bank.py", "--seed", "1", "--tier-mix", "1:10",
                    "--out", "_selftest_items"], check=True)
    items = json.loads(Path("_selftest_items/items.json").read_text())
    answers = json.loads(Path("_selftest_items/answers.json").read_text())
    rng = _r.Random(0)
    singles = {}
    for m in ["M1", "M2", "M3", "M4", "M5"]:
        acc = {}
        for it in items:
            acc[it["id"]] = answers[it["id"]] if rng.random() < 0.7 else str(rng.randint(1, 999))
        singles[m] = acc
    Path("_selftest_run").mkdir(exist_ok=True)
    Path("_selftest_run/singles.json").write_text(json.dumps(singles, indent=2))
    # parse_finals sanity
    demo = "working...\nFINAL 1: 42\nFINAL 2: 7/8\nFINAL 3: 1,234"
    parsed = parse_finals(demo, 3)
    assert parsed == {1: "42", 2: "7/8", 3: "1234"}, parsed
    print("SELFTEST PASSED - items generated, singles simulated, parser OK.")
    print("Now run: python analyze_reliability.py --run _selftest_run "
          "--items _selftest_items --panels panels.json --selftest-panels")
    return 0


if __name__ == "__main__":
    sys.exit(main())
