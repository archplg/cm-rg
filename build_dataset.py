#!/usr/bin/env python3
"""
Build a publication-quality dataset from the Archipelago experiment outputs.

Produces 5 Parquet tables + dataset card + citation + license in dataset_release/,
ready to upload to Zenodo (for DOI) and HuggingFace Hub.

Schema:
  cells.parquet      one row per cell - metadata + summary metrics
  constructs.parquet one row per elicited bipolar construct
  ratings.parquet    one row per (rater, construct, element) rating - LONG FORMAT
  responses.parquet  one row per free response from a model
  api_calls.parquet  one row per API call (full audit trail)

Plus:
  dataset_card.md    HuggingFace-style dataset documentation
  CITATION.cff       Citation File Format
  LICENSE            CC-BY 4.0 full text
  metadata.json      Croissant minimal metadata (ML datasets standard)

Run:
    pip install pyarrow pandas
    python build_dataset.py [--version v1.0]
"""
from __future__ import annotations
import argparse
import json
import hashlib
from datetime import datetime
from pathlib import Path
from collections import Counter

import pandas as pd

RESULTS_DIR = Path("./results")
LOGS_DIR = Path("./logs/api_calls")
ANALYSIS_DIR = Path("./analysis")
CONSTRUCT_ANALYSIS_DIR = Path("./construct_analysis")
OUT_DIR = Path("./dataset_release")

LICENSE_CC_BY_40 = """Creative Commons Attribution 4.0 International Public License

By exercising the Licensed Rights (defined below), You accept and agree to be
bound by the terms and conditions of this Creative Commons Attribution 4.0
International Public License ("Public License"). To the extent this Public
License may be interpreted as a contract, You are granted the Licensed Rights
in consideration of Your acceptance of these terms and conditions, and the
Licensor grants You such rights in consideration of benefits the Licensor
receives from making the Licensed Material available under these terms and
conditions.

Section 1 - Definitions.
[Standard CC-BY 4.0 definitions apply. Full legal text:
 https://creativecommons.org/licenses/by/4.0/legalcode]

You are free to:
  Share - copy and redistribute the material in any medium or format
  Adapt - remix, transform, and build upon the material for any purpose, even
          commercially.

Under the following terms:
  Attribution - You must give appropriate credit, provide a link to the license,
                and indicate if changes were made.

Suggested citation:
  Dolgov, S., with technical implementation by Claude assistant (2026).
  ACME-CrossLLM: Cross-Model LLM Construct Elicitation Dataset.
  Version {version}. Zenodo. DOI: [to be assigned]
"""


# ============================================================
# Data loaders
# ============================================================
def load_cells() -> list[dict]:
    """Load all completed cells from results/<cell>/cell.json."""
    cells = []
    if not RESULTS_DIR.exists():
        return cells
    for cd in sorted(RESULTS_DIR.iterdir()):
        if not cd.is_dir():
            continue
        cell_file = cd / "cell.json"
        if not cell_file.exists():
            continue
        with open(cell_file, encoding="utf-8") as f:
            cells.append(json.load(f))
    return cells


def load_summaries() -> dict:
    """Load analysis/all_summaries.json if exists - maps cell_id -> summary."""
    p = ANALYSIS_DIR / "all_summaries.json"
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as f:
        data = json.load(f)
    return {s["cell_id"]: s for s in data.get("summaries", []) if "cell_id" in s}


def load_construct_clusters() -> dict:
    """Load construct_analysis/decomposition_results.json - maps construct order to cluster id."""
    p = CONSTRUCT_ANALYSIS_DIR / "decomposition_results.json"
    if not p.exists():
        return {}
    with open(p, encoding="utf-8") as f:
        data = json.load(f)
    return data.get("decomp1", {})


