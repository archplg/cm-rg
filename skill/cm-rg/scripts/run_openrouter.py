#!/usr/bin/env python3
"""CM-RG four-phase pipeline over the OpenRouter API - any models, one script.

Runs the Cross-Model Repertory Grid protocol (free response - anonymization -
triadic construct elicitation - cross-rating) on ANY list of OpenRouter model
slugs, and writes a grid.json ready for analyze_grid.py.

Usage:
    # 0. Offline self-test (no network, no key, $0) - verifies the pipeline:
    python run_openrouter.py --selftest

    # 1. Set your key (never put it in a file):
    #    PowerShell:  $env:OPENROUTER_API_KEY = "sk-or-v1-..."
    #    bash:        export OPENROUTER_API_KEY="sk-or-v1-..."

    # 2. Plan the run and estimate cost (no calls are made):
    python run_openrouter.py --models "anthropic/claude-sonnet-4.6,openai/gpt-5.5,google/gemini-3.1-pro" \
        --brief ../assets/task_brief_ma.md --out run1 --dry-run

    # 3. Run for real (hard spend cap enforced):
    python run_openrouter.py --models "..." --brief ../assets/task_brief_ma.md --out run1 --max-usd 5

    # 4. Analyze:
    python analyze_grid.py run1/grid.json run1/analysis

Prompts are verbatim from the Archipelago Phase 2L pipeline - do not edit them
if you want results comparable to the published baselines.
"""
import argparse
import json
import os
import random
import re
import sys
import time
from pathlib import Path

API_BASE = "https://openrouter.ai/api/v1"
MIN_MODELS, MAX_MODELS = 3, 12
RETRIES = 3

# ---------------------------------------------------------------- prompts ---
PHASE1_SYSTEM = (
    "You are an analyst. Read the brief carefully. "
    "Provide your best-reasoned recommendation in 300-500 words. "
    "Be specific - advocate clearly for one approach. "
    "Brief follows.\n\n"
)

PHASE3_SYSTEM = (
    "You are participating in a Personal Constructs research study. You will see three "
    "anonymized advisory responses to the same brief. Your task: identify constructs - "
    "bipolar dimensions on which responses differ. Use the triadic method: for each "
    "construct, two responses share a quality that the third lacks.\n\n"
    "Output ONLY valid JSON in this format:\n"
    '[{"pole_a": "decisive", "pole_b": "deliberative", "context": "decision style"}, ...]\n\n'
    "Provide 8-12 constructs. Each pole should be a single adjective or short noun phrase. "
    "Do not include any text outside the JSON array."
)

PHASE4_SYSTEM = (
    "You are rating advisory responses on a personal constructs grid. "
    "You will see a list of CONSTRUCTS (bipolar dimensions) and a list of anonymized RESPONSES. "
    "Rate each response on each construct using a 1-7 scale where 1=strongly pole_a, 7=strongly pole_b, 4=neutral.\n\n"
    'Output ONLY valid JSON: {"ratings": [[1, 4, 7, ...], ...]} where outer array is per-response, '
    'inner array is per-construct in the listed order. No text outside the JSON.'
)

CONSTRUCTS_PER_BATCH = 50

try:  # anonymization patterns live in anonymize.py next to this file
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from anonymize import anonymize_text
except Exception:  # standalone fallback (same patterns, ported verbatim)
    _P = [
        (re.compile(r"(?i)\b(I\s+am\s+|I'm\s+)(claude|gpt|chatgpt|gemini|llama|mistral|deepseek|grok|qwen|kimi|glm|nemotron|command|granite)\b[^.]*\."), ""),
        (re.compile(r"(?i)\b(as\s+an\s+ai\s+(language\s+)?model|as\s+a\s+language\s+model)\b[^.]*\."), ""),
        (re.compile(r"(?i)\b(I\s+should\s+(note|mention|clarify)|it's\s+worth\s+noting)\b[^.]*\."), ""),
        (re.compile(r"(?i)\b(developed\s+by|trained\s+by|built\s+by)\s+(anthropic|openai|google|meta|mistral|deepseek|xai|alibaba|moonshot|zhipu|nvidia|cohere|ibm)\b[^.]*\."), ""),
        (re.compile(r"(?i)\b(Claude|GPT-?\d?\.?\d?|Gemini|LLaMA|Mistral|DeepSeek|Grok|Qwen|Kimi|GLM|Nemotron|Command|Granite)\b"), "[MODEL]"),
        (re.compile(r"(?i)\b(Anthropic|OpenAI|Google DeepMind|DeepMind|Meta AI|Mistral AI|xAI|Alibaba|Moonshot|Zhipu|NVIDIA|Cohere|IBM Research)\b"), "[LAB]"),
    ]

    def anonymize_text(text: str) -> str:
        out = text
        for pat, repl in _P:
            out = pat.sub(repl, out)
        return re.sub(r"\s+", " ", out).strip()


