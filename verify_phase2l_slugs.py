"""
Phase 2L · Pre-flight Check 1: Verify all 39 candidate model slugs exist on
OpenRouter and report their actual pricing.

This is the most important check. Phase 2J had Opus 4.8 cost=$0 because its
slug existed in /chat/completions but NOT in /models catalog - so pricing was
empty, manual fallback wrote $0.

This script catches that BEFORE we spend any real money.

Cost: $0. Makes a single GET /api/v1/models call. No inference.

Usage:
    set OPENROUTER_API_KEY=sk-or-...
    python verify_phase2l_slugs.py [--config config_phase2l.yaml]

Output:
    - Console report grouped by provider/tier
    - JSON: ./pre_flight/phase2l_slug_verification_<timestamp>.json
    - Action items: list of slugs to swap with fallback or drop
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import datetime as dt
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip install requests")
    sys.exit(1)


OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"


def load_config(config_path: Path) -> dict[str, Any]:
    with open(config_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def fetch_openrouter_catalog(api_key: str | None) -> list[dict[str, Any]]:
    """Fetch the live OpenRouter catalog. API key optional for /models endpoint."""
    headers = {"Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    print(f"Fetching catalog from {OPENROUTER_MODELS_URL} ...")
    resp = requests.get(OPENROUTER_MODELS_URL, headers=headers, timeout=30)
    resp.raise_for_status()
    payload = resp.json()
    if not isinstance(payload, dict) or "data" not in payload:
        raise RuntimeError(f"Unexpected payload shape: {list(payload)[:3]}")
    models = payload["data"]
    print(f"Catalog returned {len(models)} models.\n")
    return models


def index_catalog(catalog: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Index catalog by id for fast lookup."""
    return {m["id"]: m for m in catalog if "id" in m}


def parse_pricing(model: dict[str, Any]) -> dict[str, Any]:
    """Extract usable pricing fields. OpenRouter pricing is per token (USD)."""
    p = model.get("pricing", {}) or {}
    return {
        "prompt": float(p.get("prompt") or 0),
        "completion": float(p.get("completion") or 0),
        "request": float(p.get("request") or 0),
        "image": float(p.get("image") or 0),
        "context_length": model.get("context_length"),
        "raw_pricing": p,
    }