# ============================================================
# Table builders
# ============================================================
def build_cells_table(cells: list[dict], summaries: dict) -> pd.DataFrame:
    rows = []
    for c in cells:
        cid = c.get("cell_id")
        summ = summaries.get(cid, {})
        # Count non-empty responses
        n_valid_responses = sum(
            1 for v in c.get("free_responses", {}).values()
            if isinstance(v, str) and v.strip()
        )
        # Count constructs with non-empty poles
        n_constructs_total = sum(
            len([x for x in v if x.get("left") and x.get("right")])
            for v in c.get("constructs", {}).values()
        )
        rows.append({
            "cell_id": cid,
            "task": c.get("task"),
            "condition": c.get("condition"),
            "run_idx": c.get("run_idx"),
            "status": c.get("status"),
            "started_at": c.get("started_at"),
            "completed_at": c.get("completed_at"),
            "random_seed": c.get("random_seed"),
            "n_valid_responses": n_valid_responses,
            "n_constructs": n_constructs_total,
            "n_raters": len(c.get("ratings", {})),
            "mean_pairwise_disagreement": summ.get("mean_pairwise_disagreement"),
            "pca_pc1": summ.get("pca_pc1"),
            "pca_pc2": summ.get("pca_pc2"),
            "pca_pc3": summ.get("pca_pc3"),
            "pc1_plus_pc2": summ.get("pca_pc1_plus_pc2"),
            "n_high_corr_pairs": summ.get("n_high_corr_pairs"),
            "n_saturated_pairs": summ.get("n_saturated_pairs"),
            "pct_high_corr": summ.get("pct_high_corr"),
            "cost_usd": c.get("cost_usd"),
            "tokens_in": c.get("tokens_in"),
            "tokens_out": c.get("tokens_out"),
            "n_errors": len(c.get("errors", [])),
        })
    return pd.DataFrame(rows)


def build_constructs_table(cells: list[dict], cluster_data: dict) -> pd.DataFrame:
    rows = []
    cluster_labels = cluster_data.get("labels", []) if cluster_data else []
    idx = 0
    for c in cells:
        cid = c.get("cell_id")
        # Persona assignment per model from api_calls
        persona_for = {}
        for call in c.get("api_calls", []):
            if call.get("phase") == "phase1_freeresponse":
                persona_for[call.get("model_short_name")] = call.get("persona_or_neutral", "neutral")
        for model, constructs in c.get("constructs", {}).items():
            persona = persona_for.get(model, "neutral")
            for k, item in enumerate(constructs):
                left = item.get("left", "").strip()
                right = item.get("right", "").strip()
                if not left or not right:
                    continue
                triad = item.get("triad", []) or []
                rows.append({
                    "construct_id": item.get("id"),
                    "cell_id": cid,
                    "task": c.get("task"),
                    "condition": c.get("condition"),
                    "run_idx": c.get("run_idx"),
                    "model": model,
                    "persona": persona,
                    "construct_order_in_model": k + 1,
                    "left_pole": left,
                    "right_pole": right,
                    "triad": ",".join(triad) if triad else "",
                    "raw_output_excerpt": item.get("raw_output_excerpt", "")[:300],
                    "semantic_cluster": (cluster_labels[idx] if idx < len(cluster_labels) else None),
                })
                idx += 1
    return pd.DataFrame(rows)


def build_ratings_table(cells: list[dict]) -> pd.DataFrame:
    rows = []
    rating_id = 0
    for c in cells:
        cid = c.get("cell_id")
        # Persona for raters
        persona_for = {}
        for call in c.get("api_calls", []):
            if call.get("phase") == "phase1_freeresponse":
                persona_for[call.get("model_short_name")] = call.get("persona_or_neutral", "neutral")
        # Element to source model mapping (which model produced E1, E2, etc.)
        element_origin = c.get("element_mapping", {})
        for rater_model, rating_dict in c.get("ratings", {}).items():
            rater_persona = persona_for.get(rater_model, "neutral")
            for construct_id, elem_ratings in rating_dict.items():
                construct_origin = construct_id.split("_")[1] if "_" in construct_id else "?"
                for element_label, rating in elem_ratings.items():
                    rating_id += 1
                    rows.append({
                        "rating_id": rating_id,
                        "cell_id": cid,
                        "task": c.get("task"),
                        "condition": c.get("condition"),
                        "run_idx": c.get("run_idx"),
                        "rater_model": rater_model,
                        "rater_persona": rater_persona,
                        "construct_id": construct_id,
                        "construct_origin_model": construct_origin,
                        "element_label": element_label,
                        "element_origin_model": element_origin.get(element_label, "?"),
                        "rating": int(rating),
                    })
    return pd.DataFrame(rows)