def dynamic_redact(text: str, models: list) -> str:
    """Extra anonymization for arbitrary model lists (addition to the verbatim
    patterns): strip the participating models' own slugs, org prefixes and full
    name parts, which the fixed pattern list cannot know about. Single generic
    words are deliberately NOT stripped (would corrupt normal prose); a model
    referring to itself by a bare generic token is an accepted residual risk."""
    out = text
    frags = set()
    for slug in models:
        frags.add(slug)
        if "/" in slug:
            org, name = slug.split("/", 1)
            if len(org) >= 4:
                frags.add(org)
            if len(name) >= 6:
                frags.add(name)
    for frag in sorted(frags, key=len, reverse=True):
        out = re.sub(re.escape(frag), "[MODEL]", out, flags=re.IGNORECASE)
    return out


# ------------------------------------------------------------- transport ---
class Spend:
    def __init__(self, max_usd):
        self.max_usd = max_usd
        self.usd = 0.0
        self.calls = 0
        self.tokens_in = 0
        self.tokens_out = 0
        self.pricing = {}  # slug -> (usd_per_prompt_token, usd_per_completion_token)

    def estimate(self, model, tin, tout):
        p = self.pricing.get(model)
        return (tin * p[0] + tout * p[1]) if p else 0.0

    def add(self, model, tin, tout):
        self.calls += 1
        self.tokens_in += tin
        self.tokens_out += tout
        self.usd += self.estimate(model, tin, tout)

    def check(self):
        if self.max_usd is not None and self.usd >= self.max_usd:
            raise SpendCapReached(f"estimated spend ${self.usd:.2f} reached cap ${self.max_usd:.2f}")


class SpendCapReached(Exception):
    pass


def real_chat(api_key, model, system, user, temperature, max_tokens):
    """One chat completion via OpenRouter. Returns (content, tokens_in, tokens_out)."""
    import requests
    last_err = None
    for attempt in range(RETRIES):
        try:
            r = requests.post(
                f"{API_BASE}/chat/completions",
                headers={"Authorization": f"Bearer {api_key}",
                         "HTTP-Referer": "https://github.com/archplg/cm-rg",
                         "X-Title": "CM-RG skill"},
                json={"model": model, "temperature": temperature, "max_tokens": max_tokens,
                      "messages": [{"role": "system", "content": system},
                                   {"role": "user", "content": user}]},
                timeout=180)
            if r.status_code in (429, 500, 502, 503):
                last_err = f"HTTP {r.status_code}"
                time.sleep(2 ** (attempt + 1))
                continue
            r.raise_for_status()
            data = r.json()
            content = (data.get("choices") or [{}])[0].get("message", {}).get("content") or ""
            usage = data.get("usage") or {}
            if not content.strip():
                last_err = "empty content"
                time.sleep(2 ** (attempt + 1))
                continue
            return content, int(usage.get("prompt_tokens", 0)), int(usage.get("completion_tokens", 0))
        except SpendCapReached:
            raise
        except Exception as e:  # network errors etc.
            last_err = str(e)
            time.sleep(2 ** (attempt + 1))
    raise RuntimeError(f"{model}: all {RETRIES} attempts failed ({last_err})")


def fetch_models(api_key):
    """slug -> (prompt_price, completion_price) in USD per token; {} if unreachable."""
    try:
        import requests
        r = requests.get(f"{API_BASE}/models",
                         headers={"Authorization": f"Bearer {api_key}"} if api_key else {},
                         timeout=30)
        r.raise_for_status()
        out = {}
        for m in r.json().get("data", []):
            pr = m.get("pricing") or {}
            try:
                out[m["id"]] = (float(pr.get("prompt", 0)), float(pr.get("completion", 0)))
            except (TypeError, ValueError):
                out[m["id"]] = (0.0, 0.0)
        return out
    except Exception as e:
        print(f"  [warn] could not fetch model catalog ({e}); "
              f"slug validation and cost estimates disabled")
        return {}


# --------------------------------------------------------------- parsing ---
def strip_wrappers(content):
    c = re.sub(r"<(thinking|reasoning|analysis|reflection|scratchpad)>[\s\S]*?</\1>", "",
               content, flags=re.IGNORECASE)
    c = re.sub(r"</?(thinking|reasoning|analysis|reflection|scratchpad)>", "", c, flags=re.IGNORECASE)
    c = re.sub(r"```(?:json|JSON)?\s*", "", c)
    return re.sub(r"\s*```", "", c).strip()


