#!/usr/bin/env python3
"""
Claude-as-rater construct validation (free alternative to human inter-rater study).

Takes a sample of N elicited constructs and asks Claude (separate from the
experiment) to classify each into one of the semantic clusters identified by
construct_decomposition.py. Computes inter-rater agreement between:
  - embedding-based KMeans clusters (algorithmic)
  - Claude's manual coding (LLM-as-rater)

This is a "free" version of the human-coding validation step. For true
publication-quality, a human inter-rater study is still needed - this script
gives a reasonable lower bound.

Outputs:
  validation/CONSTRUCT_VALIDATION_FINDINGS.md
  validation/cohen_kappa.csv

Run:
    pip install requests scikit-learn
    python construct_validation.py [--n_sample 100] [--model anthropic/claude-opus-4.7]
"""
from __future__ import annotations
import argparse
import json
import os
import random
import time
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from sklearn.metrics import cohen_kappa_score, confusion_matrix

RESULTS_DIR = Path("./results")
CONSTRUCT_ANALYSIS_DIR = Path("./construct_analysis")
OUT_DIR = Path("./validation")


def load_constructs_with_clusters() -> pd.DataFrame:
    """Load all elicited constructs and their assigned clusters."""
    p = CONSTRUCT_ANALYSIS_DIR / "decomposition_results.json"
    if not p.exists():
        print(f"ERROR: {p} not found. Run construct_decomposition.py first.")
        return pd.DataFrame()
    with open(p, encoding="utf-8") as f:
        decomp = json.load(f)
    cluster_labels = decomp.get("decomp1", {}).get("labels", [])
    examples = decomp.get("decomp1", {}).get("examples", {})

    rows = []
    for cd in sorted(RESULTS_DIR.iterdir()):
        if not cd.is_dir():
            continue
        cell_file = cd / "cell.json"
        if not cell_file.exists():
            continue
        with open(cell_file, encoding="utf-8") as f:
            cell = json.load(f)
        if not cell.get("status", "").startswith("complete"):
            continue
        for model, constructs in cell.get("constructs", {}).items():
            for item in constructs:
                left = item.get("left", "").strip()
                right = item.get("right", "").strip()
                if left and right:
                    rows.append({
                        "cell_id": cd.name,
                        "task": cell.get("task"),
                        "model": model,
                        "left": left,
                        "right": right,
                        "combined": f"{left} -- {right}",
                    })
    df = pd.DataFrame(rows)
    # Add KMeans cluster labels (assumes same load order as construct_decomposition.py)
    if len(cluster_labels) == len(df):
        df["kmeans_cluster"] = cluster_labels
    else:
        print(f"WARNING: cluster labels length ({len(cluster_labels)}) != "
              f"constructs ({len(df)}). Re-run construct_decomposition.py first.")
        df["kmeans_cluster"] = None
    return df, examples


def build_classification_prompt(construct: str, cluster_descriptions: dict) -> tuple[str, str]:
    """Build a system + user prompt asking Claude to classify one construct."""
    sys_prompt = (
        "You are a research assistant classifying bipolar evaluation constructs into "
        "predefined semantic clusters. Each construct describes a dimension along "
        "which decision options were evaluated. Your task is to identify which "
        "cluster a given construct best fits into. Be precise and decisive."
    )
    options_text = "\n".join(
        f"Cluster {k}: example - \"{v[0][:200]}\""
        for k, v in cluster_descriptions.items()
    )
    user_msg = (
        f"Classify the following bipolar construct into one of the predefined "
        f"clusters. Output ONLY the cluster number (e.g., '3'), nothing else.\n\n"
        f"Construct to classify:\n  {construct}\n\n"
        f"Available clusters:\n{options_text}\n\n"
        f"Cluster number:"
    )
    return sys_prompt, user_msg