def build_responses_table(cells: list[dict]) -> pd.DataFrame:
    """One row per (cell, model) free response. Pull metadata from api_calls."""
    rows = []
    response_id = 0
    for c in cells:
        cid = c.get("cell_id")
        # Map model -> phase1 audit metadata
        phase1_meta = {}
        for call in c.get("api_calls", []):
            if call.get("phase") == "phase1_freeresponse":
                phase1_meta[call.get("model_short_name")] = call
        # Element label mapping
        inv_element = {sn: ek for ek, sn in c.get("element_mapping", {}).items()}
        for model, text in c.get("free_responses", {}).items():
            if not isinstance(text, str) or not text.strip():
                continue
            meta = phase1_meta.get(model, {})
            response_id += 1
            rows.append({
                "response_id": response_id,
                "cell_id": cid,
                "task": c.get("task"),
                "condition": c.get("condition"),
                "run_idx": c.get("run_idx"),
                "model": model,
                "model_id_used": meta.get("model_id_used"),
                "used_fallback": meta.get("used_fallback"),
                "persona": meta.get("persona_or_neutral", "neutral"),
                "element_label": inv_element.get(model),
                "response_text": text,
                "response_length_chars": len(text),
                "tokens_prompt": meta.get("prompt_tokens"),
                "tokens_completion": meta.get("completion_tokens"),
                "reasoning_tokens": meta.get("reasoning_tokens"),
                "latency_ms": meta.get("latency_ms"),
                "cost_usd": meta.get("cost_usd"),
                "finish_reason": meta.get("finish_reason"),
                "timestamp_iso": meta.get("timestamp_iso"),
            })
    return pd.DataFrame(rows)


def build_api_calls_table(cells: list[dict]) -> pd.DataFrame:
    """One row per API call across all phases."""
    rows = []
    call_id = 0
    for c in cells:
        cid = c.get("cell_id")
        for call in c.get("api_calls", []):
            call_id += 1
            rows.append({
                "call_id": call_id,
                "cell_id": cid,
                "task": c.get("task"),
                "condition": c.get("condition"),
                "run_idx": c.get("run_idx"),
                "phase": call.get("phase"),
                "model_short_name": call.get("model_short_name"),
                "model_id_used": call.get("model_id_used"),
                "used_fallback": call.get("used_fallback"),
                "persona_or_neutral": call.get("persona_or_neutral"),
                "attempts": call.get("attempts"),
                "timestamp_iso": call.get("timestamp_iso"),
                "latency_ms": call.get("latency_ms"),
                "prompt_tokens": call.get("prompt_tokens"),
                "completion_tokens": call.get("completion_tokens"),
                "reasoning_tokens": call.get("reasoning_tokens", 0),
                "finish_reason": call.get("finish_reason"),
                "cost_usd": call.get("cost_usd"),
                "audit_file": call.get("audit_file"),
            })
    return pd.DataFrame(rows)


# ============================================================
# Dataset card and metadata
# ============================================================
def _stat_row(name: str, value, fmt: str = "{}") -> str:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return f"- **{name}**: n/a\n"
    return f"- **{name}**: {fmt.format(value)}\n"


