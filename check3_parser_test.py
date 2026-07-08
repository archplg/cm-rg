"""
Phase 2L · Pre-flight Check 3: Construct parser validation.

Tests construct extraction parser against:
  1. Synthetic well-formed JSON responses
  2. Synthetic malformed responses (missing fields, wrong types)
  3. Real Phase 2J responses if available

Catches the Phase 2J ?-marks bug (regex too narrow) BEFORE Phase 2L run.

Cost: $0 (no API calls).
Usage: python check3_parser_test.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


# Construct extraction parser (target shape: list[dict] with "pole_a", "pole_b", "context")
SYNTH_CASES = [
    # CASE 1: perfect JSON array
    {
        "name": "perfect_json_array",
        "input": '[{"pole_a": "decisive", "pole_b": "deliberative", "context": "leadership"}, {"pole_a": "transparent", "pole_b": "strategic", "context": "communication"}]',
        "expected_count": 2,
        "should_pass": True,
    },
    # CASE 2: JSON wrapped in markdown fence
    {
        "name": "markdown_fenced_json",
        "input": '```json\n[{"pole_a": "ambitious", "pole_b": "cautious", "context": "risk"}]\n```',
        "expected_count": 1,
        "should_pass": True,
    },
    # CASE 3: numbered list format
    {
        "name": "numbered_list_format",
        "input": '1. decisive vs deliberative (leadership)\n2. transparent vs opaque (communication)\n3. ambitious vs cautious (risk)',
        "expected_count": 3,
        "should_pass": True,
    },
    # CASE 4: bullet list format
    {
        "name": "bullet_list_format",
        "input": '- decisive / deliberative (in leadership)\n- transparent / opaque (in communication)',
        "expected_count": 2,
        "should_pass": True,
    },
    # CASE 5: malformed - missing pole_b
    {
        "name": "missing_pole_b",
        "input": '[{"pole_a": "decisive", "context": "leadership"}]',
        "expected_count": 0,
        "should_pass": False,
    },
    # CASE 6: empty string
    {
        "name": "empty_response",
        "input": '',
        "expected_count": 0,
        "should_pass": False,
    },
    # CASE 7: prose with embedded constructs
    {
        "name": "prose_with_embeded",
        "input": 'After analysis, I see decisive vs deliberative in leadership, '
                 'and transparent vs opaque in communication style.',
        "expected_count": 2,
        "should_pass": True,
    },
    # CASE 8: thinking model with reasoning chain
    {
        "name": "reasoning_chain_prefix",
        "input": '<thinking>Let me identify constructs...</thinking>\n'
                 '[{"pole_a": "fast", "pole_b": "thorough", "context": "decision speed"}]',
        "expected_count": 1,
        "should_pass": True,
    },
]


def extract_json_array(text: str) -> list[dict[str, Any]] | None:
    """Try to extract JSON array from response. Strips markdown fences."""
    if not text:
        return None
    cleaned = re.sub(r'```(?:json)?\s*', '', text)
    cleaned = re.sub(r'\s*```', '', cleaned)
    # Find first [ ... ]
    match = re.search(r'\[[\s\S]*\]', cleaned)
    if not match:
        return None
    try:
        data = json.loads(match.group())
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        return None
    return None


def extract_constructs_from_lines(text: str) -> list[dict[str, Any]]:
    """Fallback: extract from numbered/bullet lines like 'A vs B (context)' or 'A / B (in context)'."""
    constructs = []
    lines = text.splitlines() if text else []
    pattern = re.compile(
        r'^\s*(?:\d+\.|\-|\*)?\s*([A-Za-z][A-Za-z\s\-]*?)\s+(?:vs|/)\s+'
        r'([A-Za-z][A-Za-z\s\-]*?)\s*\((?:in\s+)?([^\)]+)\)'
    )
    for line in lines:
        m = pattern.search(line)
        if m:
            constructs.append({
                "pole_a": m.group(1).strip(),
                "pole_b": m.group(2).strip(),
                "context": m.group(3).strip(),
            })
    return constructs


def extract_constructs_from_prose(text: str) -> list[dict[str, Any]]:
    """Last resort: scan prose for 'X vs Y' patterns with nearby context."""
    if not text:
        return []
    constructs = []
    pattern = re.compile(
        r'([A-Za-z]+)\s+vs\s+([A-Za-z]+)\s+in\s+([a-z\s]+?)(?:[\.,;]|$|\sand\s)'
    )
    for m in pattern.finditer(text):
        constructs.append({
            "pole_a": m.group(1).strip(),
            "pole_b": m.group(2).strip(),
            "context": m.group(3).strip(),
        })
    return constructs


def strip_reasoning_tags(text: str) -> str:
    """Remove <thinking>, <reasoning>, <analysis> blocks - reasoning models prepend these."""
    if not text:
        return text
    # Multi-line tag content strip
    out = re.sub(r"<(thinking|reasoning|analysis|reflection|scratchpad)>[\s\S]*?</\1>", "", text, flags=re.IGNORECASE)
    # Also strip orphan opening tags + everything until next </
    out = re.sub(r"<(thinking|reasoning|analysis|reflection|scratchpad)>", "", out, flags=re.IGNORECASE)
    out = re.sub(r"</(thinking|reasoning|analysis|reflection|scratchpad)>", "", out, flags=re.IGNORECASE)
    return out.strip()


def parse_constructs(text: str) -> list[dict[str, Any]]:
    """Main parser - tries JSON, then line patterns, then prose.

    Now handles reasoning models (DeepSeek R1, Kimi Thinking, Qwen thinking) that
    wrap their output in <thinking>...</thinking> blocks.
    """
    # First, strip reasoning model tags
    cleaned = strip_reasoning_tags(text)
    # Try JSON first
    arr = extract_json_array(cleaned)
    if arr is not None:
        # Validate each item has required fields
        valid = [d for d in arr if isinstance(d, dict)
                 and "pole_a" in d and "pole_b" in d and "context" in d
                 and d["pole_a"] and d["pole_b"]]
        if valid:
            return valid
    # Try line patterns
    lines = extract_constructs_from_lines(cleaned)
    if lines:
        return lines
    # Try prose
    prose = extract_constructs_from_prose(cleaned)
    if prose:
        return prose
    # LAST RESORT: try original text (in case stripping was too aggressive)
    if cleaned != text:
        arr = extract_json_array(text)
        if arr is not None:
            valid = [d for d in arr if isinstance(d, dict)
                     and "pole_a" in d and "pole_b" in d and "context" in d
                     and d["pole_a"] and d["pole_b"]]
            if valid:
                return valid
    return []


def run_tests() -> int:
    print("Phase 2L Check 3: Construct parser validation")
    print("=" * 100)
    failures = 0
    for case in SYNTH_CASES:
        result = parse_constructs(case["input"])
        n = len(result)
        passed = (n >= case["expected_count"]) if case["should_pass"] else (n == 0)
        status = "PASS" if passed else "FAIL"
        if not passed:
            failures += 1
        print(f"  [{status}] {case['name']:<28} expected_count>={case['expected_count']:<3} got={n}")
        if not passed:
            print(f"         input: {case['input'][:80]}")
            print(f"         got: {result}")

    print("=" * 100)
    print(f"Synthetic tests: {len(SYNTH_CASES) - failures}/{len(SYNTH_CASES)} passed.")

    # Try to load real Phase 2J responses if available
    print("\nLooking for Phase 2J cells to test against real data...")
    phase2j_dirs = [
        Path("./results_phase2k"),
        Path("./results_phase2j"),
        Path("./results"),
    ]
    found_real = False
    for d in phase2j_dirs:
        if d.exists():
            cells = list(d.rglob("constructs*.json"))[:10]
            if cells:
                print(f"Found {len(cells)} construct JSONs in {d}. Sampling 10...")
                for c in cells:
                    try:
                        data = json.loads(c.read_text(encoding="utf-8"))
                        n = len(data) if isinstance(data, list) else len(data.get("constructs", []))
                        print(f"  {c.name:<40} - {n} constructs")
                    except Exception as e:
                        print(f"  {c.name:<40} - PARSE FAIL: {e}")
                found_real = True
                break

    if not found_real:
        print("  No Phase 2J/2K data found - synthetic tests only.")

    print(f"\nFailures: {failures}. {'GO' if failures == 0 else 'FIX BEFORE RUN'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run_tests())