def verify_slug(
    slug: str,
    fallback_slug: str | None,
    catalog_index: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Check primary slug, then fallback. Return status report."""
    result: dict[str, Any] = {
        "slug": slug,
        "fallback_slug": fallback_slug,
        "primary_found": False,
        "fallback_found": False,
        "primary_pricing": None,
        "fallback_pricing": None,
        "resolved_slug": None,
        "resolved_pricing": None,
        "status": "MISSING",
    }

    if slug in catalog_index:
        result["primary_found"] = True
        result["primary_pricing"] = parse_pricing(catalog_index[slug])

    if fallback_slug and fallback_slug in catalog_index:
        result["fallback_found"] = True
        result["fallback_pricing"] = parse_pricing(catalog_index[fallback_slug])

    if result["primary_found"]:
        pricing = result["primary_pricing"]
        if pricing["prompt"] > 0 or pricing["completion"] > 0:
            result["status"] = "OK"
            result["resolved_slug"] = slug
            result["resolved_pricing"] = pricing
        else:
            result["status"] = "PRIMARY_ZERO_PRICING"
            if result["fallback_found"]:
                fp = result["fallback_pricing"]
                if fp["prompt"] > 0 or fp["completion"] > 0:
                    result["status"] = "FALLBACK_USED"
                    result["resolved_slug"] = fallback_slug
                    result["resolved_pricing"] = fp
    elif result["fallback_found"]:
        fp = result["fallback_pricing"]
        if fp["prompt"] > 0 or fp["completion"] > 0:
            result["status"] = "FALLBACK_USED"
            result["resolved_slug"] = fallback_slug
            result["resolved_pricing"] = fp
        else:
            result["status"] = "BOTH_ZERO_PRICING"

    return result


def format_pricing_per_million(pricing: dict[str, Any] | None) -> str:
    if pricing is None:
        return "n/a"
    p = pricing["prompt"] * 1_000_000
    c = pricing["completion"] * 1_000_000
    return f"${p:.2f}/${c:.2f} per Mtok"


def status_icon(status: str) -> str:
    return {
        "OK": "[OK]      ",
        "FALLBACK_USED": "[FALLBACK]",
        "PRIMARY_ZERO_PRICING": "[ZERO $]  ",
        "BOTH_ZERO_PRICING": "[NO $]    ",
        "MISSING": "[MISSING] ",
    }.get(status, "[?]       ")


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 2L pre-flight check 1: slug verification")
    parser.add_argument("--config", default="config_phase2l.yaml")
    parser.add_argument("--output-dir", default="./pre_flight")
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"ERROR: config not found: {config_path}")
        return 2

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("WARNING: OPENROUTER_API_KEY not set in environment.")
        print("         /models endpoint works without auth but the call may be rate-limited.")
        print("         Continuing without key.\n")

    config = load_config(config_path)
    candidate_models = config.get("models", [])
    if not candidate_models:
        print("ERROR: config has no 'models' section.")
        return 2

    print(f"Loaded {len(candidate_models)} candidate models from {config_path.name}.\n")

    catalog = fetch_openrouter_catalog(api_key)
    catalog_index = index_catalog(catalog)

    results = []
    print(f"{'Status':<10} {'short':<6} {'family':<10} {'tier':<10} {'slug':<50} pricing")
    print("-" * 130)

    by_provider: dict[str, list[dict[str, Any]]] = {}

    for entry in candidate_models:
        slug = entry["id"]
        fallback = entry.get("fallback_id")
        family = entry.get("family", "?")
        tier = entry.get("tier", "?")
        short = entry.get("short_name", "?")

        check = verify_slug(slug, fallback, catalog_index)
        check["short_name"] = short
        check["family"] = family
        check["tier"] = tier
        results.append(check)

        by_provider.setdefault(family, []).append(check)

        line = f"{status_icon(check['status'])} {short:<6} {family:<10} {tier:<10} {slug:<50}"
        if check["status"] in ("OK", "FALLBACK_USED"):
            line += " " + format_pricing_per_million(check["resolved_pricing"])
            if check["status"] == "FALLBACK_USED":
                line += f"  (using fallback: {check['resolved_slug']})"
        elif check["status"] == "PRIMARY_ZERO_PRICING":
            line += f"  slug exists but pricing is ZERO - this is the Phase 2J bug"
        else:
            line += f"  not found in catalog"
        print(line)

    print("-" * 130)

    # Summary
    counts: dict[str, int] = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    print("\nSummary:")
    for status, n in sorted(counts.items()):
        print(f"  {status_icon(status)} {n}")
    ok = counts.get("OK", 0) + counts.get("FALLBACK_USED", 0)
    total = len(results)
    print(f"\n  Usable: {ok}/{total} ({100*ok/total:.0f}%)")

    # Per-provider tier completeness
    print("\nPer-provider tier completeness (cheap / mid / flagship):")
    for fam, checks in sorted(by_provider.items()):
        tiers_ok = {c["tier"]: c["status"] in ("OK", "FALLBACK_USED") for c in checks}
        line = f"  {fam:<10} "
        for t in ("cheap", "mid", "flagship"):
            symbol = "OK" if tiers_ok.get(t) else "--"
            line += f" {t}={symbol}"
        all_ok = all(tiers_ok.values())
        line += f"   {'COMPLETE' if all_ok else 'INCOMPLETE'}"
        print(line)

    # Action items
    actions = []
    for r in results:
        if r["status"] == "MISSING":
            actions.append(f"  - {r['short_name']} ({r['family']}/{r['tier']}): slug {r['slug']} MISSING. Find alternative or drop this tier slot.")
        elif r["status"] == "PRIMARY_ZERO_PRICING":
            actions.append(f"  - {r['short_name']} ({r['family']}/{r['tier']}): slug {r['slug']} has ZERO pricing. Check if it's free model, or replace.")
        elif r["status"] == "BOTH_ZERO_PRICING":
            actions.append(f"  - {r['short_name']} ({r['family']}/{r['tier']}): both primary and fallback have zero pricing. Drop or find live model.")

    if actions:
        print("\nAction items:")
        for a in actions:
            print(a)
    else:
        print("\nNo action items. All slugs verified with valid pricing. Proceed to Check 2.")

    # Save JSON
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = output_dir / f"phase2l_slug_verification_{ts}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "timestamp": ts,
                "catalog_total_models": len(catalog),
                "candidates_checked": len(results),
                "summary": counts,
                "results": results,
            },
            f,
            indent=2,
        )
    print(f"\nReport saved: {out_path}")

    # Exit non-zero if anything is missing - useful for CI / gating
    if counts.get("MISSING", 0) > 0 or counts.get("BOTH_ZERO_PRICING", 0) > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