def call_openrouter(api_key: str, model: str, sys_prompt: str, user_msg: str,
                    timeout: int = 120, raw_log_path: Path = None) -> str | None:
    """Call OpenRouter with enough max_tokens budget for reasoning models.

    Bumped max_tokens from 50 to 2000 to accommodate thinking models
    (GPT-5.x, Gemini Thinking, Kimi k2.6 etc.) that consume budget on
    reasoning_tokens before producing visible output.
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://archplg.co.uk",
        "X-Title": "Archipelago construct validation",
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_msg},
        ],
        "temperature": 0.0,
        "max_tokens": 2000,   # was 50 - reasoning models need budget for thinking
    }
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=timeout)
        if r.status_code != 200:
            if raw_log_path:
                with open(raw_log_path, "a", encoding="utf-8") as fh:
                    fh.write(f"HTTP {r.status_code}: {r.text[:300]}\n")
            return None
        data = r.json()
        content = data["choices"][0]["message"].get("content")
        finish = data["choices"][0].get("finish_reason", "unknown")
        # Log raw responses for debugging cross-model parsing issues
        if raw_log_path:
            usage = data.get("usage", {})
            with open(raw_log_path, "a", encoding="utf-8") as fh:
                fh.write(f"finish={finish} tokens={usage} content={repr(content)[:200]}\n")
        return content
    except Exception as exc:
        if raw_log_path:
            with open(raw_log_path, "a", encoding="utf-8") as fh:
                fh.write(f"EXCEPTION: {exc}\n")
        print(f"  API error: {exc}")
        return None


def parse_cluster_id(response: str) -> int | None:
    """Extract first integer from response."""
    if not response:
        return None
    import re
    m = re.search(r"\b(\d+)\b", response)
    if m:
        try:
            return int(m.group(1))
        except ValueError:
            return None
    return None


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--n_sample", type=int, default=100,
                   help="Number of constructs to validate (default: 100)")
    p.add_argument("--model", default="anthropic/claude-opus-4.7",
                   help="OpenRouter model ID for the rater")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--out", default=str(OUT_DIR))
    args = p.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set in environment.")
        return 1

    print(f"Loading constructs with cluster labels...")
    df, examples = load_constructs_with_clusters()
    if df.empty:
        return 1
    print(f"  {len(df)} constructs loaded")
    valid = df[df["kmeans_cluster"].notna()].copy()
    if len(valid) < 10:
        print(f"  Too few labeled constructs ({len(valid)}). Re-run decomp first.")
        return 1
    print(f"  {len(valid)} with cluster labels")

    rng = random.Random(args.seed)
    sample_n = min(args.n_sample, len(valid))
    sample = valid.sample(n=sample_n, random_state=args.seed).reset_index(drop=True)
    print(f"\nSampling {sample_n} constructs for Claude validation")
    print(f"Estimated cost: ${sample_n * 0.003:.2f} (~50 tokens per call)")

    # Call rater for each
    raw_log_path = out_dir / "raw_responses.log"
    raw_log_path.write_text("", encoding="utf-8")   # clear from any prior run
    model_short = args.model.split("/")[-1]
    print(f"\nCalling {args.model} for classification...")
    print(f"Raw responses logged to: {raw_log_path}")
    rater_labels = []
    parse_failures = 0
    for i, row in sample.iterrows():
        sys_p, user_p = build_classification_prompt(row["combined"], examples)
        response = call_openrouter(api_key, args.model, sys_p, user_p,
                                    raw_log_path=raw_log_path)
        cid = parse_cluster_id(response)
        if cid is None and response:
            parse_failures += 1
        rater_labels.append(cid)
        if (i + 1) % 10 == 0:
            print(f"  {i+1}/{sample_n} done (parse failures so far: {parse_failures})")
        time.sleep(0.5)  # be gentle to API
    claude_labels = rater_labels   # backward compat var name

    sample["claude_cluster"] = claude_labels
    sample["match"] = (sample["kmeans_cluster"] == sample["claude_cluster"])

    # Drop unsuccessful classifications
    successful = sample.dropna(subset=["claude_cluster"]).copy()
    successful["claude_cluster"] = successful["claude_cluster"].astype(int)

    print(f"\nResults:")
    print(f"  Total sampled: {sample_n}")
    print(f"  Successfully classified by {model_short}: {len(successful)}")
    print(f"  Parse failures (non-empty response, no digit): {parse_failures}")

    if len(successful) >= 5:
        kappa = cohen_kappa_score(successful["kmeans_cluster"], successful["claude_cluster"])
        accuracy = (successful["kmeans_cluster"] == successful["claude_cluster"]).mean()
        print(f"  Inter-rater accuracy (KMeans vs Claude): {accuracy*100:.1f}%")
        print(f"  Cohen's kappa: {kappa:.3f}")

        # Confusion matrix
        n_clusters = len(set(successful["kmeans_cluster"]) | set(successful["claude_cluster"]))
        labels = sorted(set(successful["kmeans_cluster"]) | set(successful["claude_cluster"]))
        cm = confusion_matrix(successful["kmeans_cluster"], successful["claude_cluster"], labels=labels)
        cm_df = pd.DataFrame(cm, index=[f"KM_{l}" for l in labels],
                              columns=[f"Cl_{l}" for l in labels])
        cm_df.to_csv(out_dir / "confusion_matrix.csv")

        # Save detailed results
        successful.to_csv(out_dir / "sample_results.csv", index=False)
        with open(out_dir / "cohen_kappa.csv", "w", encoding="utf-8") as f:
            f.write(f"metric,value\naccuracy,{accuracy}\ncohen_kappa,{kappa}\nn_sample,{len(successful)}\n")

        # Markdown report
        lines = ["# Construct Cluster Validation: KMeans vs Claude\n\n"]
        lines.append(f"Sampled {sample_n} constructs (from {len(valid)} total). "
                      f"Asked {args.model} to classify each into one of the "
                      f"clusters identified by KMeans clustering in construct_decomposition.py.\n\n")
        lines.append(f"**Successfully classified by Claude**: {len(successful)} of {sample_n}\n\n")
        lines.append("## Headline metrics\n\n")
        lines.append(f"- **Accuracy** (Claude agrees with KMeans on cluster assignment): **{accuracy*100:.1f}%**\n")
        lines.append(f"- **Cohen's kappa** (agreement adjusted for chance): **{kappa:.3f}**\n\n")
        lines.append("## How to interpret\n\n")
        lines.append("- **kappa < 0.4**: poor agreement - KMeans clusters may not be semantically valid\n")
        lines.append("- **kappa 0.4-0.6**: moderate agreement - KMeans captures some structure but Claude sees different boundaries\n")
        lines.append("- **kappa 0.6-0.8**: substantial agreement - KMeans clusters are reasonable approximations of human-readable categories\n")
        lines.append("- **kappa > 0.8**: almost perfect agreement - KMeans matches semantic intuitions strongly\n\n")
        if kappa < 0.4:
            lines.append("**Verdict**: KMeans clusters do NOT have strong semantic validity. ")
            lines.append("Consider re-clustering with different parameters or report decomposition as exploratory.\n\n")
        elif kappa < 0.6:
            lines.append("**Verdict**: KMeans clusters have **moderate semantic validity**. ")
            lines.append("Acceptable for exploratory analysis; report with caveat.\n\n")
        elif kappa < 0.8:
            lines.append("**Verdict**: KMeans clusters have **substantial semantic validity**. ")
            lines.append("Acceptable for publication; cite Cohen's kappa in dataset card.\n\n")
        else:
            lines.append("**Verdict**: KMeans clusters have **excellent semantic validity**. ")
            lines.append("Strong publication signal for the decomposition approach.\n\n")

        lines.append("## Caveats\n\n")
        lines.append("- This is **LLM-as-rater**, not human inter-rater. Real inter-rater study with 3+ humans on Prolific would give stronger validation.\n")
        lines.append("- Claude as classifier may share biases with Claude as construct-elicitor (M1). Truly independent validation requires non-Anthropic model.\n")
        lines.append("- Confidence in kappa drops with small n. Run with --n_sample 200 for tighter estimate.\n")

        (out_dir / "CONSTRUCT_VALIDATION_FINDINGS.md").write_text("".join(lines), encoding="utf-8")
        print(f"\nWritten: {out_dir}/CONSTRUCT_VALIDATION_FINDINGS.md")
    else:
        print("ERROR: too few successful classifications for meaningful agreement statistics.")
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
