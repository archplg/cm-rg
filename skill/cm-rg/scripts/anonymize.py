#!/usr/bin/env python3
"""CM-RG Phase 2: anonymize free responses and assign shuffled element labels.

Usage:
    python anonymize.py phase1_responses.json outdir/ [--seed 42]

Input : JSON list [{"model": "...", "text": "..."}]
Output: outdir/anonymized.json  [{"element": "E1", "text": "..."}]  (shuffled order)
        outdir/mapping.json     {"E1": "model-name", ...}  -- NEVER show to raters

Patterns ported verbatim from the Archipelago Phase 2L pipeline (run_phase2l.py).
"""
import argparse
import json
import random
import re
import sys
from pathlib import Path

ANON_PATTERNS = [
    (re.compile(r"(?i)\b(I\s+am\s+|I'm\s+)(claude|gpt|chatgpt|gemini|llama|mistral|deepseek|grok|qwen|kimi|glm|nemotron|command|granite)\b[^.]*\."), ""),
    (re.compile(r"(?i)\b(as\s+an\s+ai\s+(language\s+)?model|as\s+a\s+language\s+model)\b[^.]*\."), ""),
    (re.compile(r"(?i)\b(I\s+should\s+(note|mention|clarify)|it's\s+worth\s+noting)\b[^.]*\."), ""),
    (re.compile(r"(?i)\b(developed\s+by|trained\s+by|built\s+by)\s+(anthropic|openai|google|meta|mistral|deepseek|xai|alibaba|moonshot|zhipu|nvidia|cohere|ibm)\b[^.]*\."), ""),
    (re.compile(r"(?i)\b(Claude|GPT-?\d?\.?\d?|Gemini|LLaMA|Mistral|DeepSeek|Grok|Qwen|Kimi|GLM|Nemotron|Command|Granite)\b"), "[MODEL]"),
    (re.compile(r"(?i)\b(Anthropic|OpenAI|Google DeepMind|DeepMind|Meta AI|Mistral AI|xAI|Alibaba|Moonshot|Zhipu|NVIDIA|Cohere|IBM Research)\b"), "[LAB]"),
]


def anonymize_text(text: str) -> str:
    out = text
    for pat, repl in ANON_PATTERNS:
        out = pat.sub(repl, out)
    return re.sub(r"\s+", " ", out).strip()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("responses", help="phase1_responses.json")
    ap.add_argument("outdir")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    responses = json.loads(Path(args.responses).read_text(encoding="utf-8"))
    if not isinstance(responses, list) or not all("model" in r and "text" in r for r in responses):
        print("ERROR: input must be a JSON list of {model, text} objects", file=sys.stderr)
        return 1

    rng = random.Random(args.seed)
    order = list(range(len(responses)))
    rng.shuffle(order)

    anonymized, mapping = [], {}
    for label_idx, src_idx in enumerate(order, start=1):
        label = f"E{label_idx}"
        anonymized.append({"element": label, "text": anonymize_text(responses[src_idx]["text"])})
        mapping[label] = responses[src_idx]["model"]

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "anonymized.json").write_text(
        json.dumps(anonymized, indent=2, ensure_ascii=False), encoding="utf-8")
    (outdir / "mapping.json").write_text(
        json.dumps(mapping, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Anonymized {len(anonymized)} responses -> {outdir}/anonymized.json")
    print("mapping.json written - do not include it in any rater prompt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
