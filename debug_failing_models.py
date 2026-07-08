"""
Phase 2L · Quick debug: identify why models are returning $0 / 0 ratings fast.

Tests one of the failing models with verbose output - shows actual HTTP status,
error body, and OpenRouter account balance.

Cost: <$0.01 (single call per model).
Usage:
    set OPENROUTER_API_KEY=sk-or-...
    python debug_failing_models.py
"""
from __future__ import annotations

import json
import os
import sys
import requests


FAILING_MODELS = [
    ("M_C", "mistralai/ministral-3b-2512"),
    ("Z_C", "z-ai/glm-4-32b"),
    ("Q_C", "qwen/qwen-2.5-7b-instruct"),
    ("K_F", "moonshotai/kimi-k2.6"),
    ("Z_F", "z-ai/glm-5.1"),
    ("N_C", "nvidia/nemotron-nano-9b-v2"),
    ("N_M", "nvidia/llama-3.3-nemotron-super-49b-v1.5"),
]


def main() -> int:
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set.")
        print("Set it: $env:OPENROUTER_API_KEY = 'sk-or-v1-...'")
        return 2

    print("=" * 100)
    print("STEP 1: Check OpenRouter account balance & key validity")
    print("=" * 100)
    try:
        resp = requests.get(
            "https://openrouter.ai/api/v1/auth/key",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        print(f"HTTP {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json().get("data", {})
            print(f"  Label:        {data.get('label', 'n/a')}")
            print(f"  Usage:        ${data.get('usage', 0):.4f}")
            print(f"  Limit:        ${data.get('limit', 'unlimited')}")
            print(f"  Remaining:    ${data.get('limit_remaining', 'n/a')}")
            print(f"  Is free tier: {data.get('is_free_tier', False)}")
            print(f"  Is provisioning: {data.get('is_provisioning_key', False)}")
        else:
            print(f"  Body: {resp.text[:500]}")
            print(f"\n  → API key issue. Cannot proceed.")
            return 1
    except Exception as e:
        print(f"  ERROR: {type(e).__name__}: {e}")
        return 1

    print(f"\n{'=' * 100}")
    print("STEP 2: Test failing models one by one")
    print("=" * 100)

    failures = []
    for short, slug in FAILING_MODELS:
        print(f"\n[{short}] {slug}")
        try:
            resp = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://crossmodelrg.org",
                    "X-Title": "CM-RG Debug",
                },
                json={
                    "model": slug,
                    "messages": [{"role": "user", "content": "Say 'hi' in one word."}],
                    "max_tokens": 50,
                    "temperature": 0.0,
                    "usage": {"include": True},
                },
                timeout=30,
            )
            print(f"  HTTP {resp.status_code}")
            try:
                body = resp.json()
                if resp.status_code == 200:
                    # Show usage and short content
                    choices = body.get("choices", [])
                    content = ""
                    if choices and isinstance(choices[0], dict):
                        content = (choices[0].get("message") or {}).get("content", "")
                    usage = body.get("usage", {})
                    print(f"  Content: {content[:80]!r}")
                    print(f"  Usage cost: ${usage.get('cost', 'n/a')}")
                    if usage.get("cost", 0) == 0:
                        print(f"  WARNING: cost=$0 even on 200 OK")
                        failures.append((short, "ZERO_COST"))
                    print(f"  Status: OK")
                else:
                    print(f"  Error body: {json.dumps(body, indent=2)[:500]}")
                    failures.append((short, f"HTTP_{resp.status_code}"))
            except json.JSONDecodeError:
                print(f"  Non-JSON body: {resp.text[:300]}")
                failures.append((short, "NON_JSON"))
        except Exception as e:
            print(f"  EXCEPTION: {type(e).__name__}: {e}")
            failures.append((short, type(e).__name__))

    print(f"\n{'=' * 100}")
    print("SUMMARY")
    print("=" * 100)
    if failures:
        print(f"FAILED ({len(failures)}/{len(FAILING_MODELS)}):")
        for short, reason in failures:
            print(f"  {short:<6} - {reason}")
    else:
        print(f"All {len(FAILING_MODELS)} models OK!")

    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
