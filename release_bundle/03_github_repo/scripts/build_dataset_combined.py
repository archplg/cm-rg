#!/usr/bin/env python3
"""
build_dataset_combined.py - производство HF-готового parquet dataset
из всех 5 фаз CM-RG (pilot, extended, phase2h, phase2h_extended, phase2j).

Производит файлы в hf_dataset/:
  data/cells.parquet       98 rows
  data/responses.parquet   ~900 rows
  data/constructs.parquet  ~1,861 rows
  data/ratings.parquet     ~110,882 rows (LONG format)
  data/api_calls.parquet   ~3,500 rows (audit trail)
  README.md                HF-compatible card (copy of DATASET_CARD.md)
  LICENSE                  CC-BY 4.0
  CITATION.cff             citation file

Запуск:
  pip install pyarrow pandas  # уже стоят
  python build_dataset_combined.py [--out hf_dataset]

После: можно сделать
  cd hf_dataset && huggingface-cli upload archipelago-research/cm-rg-v2 .
"""
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

import pandas as pd

PHASES = {
    "pilot":             Path("results_pilot"),
    "extended":          Path("results_extended"),
    "phase2h":           Path("results_phase2h"),
    "phase2h_extended":  Path("results_phase2h_extended"),
    "phase2j":           Path("results_phase2j"),
    "phase2k":           Path("results_phase2k"),       # paired-design replication
}


def collect_cells():
    cells_rows = []
    responses_rows = []
    constructs_rows = []
    ratings_rows = []
    api_rows = []
    rating_id = 0
    api_id = 0

    for phase_name, path in PHASES.items():
        if not path.exists():
            print(f"WARN: {path} not found - skipping")
            continue
        for cell_dir in sorted(path.iterdir()):
            if not cell_dir.is_dir(): continue
            cj = cell_dir / "cell.json"
            if not cj.exists(): continue
            try:
                data = json.loads(cj.read_text(encoding='utf-8'))
            except Exception as e:
                print(f"WARN: skip {cell_dir.name}: {e}")
                continue

            cell_id = data.get('cell_id', cell_dir.name)
            task = data.get('task', '?')
            condition = data.get('condition', '?')
            run_idx = data.get('run_idx', 0)
            status = data.get('status', '?')

            # cells row
            cells_rows.append({
                'phase': phase_name,
                'cell_id': cell_id,
                'task_id': task,
                'condition_id': condition,
                'run_id': run_idx,
                'status': status,
                'started_at': data.get('started_at'),
                'completed_at': data.get('completed_at'),
                'random_seed': data.get('random_seed'),
                'n_models': len(data.get('free_responses', {})),
                'n_constructs': sum(len(v) for v in data.get('constructs', {}).values()),
                'cost_usd_script_reported': data.get('cost_usd', 0),
            })

            # element_mapping: anonymized element -> model_id
            element_to_model = data.get('element_mapping', {})

            # responses
            for model_id, content in data.get('free_responses', {}).items():
                if isinstance(content, dict):
                    text = content.get('content', '')
                else:
                    text = str(content)
                responses_rows.append({
                    'phase': phase_name,
                    'cell_id': cell_id,
                    'task_id': task,
                    'condition_id': condition,
                    'run_id': run_idx,
                    'model_id': model_id,
                    'response_text': text[:5000],  # cap to 5K chars for parquet size
                    'response_length_chars': len(text),
                })

            # constructs
            for owner_model, items in data.get('constructs', {}).items():
                for item in items:
                    cid = item.get('id')
                    left = item.get('left', '').strip()
                    right = item.get('right', '').strip()
                    if not (cid and left and right): continue
                    constructs_rows.append({
                        'phase': phase_name,
                        'cell_id': cell_id,
                        'task_id': task,
                        'condition_id': condition,
                        'run_id': run_idx,
                        'construct_id': cid,
                        'owner_model_id': owner_model,
                        'left_pole': left,
                        'right_pole': right,
                        'triad_elements': item.get('triad', []),
                    })

            # ratings (LONG format - one row per (rater, construct, element))
            for rater_model, rater_constructs in data.get('ratings', {}).items():
                for c_id, ele_map in rater_constructs.items():
                    if not isinstance(ele_map, dict): continue
                    for element_id, rating in ele_map.items():
                        if not isinstance(rating, (int, float)): continue
                        if not (1 <= rating <= 7): continue
                        rating_id += 1
                        ratings_rows.append({
                            'rating_id': f"R{rating_id:07d}",
                            'phase': phase_name,
                            'cell_id': cell_id,
                            'task_id': task,
                            'condition_id': condition,
                            'run_id': run_idx,
                            'construct_id': c_id,
                            'element_id': element_id,
                            'rated_model_id': element_to_model.get(element_id, ''),
                            'rater_model_id': rater_model,
                            'rating': float(rating),
                        })

            # api_calls
            for c in data.get('api_calls', []):
                api_id += 1
                api_rows.append({
                    'call_id': f"C{api_id:07d}",
                    'phase': phase_name,
                    'cell_id': cell_id,
                    'phase_step': c.get('phase', ''),
                    'model_short_name': c.get('model_short_name', ''),
                    'model_id_used': c.get('model_id_used', ''),
                    'used_fallback': c.get('used_fallback', False),
                    'attempts': c.get('attempts', 1),
                    'latency_ms': c.get('latency_ms', 0),
                    'prompt_tokens': c.get('prompt_tokens', 0),
                    'completion_tokens': c.get('completion_tokens', 0),
                    'reasoning_tokens': c.get('reasoning_tokens', 0),
                    'finish_reason': c.get('finish_reason', ''),
                    'cost_usd_recorded': c.get('cost_usd', 0),
                    'timestamp_iso': c.get('timestamp_iso', ''),
                })

    return cells_rows, responses_rows, constructs_rows, ratings_rows, api_rows


