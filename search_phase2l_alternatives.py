"""
Phase 2L · Catalog search helper.

Looks up ALL models in OpenRouter catalog matching given provider prefixes
and sorts them by completion pricing (proxy for tier). Helps find tier
alternatives for providers where Check 1 reported MISSING slots.

Cost: $0. Single GET to OpenRouter /models.

Usage:
    python search_phase2l_alternatives.py
        # uses default list of problem providers from Check 1
    python search_phase2l_alternatives.py --providers mistralai x-ai qwen deepseek
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)


OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"

DEFAULT_PROBLEM_PROVIDERS = [
    "mistralai",      # only flagship found
    "x-ai",           # only flagship found
    "qwen",           # mid=flagship duplicate
    "deepseek",       # no mid
    "z-ai",           # only flagship
    "nvidia",         # only cheap
    "google",         # cross-gen via fallback
    "moonshotai",     # cheap=mid
    "cohere",         # mostly fallback
    "ibm-granite",    # all missing - confirm absent
]


def fetch_catalog(api_key: str | None) -> list[dict[str, Any]]:
    headers = {"Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    resp = requests.get(OPENROUTER_MODELS_URL, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.json().get("data", [])


def get_completion_price_per_mtok(model: dict[str, Any]) -> float:
    p = (model.get("pricing") or {}).get("completion")
    try:
        return float(p) * 1_000_000 if p is not None else float("inf")
    except (TypeError, ValueError):
        return float("inf")


def get_prompt_price_per_mtok(model: dict[str, Any]) -> float:
    p = (model.get("pricing") or {}).get("prompt")
    try:
        return float(p) * 1_000_000 if p is not None else float("inf")
    except (TypeError, ValueError):
        return float("inf")


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 2L catalog search")
    parser.add_argument("--providers", nargs="*", default=DEFAULT_PROBLEM_PROVIDERS,
                        help="Provider prefixes to enumerate (default: problem providers from Check 1)")
    parser.add_argument("--output-dir", default="./pre_flight")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("WARNING: OPENROUTER_API_KEY not set. /models endpoint works without auth.\n")

    catalog = fetch_catalog(api_key)
    print(f"Catalog total: {len(catalog)} models.\n")

    by_provider: dict[str, list[dict[str, Any]]] = {p: [] for p in args.providers}
    for m in catalog:
        slug = m.get("id", "")
        for p in args.providers:
            if slug.lower().startswith(p.lower() + "/"):
                by_provider[p].append(m)
                break

    output: dict[str, Any] = {}

    for prov, models in by_provider.items():
        models_sorted = sorted(models, key=get_completion_price_per_mtok)
        print(f"\n{'='*100}")
        print(f"  PROVIDER: {prov}   ({len(models_sorted)} models found)")
        print(f"{'='*100}")
        if not models_sorted:
            print("  (no models found - this provider is absent from OpenRouter catalog)")
            output[prov] = []
            continue
        print(f"{'slug':<55} {'$prompt':>10} {'$compl':>10}  ctx     name")
        rows = []
        for m in models_sorted:
            pp = get_prompt_price_per_mtok(m)
            cp = get_completion_price_per_mtok(m)
            pp_str = f"${pp:.2f}" if pp < float("inf") else "n/a"
            cp_str = f"${cp:.2f}" if cp < float("inf") else "n/a"
            ctx = m.get("context_length") or "-"
            name = m.get("name") or ""
            print(f"  {m['id']:<53} {pp_str:>10} {cp_str:>10}  {str(ctx)[:7]:<8}{name[:55]}")
            rows.append({
                "slug": m["id"],
                "prompt_per_mtok_usd": pp if pp < float("inf") else None,
                "completion_per_mtok_usd": cp if cp < float("inf") else None,
                "context_length": m.get("context_length"),
                "name": m.get("name"),
            })
        output[prov] = rows

    # Suggest tier picks based on completion price tertiles
    print(f"\n\n{'='*100}")
    print("  SUGGESTED TIER PICKS (cheap = lowest 33%, mid = middle, flagship = highest 33%)")
    print(f"{'='*100}")
    for prov, models in by_provider.items():
        models_sorted = sorted(models, key=get_completion_price_per_mtok)
        valid = [m for m in models_sorted if get_completion_price_per_mtok(m) < float("inf")]
        if len(valid) == 0:
            print(f"  {prov:<14}: NO DATA")
            continue
        if len(valid) < 3:
            print(f"  {prov:<14}: only {len(valid)} priced model(s) - flagship-only candidate")
            for m in valid:
                cp = get_completion_price_per_mtok(m)
                print(f"                  -> {m['id']:<50} ${cp:.2f}/Mtok completion")
            continue
        n = len(valid)
        cheap_idx = n // 3 - 1 if n // 3 > 0 else 0
        mid_idx = n // 2
        flag_idx = n - 1
        cheap = valid[cheap_idx]
        mid = valid[mid_idx]
        flag = valid[flag_idx]
        # Skip degenerate cases where same slug
        if cheap["id"] == flag["id"]:
            print(f"  {prov:<14}: only 1 distinct model - flagship-only candidate")
            continue
        print(f"  {prov:<14}: cheap='{cheap['id']}'  mid='{mid['id']}'  flagship='{flag['id']}'")

    # Save full output
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    import datetime as dt
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = output_dir / f"phase2l_catalog_search_{ts}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print(f"\nFull catalog dump saved: {out_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
