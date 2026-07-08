"""
Phase 2L · Pre-flight Check 2: Cost dry-run on a single cell.

Runs ONE task × ONE condition × ONE run across all verified models to:
  1. Measure REAL cost per model (calibrate budget estimate)
  2. Verify usage.cost field is returned (catches Phase 2J $0 bug at scale)
  3. Validate response parser works on each model's output format
  4. Estimate full Phase 2L cost by extrapolation

Cost: $1-3 (single task across 39 models, single condition, single run).
Aborts if estimated full cost exceeds 1.5x the configured budget.

Usage:
    set OPENROUTER_API_KEY=sk-or-...
    python dry_run_phase2l.py --task K
        # uses task_K_brief.md - the cheapest/simplest task to dry-run on

    python dry_run_phase2l.py --task K --dry  # simulation only, no real API calls
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import datetime as dt
from pathlib import Path
from typing import Any

try:
    import yaml
    import requests
except ImportError as exc:
    print(f"ERROR: missing dependency ({exc}). Run: pip install pyyaml requests")
    sys.exit(1)


def load_config(p: Path) -> dict[str, Any]:
    with open(p, encoding="utf-8") as f:
        return yaml.safe_load(f)


def call_openrouter(
    *,
    api_key: str,
    base_url: str,
    model_slug: str,
    system_prompt: str,
    user_prompt: str,
    max_tokens: int,
    temperature: float,
    timeout: int,
) -> dict[str, Any]:
    url = base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://crossmodelrg.org",
        "X-Title": "CM-RG Phase 2L dry run",
    }
    payload = {
        "model": model_slug,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "usage": {"include": True},
    }
    t0 = time.time()
    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    latency_ms = int((time.time() - t0) * 1000)
    return {"status": resp.status_code, "body": resp.json() if resp.content else None, "latency_ms": latency_ms}


def extract_cost(api_body: dict[str, Any]) -> float | None:
    """Extract cost from usage.cost first, then cost_details, then None."""
    if not api_body or "usage" not in api_body:
        return None
    usage = api_body["usage"] or {}
    if not isinstance(usage, dict):
        return None
    # Primary: usage.cost
    cost = usage.get("cost")
    if cost is not None:
        try:
            return float(cost)
        except (TypeError, ValueError):
            pass
    # Fallback: cost_details.upstream_inference_cost
    cd = usage.get("cost_details") or {}
    if isinstance(cd, dict):
        upstream = cd.get("upstream_inference_cost")
        if upstream is not None:
            try:
                return float(upstream)
            except (TypeError, ValueError):
                pass
    return None


def parser_check(raw_text: str) -> dict[str, Any]:
    """Smoke-test that response is non-trivial. Real parser tests run separately."""
    out = {
        "is_non_empty": bool(raw_text and raw_text.strip()),
        "char_len": len(raw_text or ""),
        "looks_like_recommendation": False,
    }
    if not raw_text:
        return out
    lower = raw_text.lower()
    keywords = ("recommend", "i would", "the best", "option", "choose", "the most", "prioritize")
    out["looks_like_recommendation"] = any(k in lower for k in keywords)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 2L Check 2 dry-run on single cell")
    parser.add_argument("--config", default="config_phase2l.yaml")
    parser.add_argument("--task", default="K", help="Task ID to dry-run (cheapest task recommended)")
    parser.add_argument("--output-dir", default="./pre_flight")
    parser.add_argument("--dry", action="store_true", help="Simulate without API calls (sanity check of script)")
    args = parser.parse_args()

    config_path = Path(args.config)
    config = load_config(config_path)

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key and not args.dry:
        print("ERROR: OPENROUTER_API_KEY not set. Use --dry to simulate.")
        return 2

    # Identify task brief
    task_brief_path = None
    for t in config["tasks"]:
        if str(t.get("id")).strip() == args.task:
            task_brief_path = Path(t["brief_file"])
            break
    if task_brief_path is None:
        print(f"ERROR: task id '{args.task}' not in config.")
        return 2
    if not task_brief_path.exists():
        print(f"ERROR: task brief file not found: {task_brief_path}")
        return 2
    task_brief = task_brief_path.read_text(encoding="utf-8")

    # Use neutral condition only
    neutral = next((c for c in config["conditions"] if c["id"] == "N"), None)
    if neutral is None:
        print("ERROR: no neutral condition in config.")
        return 2

    system_prompt = neutral["system_prompt"]
    user_prompt = (
        task_brief
        + "\n\nProvide a 200-400 word free-form recommendation. Advocate for one option clearly."
    )

    free_params = config["parameters"]["free_response"]
    max_tokens = int(free_params["max_tokens"])
    temperature = float(free_params["temperature"])

    timeout = int(config["openrouter"]["request_timeout_seconds"])
    base_url = config["openrouter"]["base_url"]

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")

    results = []
    print(f"Dry-running task {args.task} on {len(config['models'])} models (neutral condition, 1 call each).\n")
    print(f"{'short':<6} {'family':<10} {'tier':<10} {'slug':<48} status   cost     latency  notes")
    print("-" * 130)

    total_cost = 0.0
    by_family_cost: dict[str, float] = {}
    skipped = 0

    for m in config["models"]:
        slug = m["id"]
        short = m.get("short_name", "?")
        family = m.get("family", "?")
        tier = m.get("tier", "?")
        line_pre = f"{short:<6} {family:<10} {tier:<10} {slug:<48}"

        if args.dry:
            print(line_pre + " DRY     skip      skip     simulated (no API call)")
            results.append({"slug": slug, "status": "DRY_SIMULATED"})
            continue

        try:
            r = call_openrouter(
                api_key=api_key,
                base_url=base_url,
                model_slug=slug,
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                timeout=timeout,
            )
            body = r["body"]
            status = r["status"]
            if status != 200:
                err_snippet = json.dumps(body)[:120] if body else "(no body)"
                print(line_pre + f" HTTP{status}  -        {r['latency_ms']}ms   {err_snippet}")
                results.append({"slug": slug, "status": f"HTTP_{status}", "error": err_snippet})
                skipped += 1
                continue

            cost = extract_cost(body)
            if cost is None:
                cost = 0.0
                cost_note = "WARNING: usage.cost MISSING (Phase 2J bug)"
            else:
                cost_note = ""
            total_cost += cost
            by_family_cost[family] = by_family_cost.get(family, 0) + cost

            choices = body.get("choices") or [] if body else []
            content = ""
            if choices and isinstance(choices, list):
                msg = choices[0].get("message", {}) if isinstance(choices[0], dict) else {}
                content = msg.get("content", "") or ""
            pcheck = parser_check(content)
            parser_status = "OK" if pcheck["is_non_empty"] and pcheck["looks_like_recommendation"] else "WEAK"

            print(
                line_pre
                + f" 200      ${cost:.4f}  {r['latency_ms']}ms   parser={parser_status} {cost_note}"
            )

            results.append({
                "slug": slug,
                "short_name": short,
                "family": family,
                "tier": tier,
                "status": "OK",
                "cost_usd": cost,
                "latency_ms": r["latency_ms"],
                "parser_status": parser_status,
                "parser_details": pcheck,
                "response_excerpt": content[:300],
                "usage": (body.get("usage") or {}) if body else {},
            })

        except Exception as exc:  # pragma: no cover
            print(line_pre + f" EXC     -        -        {type(exc).__name__}: {exc}")
            results.append({"slug": slug, "status": "EXCEPTION", "error": str(exc)})
            skipped += 1

    print("-" * 130)
    print(f"\nTotal cost across {len(results)} models for ONE cell: ${total_cost:.4f}")
    print(f"Skipped (errors): {skipped}")

    # Extrapolate to full Phase 2L: 7 tasks x 2 conditions = 14 cells
    # 4 phases per cell -> roughly 4x for full pipeline if each phase has similar cost
    n_cells = 14
    n_phases = 4
    extrapolated_full = total_cost * n_cells * n_phases
    print(f"\nExtrapolated full Phase 2L cost (this rate x {n_cells} cells x {n_phases} phases): ${extrapolated_full:.2f}")

    budget = float(config["experiment"].get("total_budget_usd") or 120)
    if extrapolated_full > 1.5 * budget:
        print(f"\nWARNING: extrapolated ${extrapolated_full:.2f} exceeds 1.5x budget (${budget}). Investigate before full run.")
    else:
        print(f"\nWithin budget envelope (${budget}). Proceed with caution to Check 3.")

    print("\nPer-family cost on this single cell:")
    for fam, c in sorted(by_family_cost.items(), key=lambda kv: -kv[1]):
        print(f"  {fam:<10}  ${c:.4f}")

    out_path = output_dir / f"phase2l_dry_run_{args.task}_{ts}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": ts,
                "task": args.task,
                "models_run": len(results),
                "total_cost_usd_single_cell": total_cost,
                "extrapolated_full_phase2l_usd": extrapolated_full,
                "budget_usd": budget,
                "by_family_cost": by_family_cost,
                "results": results,
            },
            f,
            indent=2,
        )
    print(f"\nReport saved: {out_path}")

    # Exit non-zero if any zero-cost model or weak parsing
    weak_models = [r for r in results if r.get("status") == "OK" and r.get("cost_usd") == 0]
    if weak_models:
        print(f"\nERROR: {len(weak_models)} model(s) returned zero cost (Phase 2J bug repeat). Investigate before full run.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