def build_dataset_card(df_cells, df_constructs, df_ratings, df_responses, df_api,
                        version: str) -> str:
    """Build a HuggingFace-style dataset card."""
    n_cells = len(df_cells)
    n_constructs = len(df_constructs)
    n_ratings = len(df_ratings)
    n_responses = len(df_responses)
    n_api = len(df_api)
    total_cost = df_cells["cost_usd"].sum() if "cost_usd" in df_cells else 0.0

    tasks = sorted(df_cells["task"].dropna().unique()) if "task" in df_cells else []
    models = sorted(df_responses["model"].dropna().unique()) if "model" in df_responses else []
    personas = sorted(df_responses["persona"].dropna().unique()) if "persona" in df_responses else []
    model_ids = sorted(df_responses["model_id_used"].dropna().unique()) if "model_id_used" in df_responses else []

    finish_reasons = Counter(df_api["finish_reason"].dropna()) if "finish_reason" in df_api else Counter()
    finish_top = finish_reasons.most_common(5)

    # M5 dropout estimate
    m5_responses = df_responses[df_responses["model"] == "M5"] if "model" in df_responses else pd.DataFrame()
    m5_expected = n_cells  # each cell should have 1 response per model
    m5_actual = len(m5_responses)
    m5_dropout = (1 - m5_actual / m5_expected) * 100 if m5_expected else 0

    parts = []
    parts.append(f"""# ACME-CrossLLM Dataset

**Archipelago Construct Mapping Experiment: Cross-Model LLM Diversity Data**

Version: {version}
License: CC-BY 4.0
DOI: [to be assigned via Zenodo upload]

## Overview

This dataset captures how five frontier large language models from different
labs (Anthropic Claude, OpenAI GPT, Google Gemini, DeepSeek, Moonshot Kimi)
respond to decision tasks and elicit bipolar evaluation constructs, in the
Personal Construct Psychology (Kelly's Repertory Grid) tradition adapted for
LLM agents.

Each "cell" represents one complete run of the pipeline (free responses ->
anonymization -> triadic construct elicitation -> ratings) on one (task,
condition) pair. Models work under two conditions: Neutral (analyst persona)
and Persona (one of five epistemological frames: Quantitative, Systems,
Engineering, Humanist, Contrarian; assigned via Latin square across tasks).

## Statistics

""")
    parts.append(_stat_row("Total cells", n_cells))
    parts.append(_stat_row("Total constructs elicited", n_constructs))
    parts.append(_stat_row("Total ratings", n_ratings))
    parts.append(_stat_row("Total free responses", n_responses))
    parts.append(_stat_row("Total API calls (audit trail)", n_api))
    parts.append(_stat_row("Total cost (USD)", round(total_cost, 2), "${}"))
    parts.append(_stat_row("Tasks", ", ".join(tasks)))
    parts.append(_stat_row("Models", ", ".join(models)))
    parts.append(_stat_row("Personas", ", ".join(personas)))
    parts.append(_stat_row("M5 (Moonshot Kimi) dropout rate",
                            round(m5_dropout, 1), "{}%"))
    parts.append("\nModel IDs used (snapshot at collection time):\n")
    for m in model_ids:
        parts.append(f"  - `{m}`\n")
    parts.append("\nFinish reason distribution (top 5):\n")
    for fr, cnt in finish_top:
        parts.append(f"  - **{fr}**: {cnt} calls\n")

    parts.append("""

## Files

| File | Description | Schema |
|---|---|---|
| `cells.parquet` | One row per cell, with metadata and summary metrics | cell_id, task, condition, run_idx, status, started_at, completed_at, random_seed, n_valid_responses, n_constructs, n_raters, mean_pairwise_disagreement, pca_pc1, pca_pc2, pca_pc3, pc1_plus_pc2, n_high_corr_pairs, cost_usd, tokens_in, tokens_out, n_errors |
| `constructs.parquet` | One row per elicited bipolar construct | construct_id, cell_id, task, condition, run_idx, model, persona, construct_order_in_model, left_pole, right_pole, triad, raw_output_excerpt, semantic_cluster |
| `ratings.parquet` | Long-format ratings (each rating is one row) | rating_id, cell_id, task, condition, run_idx, rater_model, rater_persona, construct_id, construct_origin_model, element_label, element_origin_model, rating (1-7) |
| `responses.parquet` | Free responses from each model on each cell | response_id, cell_id, task, condition, run_idx, model, model_id_used, used_fallback, persona, element_label, response_text, response_length_chars, tokens_prompt, tokens_completion, reasoning_tokens, latency_ms, cost_usd, finish_reason, timestamp_iso |
| `api_calls.parquet` | Full audit trail of every API call | call_id, cell_id, task, condition, run_idx, phase, model_short_name, model_id_used, used_fallback, persona_or_neutral, attempts, timestamp_iso, latency_ms, prompt_tokens, completion_tokens, reasoning_tokens, finish_reason, cost_usd, audit_file |

## Data collection methodology

See `PROTOCOL.md` for the pre-registered protocol (locked before data collection).

Each cell follows this pipeline:

1. **Free response (Phase 1)**: 5 models each receive the task brief plus a
   condition-appropriate system prompt; generate 200-400 word recommendation.
2. **Anonymization (Phase 2)**: responses are shuffled, labeled E1..E5; short
   summaries are computed programmatically (first 3 sentences).
3. **Triadic construct elicitation (Phase 3)**: each model is assigned 3
   triads. For each, identifies a bipolar construct that distinguishes two
   responses from the third.
4. **Ratings (Phase 4)**: each model rates all 5 responses on all collected
   constructs (1-7 Likert).

All API calls are logged to `logs/api_calls/<cell_id>/...json` with full
prompts, raw responses, usage, latency, finish reason.

## Limitations and biases

- **M5 dropout**: Moonshot Kimi (a thinking model) routinely hits output token
  limits due to extensive internal reasoning. Approximately {m5_dropout}% of
  M5 calls return empty content even after retries. This means many cells
  have 4 active models instead of 5. Models are not interchangeable for the
  same prompt - this is a known limitation when using thinking models in
  output-constrained settings.
- **English only**: all tasks and responses are in English.
- **Frontier-only**: models tested are 2026 frontier; smaller/older models
  may exhibit different patterns.
- **5-option tasks**: all tasks present exactly 5 options. PCA dimensionality
  is constrained by this.
- **Model versioning**: OpenRouter slugs can change over time. The exact
  model_id used at collection time is preserved in `responses.parquet`,
  `api_calls.parquet`, and `results/run_manifest.json`.
- **Task pool size**: 7 tasks across 3 domains is modest. Generalization
  beyond these tasks is unverified.

## Intended use

- Studying LLM behavioral diversity and convergence
- Benchmarking ensemble/mixture-of-agents methods
- Cross-model alignment research
- Evaluating Repertory Grid as an LLM evaluation method
- Comparing Western vs Chinese-trained frontier models

## NOT intended for

- Training models (this is behavioral evaluation data, not training data)
- Drawing strong claims without acknowledging the limitations above
- Diagnosing real-world cases mentioned in tasks (Task G medical triage
  is a hypothetical for evaluation, not a treatment protocol)

## Ethical considerations

- All data is generated by commercial LLM APIs; no human subjects.
- Task G (medical triage under scarcity) is sensitive content. Discussion of
  triage protocols was conducted as a structured decision exercise. Outputs
  should not be interpreted as endorsement of any specific protocol.
- Task E (AI safety governance) is politically sensitive; outputs reflect
  model behavior, not authoritative policy positions.
- Models may exhibit biases inherited from training data. The dataset
  preserves these for study, not for amplification.

## Citation

```
@dataset{{dolgov2026acme,
  title = {{ACME-CrossLLM: Cross-Model LLM Construct Elicitation Dataset}},
  author = {{Dolgov, Sergey}},
  note = {{Technical implementation by Claude assistant}},
  year = {{2026}},
  publisher = {{Zenodo}},
  version = {{{version}}},
  doi = {{[to be assigned]}},
  url = {{https://zenodo.org/...}}
}}
```

## Contact

Sergey Dolgov - https://archplg.co.uk
""".replace("{m5_dropout}", str(round(m5_dropout, 1))))

    return "".join(parts)