def write_parquet(rows, path, sort_by=None):
    if not rows:
        print(f"  WARN: no rows for {path}")
        return
    df = pd.DataFrame(rows)
    if sort_by:
        df = df.sort_values(by=sort_by)
    df.to_parquet(path, engine='pyarrow', compression='snappy', index=False)
    print(f"  Wrote {path}: {len(df):,} rows, {path.stat().st_size:,} bytes")


def write_license(out_dir: Path):
    text = """Creative Commons Attribution 4.0 International (CC BY 4.0)

You are free to:
  Share - copy and redistribute the material in any medium or format
  Adapt - remix, transform, and build upon the material for any purpose,
          even commercially.

Under the following terms:
  Attribution - You must give appropriate credit, provide a link to the
                license, and indicate if changes were made.

Full text: https://creativecommons.org/licenses/by/4.0/legalcode
"""
    (out_dir / "LICENSE").write_text(text, encoding='utf-8')


def write_citation(out_dir: Path):
    text = """cff-version: 1.2.0
message: "If you use this dataset, please cite it as below."
authors:
  - family-names: Dolgov
    given-names: Sergey
    affiliation: Archipelago Research
    email: sergey@archplg.co.uk
title: "Cross-Model Repertory Grid: A Dataset of LLM-as-LLM Evaluative Ratings"
version: "1.0"
date-released: 2026-05-29
doi: "10.5281/zenodo.PENDING"
license: CC-BY-4.0
repository-code: "https://github.com/archipelago-research/cm-rg"
url: "https://crossmodelrg.org"
keywords:
  - large-language-models
  - llm-evaluation
  - cross-model-evaluation
  - repertory-grid
  - kelly-personal-constructs
  - calibration-drift
  - evaluative-diversity
"""
    (out_dir / "CITATION.cff").write_text(text, encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="hf_dataset", help="Output directory")
    args = ap.parse_args()

    out_dir = Path(args.out)
    data_dir = out_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/5] Collecting cells across {len(PHASES)} phases ...")
    cells, responses, constructs, ratings, api_calls = collect_cells()
    print(f"  Cells: {len(cells)}, responses: {len(responses)}, constructs: {len(constructs)}")
    print(f"  Ratings: {len(ratings):,}, api_calls: {len(api_calls):,}")

    print(f"\n[2/5] Writing parquet tables ...")
    write_parquet(cells,      data_dir / "cells.parquet",      sort_by=['phase', 'cell_id'])
    write_parquet(responses,  data_dir / "responses.parquet",  sort_by=['phase', 'cell_id', 'model_id'])
    write_parquet(constructs, data_dir / "constructs.parquet", sort_by=['phase', 'cell_id', 'construct_id'])
    write_parquet(ratings,    data_dir / "ratings.parquet",    sort_by=['rating_id'])
    write_parquet(api_calls,  data_dir / "api_calls.parquet",  sort_by=['call_id'])

    print(f"\n[3/5] Writing license + citation ...")
    write_license(out_dir)
    write_citation(out_dir)

    print(f"\n[4/5] Copying DATASET_CARD.md as README.md ...")
    src = Path("DATASET_CARD.md")
    if src.exists():
        (out_dir / "README.md").write_text(src.read_text(encoding='utf-8'), encoding='utf-8')
        print(f"  Copied {src} -> {out_dir / 'README.md'}")
    else:
        print(f"  WARN: {src} not found - HF expects README.md with YAML frontmatter")

    print(f"\n[5/5] Summary statistics ...")
    summary = {
        "n_cells": len(cells),
        "n_responses": len(responses),
        "n_constructs": len(constructs),
        "n_ratings": len(ratings),
        "n_api_calls": len(api_calls),
        "phases": list(PHASES.keys()),
        "build_date": datetime.now().isoformat(),
        "build_script": "build_dataset_combined.py",
        "license": "CC-BY-4.0",
    }
    (out_dir / "metadata.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"  metadata.json -> {out_dir / 'metadata.json'}")

    print(f"\nDone. Dataset built at: {out_dir.absolute()}")
    print(f"Next steps:")
    print(f"  1. cd {out_dir}")
    print(f"  2. huggingface-cli login")
    print(f"  3. huggingface-cli upload archipelago-research/cm-rg-v2 . -