def balanced(text, open_ch, close_ch):
    """Yield balanced top-level spans of open_ch...close_ch."""
    depth, start = 0, None
    for i, ch in enumerate(text):
        if ch == open_ch:
            if depth == 0:
                start = i
            depth += 1
        elif ch == close_ch and depth > 0:
            depth -= 1
            if depth == 0:
                yield text[start:i + 1]


def parse_constructs(content):
    c = strip_wrappers(content)
    for span in balanced(c, "[", "]"):
        try:
            arr = json.loads(span)
        except json.JSONDecodeError:
            continue
        items = [x for x in arr if isinstance(x, dict) and x.get("pole_a") and x.get("pole_b")]
        if len(items) >= 4:
            return [{"pole_a": str(x["pole_a"]).strip(), "pole_b": str(x["pole_b"]).strip(),
                     "context": str(x.get("context", "")).strip()} for x in items[:12]]
    return None


def parse_ratings(content, n_elements, n_constructs):
    c = strip_wrappers(content)
    candidates = []
    for span in balanced(c, "{", "}"):
        try:
            obj = json.loads(span)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "ratings" in obj:
            candidates.append(obj["ratings"])
    for m in candidates:
        if (isinstance(m, list) and len(m) == n_elements and
                all(isinstance(row, list) and len(row) == n_constructs for row in m)):
            out = []
            for row in m:
                out.append([int(round(v)) if isinstance(v, (int, float)) and 1 <= round(v) <= 7
                            else None for v in row])
            return out
    return None


# ----------------------------------------------------------------- logic ---
def triads_for(n):
    """One distinct triad per rater (see references/protocol.md)."""
    if n == 3:
        return [(0, 1, 2)] * 3
    if n == 4:
        return [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]
    return [(i % n, (i + 1) % n, (i + 2) % n) for i in range(n)]