def build_citation_cff(version: str) -> str:
    return f"""cff-version: 1.2.0
message: "If you use this dataset, please cite it as below."
title: "ACME-CrossLLM: Cross-Model LLM Construct Elicitation Dataset"
authors:
  - family-names: "Dolgov"
    given-names: "Sergey"
    affiliation: "Archipelago"
    website: "https://archplg.co.uk"
date-released: "{datetime.now().strftime('%Y-%m-%d')}"
version: "{version}"
license: "CC-BY-4.0"
type: dataset
keywords:
  - "large language models"
  - "evaluation"
  - "Repertory Grid"
  - "Personal Construct Psychology"
  - "cross-model diversity"
  - "epistemic framing"
  - "LLM benchmarks"
notes: |
  Technical implementation by Claude assistant.
  Pre-registered protocol available in PROTOCOL.md within the data archive.
"""


def build_croissant_metadata(df_cells, df_constructs, df_ratings, df_responses, df_api,
                              version: str) -> dict:
    """Minimal Croissant-style JSON-LD metadata for ML dataset standards."""
    return {
        "@context": "https://schema.org/",
        "@type": "Dataset",
        "name": "ACME-CrossLLM",
        "alternateName": "Archipelago Construct Mapping Experiment - Cross-Model",
        "description": (
            "Cross-model LLM behavioral data: 5 frontier models from different labs "
            "(Anthropic, OpenAI, Google, DeepSeek, Moonshot) respond to 7 decision "
            "tasks under Neutral and Persona conditions. Elicits bipolar evaluation "
            "constructs via Repertory Grid pipeline."
        ),
        "url": "https://archplg.co.uk",
        "version": version,
        "license": "https://creativecommons.org/licenses/by/4.0/",
        "creator": [
            {
                "@type": "Person",
                "name": "Sergey Dolgov",
                "affiliation": "Archipelago",
            },
        ],
        "contributor": [
            {
                "@type": "Person",
                "name": "Claude assistant (technical implementation)",
                "affiliation": "Anthropic",
            },
        ],
        "datePublished": datetime.now().strftime("%Y-%m-%d"),
        "keywords": ["LLM", "evaluation", "Repertory Grid", "cross-model diversity"],
        "distribution": [
            {"@type": "DataDownload", "encodingFormat": "application/parquet",
             "name": "cells.parquet", "contentSize": f"{len(df_cells)} rows"},
            {"@type": "DataDownload", "encodingFormat": "application/parquet",
             "name": "constructs.parquet", "contentSize": f"{len(df_constructs)} rows"},
            {"@type": "DataDownload", "encodingFormat": "application/parquet",
             "name": "ratings.parquet", "contentSize": f"{len(df_ratings)} rows"},
            {"@type": "DataDownload", "encodingFormat": "application/parquet",
             "name": "responses.parquet", "contentSize": f"{len(df_responses)} rows"},
            {"@type": "DataDownload", "encodingFormat": "application/parquet",
             "name": "api_calls.parquet", "contentSize": f"{len(df_api)} rows"},
        ],
    }


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ============================================================
# Main
# ============================================================
def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--version", default="v1.0",
                   help="Dataset version (default: v1.0)")
    p.add_argument("--out", default=str(OUT_DIR),
                   help=f"Output directory (default: {OUT_DIR})")
    args = p.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Loading data...")
    cells = load_cells()
    summaries = load_summaries()
    cluster_data = load_construct_clusters()
    print(f"  Cells loaded: {len(cells)}")
    print(f"  Summaries loaded: {len(summaries)}")
    print(f"  Cluster data loaded: {bool(cluster_data)}")

    if not cells:
        print("ERROR: no cells found in results/. Run experiment first.")
        return 1

    print("\nBuilding tables...")
    df_cells = build_cells_table(cells, summaries)
    print(f"  cells: {len(df_cells)} rows")
    df_constructs = build_constructs_table(cells, cluster_data)
    print(f"  constructs: {len(df_constructs)} rows")
    df_ratings = build_ratings_table(cells)
    print(f"  ratings: {len(df_ratings)} rows")
    df_responses = build_responses_table(cells)
    print(f"  responses: {len(df_responses)} rows")
    df_api = build_api_calls_table(cells)
    print(f"  api_calls: {len(df_api)} rows")

    print("\nSaving Parquet tables...")
    df_cells.to_parquet(out_dir / "cells.parquet", index=False)
    df_constructs.to_parquet(out_dir / "constructs.parquet", index=False)
    df_ratings.to_parquet(out_dir / "ratings.parquet", index=False)
    df_responses.to_parquet(out_dir / "responses.parquet", index=False)
    df_api.to_parquet(out_dir / "api_calls.parquet", index=False)

    print("\nGenerating dataset card, license, citation...")
    card = build_dataset_card(df_cells, df_constructs, df_ratings, df_responses, df_api,
                                args.version)
    (out_dir / "dataset_card.md").write_text(card, encoding="utf-8")

    cff = build_citation_cff(args.version)
    (out_dir / "CITATION.cff").write_text(cff, encoding="utf-8")

    (out_dir / "LICENSE").write_text(
        LICENSE_CC_BY_40.replace("{version}", args.version), encoding="utf-8")

    metadata = build_croissant_metadata(df_cells, df_constructs, df_ratings, df_responses, df_api,
                                          args.version)
    with open(out_dir / "metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    # Copy PROTOCOL.md if it exists - critical for pre-registration claim
    proto = Path("PROTOCOL.md")
    if proto.exists():
        (out_dir / "PROTOCOL.md").write_text(proto.read_text(encoding="utf-8"),
                                              encoding="utf-8")

    # SHA-256 of each output file for integrity
    print("\nComputing SHA-256 checksums...")
    checksums = {}
    for f in sorted(out_dir.iterdir()):
        if f.is_file() and f.suffix in {".parquet", ".md", ".cff", ".json"}:
            checksums[f.name] = file_sha256(f)
    with open(out_dir / "SHA256SUMS.txt", "w", encoding="utf-8") as f:
        for name, h in sorted(checksums.items()):
            f.write(f"{h}  {name}\n")

    print(f"\nDataset {args.version} ready in: {out_dir}")
    print("\nFiles produced:")
    for f in sorted(out_dir.iterdir()):
        size_kb = f.stat().st_size / 1024
        print(f"  {f.name:30}  {size_kb:>10.1f} KB")

    print("\nNext steps:")
    print("  1. Review dataset_card.md (especially the limitations section)")
    print("  2. Upload dataset_release/ to Zenodo for DOI:")
    print("     https://zenodo.org/uploads/new")
    print("  3. Upload to HuggingFace Hub:")
    print("     huggingface-cli upload <username>/acme-crossllm dataset_release/")
    print("  4. Cite the DOI in your paper(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
