#!/usr/bin/env python3
"""
Verify Phase 2H model IDs against current OpenRouter availability.
Cost: free (one GET request to /api/v1/models).
Critical to run before launching Phase 2H to avoid mid-experiment failure.

Run:
    python verify_phase2h_models.py
"""
from __future__ import annotations
import os
import sys
import requests

PHASE2H_MODELS = [
    # (short_name, primary_id, fallback_id)
    ("M1", "anthropic/claude-opus-4.7",        "anthropic/claude-sonnet-4.6"),
    ("M2", "openai/gpt-5.5",                   "openai/gpt-5.4"),
    ("M3", "google/gemini-3.1-pro-preview",    "google/gemini-2.5-pro"),
    ("M4", "deepseek/deepseek-v4-pro",         "deepseek/deepseek-v4-flash"),
    ("M5", "moonshotai/kimi-k2.6",             "moonshotai/kimi-k2.5"),
    ("M6", "mistralai/mistral-large-2512",     "mistralai/mistral-large-2411"),
    ("M7", "cohere/command-a",                 "cohere/command-r-plus-08-2024"),
    ("M8", "qwen/qwen3.7-max",                 "qwen/qwen3.6-max-preview"),
    ("M9", "meta-llama/llama-4-maverick",      "meta-llama/llama-3.3-70b-instruct"),
    ("M10", "x-ai/grok-4.20",                  "x-ai/grok-4.3"),
]


def main() -> int:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set", file=sys.stderr)
        return 1

    print("Fetching OpenRouter model list...")
    r = requests.get(
        "https://openrouter.ai/api/v1/models",
        headers={"Authorization": f"Bearer {api_key}"},
        timeout=20,
    )
    if r.status_code != 200:
        print(f"ERROR: OpenRouter returned {r.status_code}", file=sys.stderr)
        return 1

    data = r.json().get("data", [])
    available_ids = {m["id"] for m in data}
    print(f"  {len(available_ids)} models available on OpenRouter\n")

    primary_missing = []
    fallback_missing = []
    suggestions = {}

    print(f"{'Slot':<5} {'Primary':<45} {'Status':<10} {'Fallback':<40} {'Status':<10}")
    print("-" * 115)
    for short, primary, fallback in PHASE2H_MODELS:
        primary_ok = primary in available_ids
        fallback_ok = fallback in available_ids
        print(f"{short:<5} {primary:<45} {'OK' if primary_ok else 'MISSING':<10} "
              f"{fallback:<40} {'OK' if fallback_ok else 'MISSING':<10}")

        if not primary_ok:
            primary_missing.append((short, primary))
        if not fallback_ok:
            fallback_missing.append((short, fallback))

        # Suggest similar IDs for missing models (substring match on lab name)
        # Show ALL candidates from the lab, not just first 8 alphabetically.
        if not primary_ok or not fallback_ok:
            lab = primary.split("/")[0]
            similar = sorted([m for m in available_ids if m.startswith(lab + "/")])
            if similar:
                suggestions[short] = similar  # full list

    print()
    if primary_missing:
        print(f"PRIMARY MODELS MISSING ({len(primary_missing)}):")
        for short, mid in primary_missing:
            print(f"  {short}: {mid}")
        print()
    if fallback_missing:
        print(f"FALLBACK MODELS MISSING ({len(fallback_missing)}):")
        for short, mid in fallback_missing:
            print(f"  {short}: {mid}")
        print()

    if suggestions:
        print("=== SUGGESTED REPLACEMENTS (from same lab on OpenRouter) ===\n")
        for short, opts in suggestions.items():
            print(f"{short}: {len(opts)} candidates from this lab")
            for o in opts:
                print(f"    - {o}")
            print()

    if not primary_missing and not fallback_missing:
        print("=== ALL MODEL IDs VALID. SAFE TO LAUNCH PHASE 2H. ===")
        return 0
    else:
        n_blocked = sum(1 for short, _ in primary_missing
                        if short in [s for s, _ in fallback_missing if s == short])
        print(f"=== {len(primary_missing)} primary models need attention before launch ===")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