def run(models, brief_path, outdir, seed, max_usd, api_key, chat, dry_run):
    brief = Path(brief_path).read_text(encoding="utf-8")
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    spend = Spend(max_usd)
    spend.pricing = fetch_models(api_key) if not dry_run or True else {}

    if spend.pricing:
        unknown = [m for m in models if m not in spend.pricing]
        if unknown:
            print(f"  [warn] not in OpenRouter catalog right now: {', '.join(unknown)}")
            print("         check exact slugs at https://openrouter.ai/models")
            if not dry_run:
                sys.exit(1)

    # rough plan: tokens per call (prompt est by chars/4)
    brief_tok = len(brief) // 4
    plan = []
    plan += [("P1", m, brief_tok + 60, 800) for m in models]
    plan += [("P3", m, 3 * 450 + 150, 800) for m in models]
    est_constructs = 10 * len(models)
    n_batches = (est_constructs + CONSTRUCTS_PER_BATCH - 1) // CONSTRUCTS_PER_BATCH
    p4_out = 60 + len(models) * min(est_constructs, CONSTRUCTS_PER_BATCH) * 5
    plan += [("P4", m, len(models) * 450 + est_constructs * 15, p4_out)
             for m in models for _ in range(n_batches)]
    est_usd = sum(spend.estimate(m, tin, tout) for _, m, tin, tout in plan)
    print(f"\nPlan: {len(models)} models, {len(plan)} API calls"
          + (f", estimated cost ${est_usd:.2f}" if spend.pricing else ", cost unknown (no catalog)")
          + (f", cap ${max_usd:.2f}" if max_usd else ""))
    if dry_run:
        print("Dry run - no calls made. Remove --dry-run to execute.")
        return None

    log = {"models": models, "seed": seed, "calls": []}

    def call(phase, model, system, user, temperature, max_tokens):
        spend.check()
        content, tin, tout = chat(api_key, model, system, user, temperature, max_tokens)
        spend.add(model, tin, tout)
        log["calls"].append({"phase": phase, "model": model, "tokens_in": tin,
                             "tokens_out": tout, "est_usd": round(spend.estimate(model, tin, tout), 5)})
        return content

    # Phase 1
    print("\nPHASE 1 - free response")
    responses = []
    for m in models:
        print(f"  {m} ...", flush=True)
        responses.append({"model": m, "text": call("P1", m, PHASE1_SYSTEM, brief, 1.0, 800).strip()})
    (out / "phase1_responses.json").write_text(json.dumps(responses, indent=2, ensure_ascii=False), encoding="utf-8")

    # Phase 2
    print("PHASE 2 - anonymization")
    rng = random.Random(seed)
    order = list(range(len(models)))
    rng.shuffle(order)
    anonymized, mapping = [], {}
    for label_idx, src in enumerate(order, start=1):
        label = f"E{label_idx}"
        anonymized.append({"element": label,
                           "text": dynamic_redact(anonymize_text(responses[src]["text"]), models)})
        mapping[label] = responses[src]["model"]
    (out / "anonymized.json").write_text(json.dumps(anonymized, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "mapping.json").write_text(json.dumps(mapping, indent=2, ensure_ascii=False), encoding="utf-8")

    # Phase 3
    print("PHASE 3 - triadic elicitation")
    constructs = []
    for rater_i, m in enumerate(models):
        tri = triads_for(len(models))[rater_i]
        triad_text = "".join(f"\n\n[{anonymized[j]['element']}]\n{anonymized[j]['text']}" for j in tri)
        user = f"Three anonymized responses:{triad_text}\n\nIdentify 8-12 constructs."
        content = call("P3", m, PHASE3_SYSTEM, user, 1.0, 800)
        parsed = parse_constructs(content)
        if parsed is None:
            content = call("P3", m, PHASE3_SYSTEM,
                           user + "\n\nYour previous output was not valid JSON. Output ONLY the JSON array.",
                           1.0, 800)
            parsed = parse_constructs(content)
        if parsed is None:
            print(f"  [warn] {m}: constructs unparseable after retry - rater contributes none")
            parsed = []
        for c in parsed:
            constructs.append({"id": f"C{len(constructs)+1}", **c, "source_model": m})
        print(f"  {m}: {len(parsed)} constructs")
    if len(constructs) < 8:
        print("ERROR: fewer than 8 constructs in the union - grid not viable. See logs.")
        sys.exit(1)
    (out / "phase3_constructs.json").write_text(json.dumps(constructs, indent=2, ensure_ascii=False), encoding="utf-8")

    # Phase 4
    print("PHASE 4 - cross-rating")
    n_el, n_c = len(anonymized), len(constructs)
    resp_block = "".join(f"\n\n[{a['element']}]\n{a['text']}" for a in anonymized)
    ratings = []
    for m in models:
        matrix = [[None] * n_c for _ in range(n_el)]
        for b0 in range(0, n_c, CONSTRUCTS_PER_BATCH):
            batch = constructs[b0:b0 + CONSTRUCTS_PER_BATCH]
            lines = "\n".join(f"{i+1}. {c['pole_a']} vs {c['pole_b']}"
                              + (f" ({c['context']})" if c['context'] else "")
                              for i, c in enumerate(batch))
            user = (f"CONSTRUCTS:\n{lines}\n\nRESPONSES:{resp_block}\n\n"
                    f"Rate all {n_el} responses on all {len(batch)} constructs.")
            max_out = 100 + n_el * len(batch) * 5
            content = call("P4", m, PHASE4_SYSTEM, user, 0.0, max_out)
            parsed = parse_ratings(content, n_el, len(batch))
            if parsed is None:
                content = call("P4", m, PHASE4_SYSTEM,
                               user + f"\n\nYour previous output was invalid. Output ONLY "
                                      f'{{"ratings": [...]}} with exactly {n_el} rows of {len(batch)} integers.',
                               0.0, max_out)
                parsed = parse_ratings(content, n_el, len(batch))
            if parsed is None:
                print(f"  [warn] {m}: batch at {b0} unparseable - cells left null")
            else:
                for i in range(n_el):
                    matrix[i][b0:b0 + len(batch)] = parsed[i]
        ratings.append({"rater": m, "matrix": matrix})
        done = sum(v is not None for row in matrix for v in row)
        print(f"  {m}: {done}/{n_el * n_c} cells")
    (out / "phase4_ratings.json").write_text(json.dumps(ratings, indent=2, ensure_ascii=False), encoding="utf-8")

    # Grid
    grid = {
        "meta": {"task": Path(brief_path).stem, "condition": "N",
                 "date": time.strftime("%Y-%m-%d"), "runner": "openrouter",
                 "seed": seed, "protocol": "CM-RG Phase 2L prompts, verbatim",
                 "est_cost_usd": round(spend.usd, 4)},
        "elements": [{"id": a["element"], "model": mapping[a["element"]]} for a in anonymized],
        "constructs": constructs,
        "ratings": ratings,
    }
    (out / "grid.json").write_text(json.dumps(grid, indent=2, ensure_ascii=False), encoding="utf-8")
    log["totals"] = {"calls": spend.calls, "tokens_in": spend.tokens_in,
                     "tokens_out": spend.tokens_out, "est_usd": round(spend.usd, 4)}
    (out / "run_log.json").write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nDone: {out}/grid.json | {spend.calls} calls | est ${spend.usd:.2f}")
    print(f"Next: python {Path(__file__).parent / 'analyze_grid.py'} {out}/grid.json {out}/analysis")
    return grid


# --------------------------------------------------------------- selftest ---
def selftest():
    """Full offline run with a fake transport - verifies parsing, phases, grid."""
    import tempfile
    fake_models = ["fake/alpha", "fake/beta", "fake/gamma"]

    def fake_chat(api_key, model, system, user, temperature, max_tokens):
        if system == PHASE1_SYSTEM:
            return (f"I recommend Option B. As {model} I think risk-adjusted value wins. "
                    f"The regulatory path matters most and a partitioned purchase caps the tail risk. "
                    * 12, 500, 400)
        if system == PHASE3_SYSTEM:
            arr = [{"pole_a": f"a{i}-{model[-5:]}", "pole_b": f"b{i}", "context": "test"} for i in range(9)]
            return "```json\n" + json.dumps(arr) + "\n```", 800, 300
        m = re.search(r"all (\d+) responses on all (\d+) constructs", user)
        n_el, n_c = int(m.group(1)), int(m.group(2))
        rng = random.Random(hash(model) % 1000)
        mat = [[rng.randint(1, 7) for _ in range(n_c)] for _ in range(n_el)]
        return "<thinking>hm</thinking>" + json.dumps({"ratings": mat}), 1500, 400

    with tempfile.TemporaryDirectory() as td:
        brief = Path(td) / "brief.md"
        brief.write_text("# Test task\nPick option A or B and justify.", encoding="utf-8")
        grid = run(fake_models, brief, Path(td) / "out", 42, 5.0, "sk-test", fake_chat, dry_run=False)
        assert grid and len(grid["elements"]) == 3
        assert len(grid["constructs"]) == 27
        for r in grid["ratings"]:
            assert len(r["matrix"]) == 3 and all(len(row) == 27 for row in r["matrix"])
            assert all(v is None or 1 <= v <= 7 for row in r["matrix"] for v in row)
        # anonymization must have stripped model self-identification (slugs)
        joined = " ".join(e["text"] for e in json.loads((Path(td) / "out" / "anonymized.json").read_text()))
        for slug in fake_models:
            assert slug.lower() not in joined.lower(), f"slug leak: {slug}"
    print("\nSELFTEST PASSED - pipeline, parsers, anonymization and grid schema all OK.")


def main():
    ap = argparse.ArgumentParser(description="CM-RG over OpenRouter")
    ap.add_argument("--models", help="comma-separated OpenRouter slugs (3-12)")
    ap.add_argument("--brief", help="path to the task brief .md")
    ap.add_argument("--out", help="output directory")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--max-usd", type=float, default=5.0,
                    help="hard cap on estimated spend (default 5.0)")
    ap.add_argument("--dry-run", action="store_true", help="plan + cost estimate, no API calls")
    ap.add_argument("--selftest", action="store_true", help="offline end-to-end test, no key needed")
    args = ap.parse_args()

    if args.selftest:
        # fetch_models will fail offline and degrade gracefully - that is expected
        selftest()
        return 0

    if not (args.models and args.brief and args.out):
        ap.error("--models, --brief and --out are required (or use --selftest / --dry-run)")
    models = [m.strip() for m in args.models.split(",") if m.strip()]
    if not (MIN_MODELS <= len(models) <= MAX_MODELS):
        ap.error(f"need {MIN_MODELS}-{MAX_MODELS} models, got {len(models)}")
    if len(set(models)) != len(models):
        ap.error("duplicate model slugs in --models")

    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key and not args.dry_run:
        print("ERROR: OPENROUTER_API_KEY is not set.\n"
              '  PowerShell:  $env:OPENROUTER_API_KEY = "sk-or-v1-..."\n'
              '  bash:        export OPENROUTER_API_KEY="sk-or-v1-..."')
        return 1
    if not Path(args.brief).exists():
        print(f"ERROR: brief not found: {args.brief}")
        return 1

    try:
        run(models, args.brief, args.out, args.seed, args.max_usd, api_key, real_chat, args.dry_run)
    except SpendCapReached as e:
        print(f"\nSTOPPED: {e}. Partial results are in {args.out}/ - raise --max-usd to continue.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
