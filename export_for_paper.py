#!/usr/bin/env python3
"""
Archipelago-for-Agents cross-model - export-for-paper.

Reads all artifacts from results/ and logs/, produces paper-ready outputs:
- LaTeX tables (per-cell summary, hypothesis evaluation, model comparison)
- Reproducibility appendix as Markdown (model IDs, seeds, prompts, configs)
- Per-call CSV (latency, cost, tokens, fallbacks)
- Construct catalogue (all elicited constructs with provenance)
- Free-response catalogue (anonymized)
- Supplementary materials tarball (everything needed for a reviewer to reproduce)

Run:
    python export_for_paper.py
"""
from __future__ import annotations
import argparse
import csv
import json
import shutil
import tarfile
from pathlib import Path

RESULTS_DIR = Path("./results")
LOGS_DIR = Path("./logs")
ANALYSIS_DIR = Path("./analysis")
PAPER_DIR = Path("./paper_outputs")


def latex_escape(s: str) -> str:
    if not isinstance(s, str):
        return str(s)
    rep = {"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$",
           "#": r"\#", "_": r"\_", "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}",
           "^": r"\textasciicircum{}"}
    out = []
    for ch in s:
        out.append(rep.get(ch, ch))
    return "".join(out)


def load_cells() -> dict[str, dict]:
    cells = {}
    for cd in sorted(RESULTS_DIR.iterdir()):
        if cd.is_dir() and (cd / "cell.json").exists():
            with open(cd / "cell.json", "r", encoding="utf-8") as f:
                cells[cd.name] = json.load(f)
    return cells


def load_manifest() -> dict:
    f = RESULTS_DIR / "run_manifest.json"
    if not f.exists():
        return {}
    with open(f, "r", encoding="utf-8") as fh:
        return json.load(fh)


def load_analysis_summaries() -> list:
    f = ANALYSIS_DIR / "all_summaries.json"
    if not f.exists():
        return []
    with open(f, "r", encoding="utf-8") as fh:
        return json.load(fh).get("summaries", [])


# ============================================================
# LaTeX table generators
# ============================================================
def write_table_per_cell(summaries: list, out_path: Path) -> None:
    """Per-cell summary table for paper."""
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Per-cell metrics for the cross-model experiment. "
        r"Disagreement is mean absolute difference in ratings across all "
        r"pairs of agents on a 1--7 Likert scale.}",
        r"\label{tab:per_cell}",
        r"\small",
        r"\begin{tabular}{lcccccc}",
        r"\toprule",
        r"Cell & Task & Cond & Run & Disagreement & PC1+PC2 & HighCorr \\",
        r"\midrule",
    ]
    for s in summaries:
        lines.append(
            f"{latex_escape(s['cell_id'])} & "
            f"{s['task']} & {s['condition']} & {s['run_idx']} & "
            f"{s['mean_pairwise_disagreement']:.3f} & "
            f"{s['pca_pc1_plus_pc2']:.3f} & "
            f"{s['n_high_corr_pairs']} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_table_hypothesis(summaries: list, out_path: Path) -> None:
    """Hypothesis evaluation table contrasting pilot vs cross-model."""
    PILOT_REF = {"A": 0.31, "B": 0.14}
    cells_by_task = {}
    for s in summaries:
        cells_by_task.setdefault(s["task"], []).append(s)
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Pre-registered hypothesis test. Pilot disagreement values "
        r"are from the single-model role-played experiment. Predicted range "
        r"for cross-model was 0.6--1.5 (above pilot, below noise floor).}",
        r"\label{tab:hypothesis}",
        r"\small",
        r"\begin{tabular}{lcccc}",
        r"\toprule",
        r"Task & Pilot & Cross-model & Delta & Status \\",
        r"\midrule",
    ]
    for task in sorted(cells_by_task.keys()):
        cells = cells_by_task[task]
        cross = sum(c["mean_pairwise_disagreement"] for c in cells) / len(cells)
        pilot = PILOT_REF.get(task, "n/a")
        if isinstance(pilot, (int, float)):
            delta = cross - pilot
            status = ("Supported" if 0.6 <= cross <= 1.5 else
                      "Below predicted" if cross < 0.6 else
                      "Above predicted")
            lines.append(
                f"{task} & {pilot:.3f} & {cross:.3f} & {delta:+.3f} & {status} \\\\"
            )
        else:
            lines.append(f"{task} & --- & {cross:.3f} & --- & --- \\\\")
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_table_models(manifest: dict, cells: dict, out_path: Path) -> None:
    """Per-model breakdown table for the paper."""
    if not manifest:
        return
    lines = [
        r"\begin{table}[t]",
        r"\centering",
        r"\caption{Model identifiers, pricing at run time, total tokens "
        r"used across all cells, total cost.}",
        r"\label{tab:models}",
        r"\small",
        r"\begin{tabular}{llrrrr}",
        r"\toprule",
        r"Family & Model ID & In/M USD & Out/M USD & Tokens & Cost USD \\",
        r"\midrule",
    ]
    per_model_total = {}
    for cell in cells.values():
        for sn, cost in cell.get("per_model_cost", {}).items():
            d = per_model_total.setdefault(sn, {"cost": 0.0, "in": 0, "out": 0})
            d["cost"] += cost
            t = cell.get("per_model_tokens", {}).get(sn, {})
            d["in"] += t.get("prompt", 0)
            d["out"] += t.get("completion", 0)
    for m in manifest.get("models_snapshot", []):
        sn = m["short_name"]
        pricing = m.get("primary_pricing", {})
        p_in = float(pricing.get("prompt", "0") or "0") * 1e6
        p_out = float(pricing.get("completion", "0") or "0") * 1e6
        d = per_model_total.get(sn, {"cost": 0, "in": 0, "out": 0})
        lines.append(
            f"{m['family']} & \\texttt{{{latex_escape(m['primary_id'])}}} & "
            f"{p_in:.2f} & {p_out:.2f} & "
            f"{d['in'] + d['out']:,} & {d['cost']:.2f} \\\\"
        )
    lines += [r"\bottomrule", r"\end{tabular}", r"\end{table}"]
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ============================================================
# Reproducibility appendix
# ============================================================
def write_reproducibility_appendix(manifest: dict, cells: dict, out_path: Path) -> None:
    lines = ["# Reproducibility Appendix\n"]
    lines.append("This appendix contains all information needed to reproduce the experiment.\n")

    lines.append("\n## Run manifest\n")
    if manifest:
        lines.append(f"- Started: `{manifest.get('started_at')}` ({manifest.get('timezone')})\n")
        lines.append(f"- Python: `{manifest.get('python_version')}`\n")
        lines.append(f"- Platform: `{manifest.get('platform')}`\n")
        lines.append(f"- Script SHA-256: `{manifest.get('script_sha256')}`\n")
        lines.append(f"- Config SHA-256: `{manifest.get('config_sha256')}`\n")
        lines.append(f"- Analyzer SHA-256: `{manifest.get('analyze_sha256')}`\n")
        lines.append("\n### Package versions\n")
        for k, v in (manifest.get("package_versions") or {}).items():
            lines.append(f"- `{k}` = `{v}`\n")

    lines.append("\n## Models used (snapshot at run start)\n")
    for m in manifest.get("models_snapshot", []):
        lines.append(f"\n### {m['short_name']} ({m['family']})\n")
        lines.append(f"- Primary ID: `{m['primary_id']}`\n")
        lines.append(f"- Fallback ID: `{m['fallback_id']}`\n")
        lines.append(f"- Context length: {m.get('primary_context_length')}\n")
        pr = m.get("primary_pricing", {})
        lines.append(f"- Pricing (USD/token): input=`{pr.get('prompt')}`, output=`{pr.get('completion')}`\n")

    lines.append("\n## Cells executed\n")
    for cid, c in sorted(cells.items()):
        lines.append(
            f"- `{cid}` (task {c['task']}, cond {c['condition']}, run {c['run_idx']}): "
            f"status `{c.get('status')}`, seed `{c.get('random_seed')}`, "
            f"started `{c.get('started_at')}`, completed `{c.get('completed_at')}`\n"
        )

    lines.append("\n## Random seeds\n")
    lines.append("Each cell uses a deterministic seed derived from its `cell_id` "
                 "(see `random_seed` field in `cell.json`). The same seed governs:\n")
    lines.append("- Element label permutation (anonymization step)\n")
    lines.append("- Triad assignment to agents\n")

    lines.append("\n## Full prompts\n")
    lines.append("Every API call's full system prompt and user prompt are stored in "
                 "`logs/api_calls/<cell_id>/<phase>_<model>_<attempt>.json`. These files "
                 "also contain the full raw API response and the request payload sent.\n")

    lines.append("\n## Configuration\n")
    if manifest.get("config_full_snapshot"):
        lines.append("Complete configuration used in this run:\n\n```yaml\n")
        import yaml
        lines.append(yaml.safe_dump(manifest["config_full_snapshot"], sort_keys=False, allow_unicode=True))
        lines.append("```\n")

    out_path.write_text("".join(lines), encoding="utf-8")


# ============================================================
# Per-call CSV (latency, cost, fallback patterns)
# ============================================================
def write_api_calls_csv(cells: dict, out_path: Path) -> None:
    fieldnames = [
        "cell_id", "task", "condition", "run_idx", "phase",
        "model_short_name", "persona_or_neutral", "model_id_used",
        "used_fallback", "attempts", "latency_ms",
        "timestamp_iso", "prompt_tokens", "completion_tokens", "cost_usd",
    ]
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for cell in cells.values():
            base = {
                "cell_id": cell["cell_id"],
                "task": cell["task"],
                "condition": cell["condition"],
                "run_idx": cell["run_idx"],
            }
            for call in cell.get("api_calls", []):
                row = {**base, **call}
                w.writerow(row)


# ============================================================
# Construct catalogue
# ============================================================
def write_constructs_catalogue(cells: dict, out_path: Path) -> None:
    fieldnames = ["cell_id", "task", "condition", "run_idx",
                  "owner_model", "owner_persona", "construct_id",
                  "left_pole", "right_pole", "triad"]
    rows = []
    for cell in cells.values():
        # Find persona per model in this cell
        # (re-derive from condition mapping if present)
        persona_map = {}
        for call in cell.get("api_calls", []):
            persona_map[call["model_short_name"]] = call["persona_or_neutral"]
        for owner, items in cell.get("constructs", {}).items():
            for c in items:
                rows.append({
                    "cell_id": cell["cell_id"],
                    "task": cell["task"],
                    "condition": cell["condition"],
                    "run_idx": cell["run_idx"],
                    "owner_model": owner,
                    "owner_persona": persona_map.get(owner, "?"),
                    "construct_id": c.get("id"),
                    "left_pole": c.get("left"),
                    "right_pole": c.get("right"),
                    "triad": ",".join(c.get("triad") or []),
                })
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


# ============================================================
# Free response catalogue
# ============================================================
def write_freeresponse_catalogue(cells: dict, out_path: Path) -> None:
    """Markdown with all 50 free responses, with model and persona but anonymized element labels."""
    lines = ["# Free response catalogue\n"]
    lines.append("All 50 model responses across the 10 cells, organized by cell.\n")
    for cid in sorted(cells.keys()):
        cell = cells[cid]
        lines.append(f"\n## Cell `{cid}` (task {cell['task']}, condition {cell['condition']}, run {cell['run_idx']})\n")
        persona_map = {}
        for call in cell.get("api_calls", []):
            if call["phase"] == "phase1_freeresponse":
                persona_map[call["model_short_name"]] = (
                    call["persona_or_neutral"], call["model_id_used"]
                )
        for sn in sorted(cell.get("free_responses", {}).keys()):
            persona, mid = persona_map.get(sn, ("?", "?"))
            text = cell["free_responses"][sn]
            lines.append(f"\n### {sn} ({mid}), persona={persona}\n")
            lines.append(f"\n{text}\n")
    out_path.write_text("".join(lines), encoding="utf-8")


# ============================================================
# Tarball
# ============================================================
def make_supplementary_tarball(out_path: Path) -> None:
    """Build supplementary_materials.tar.gz with everything needed."""
    with tarfile.open(out_path, "w:gz") as tar:
        for src in [Path("PROTOCOL.md"), Path("README.md"), Path("config.yaml"),
                    Path("run_experiment.py"), Path("analyze.py"),
                    Path("export_for_paper.py"), Path("requirements.txt"),
                    Path("tasks"), Path("personas")]:
            if src.exists():
                tar.add(src, arcname=f"supplementary/{src.name}")
        for src in [RESULTS_DIR, LOGS_DIR, ANALYSIS_DIR, PAPER_DIR]:
            if src.exists():
                tar.add(src, arcname=f"supplementary/{src.name}")


# ============================================================
# Main
# ============================================================
def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--skip-tarball", action="store_true")
    args = p.parse_args()

    PAPER_DIR.mkdir(exist_ok=True)
    cells = load_cells()
    manifest = load_manifest()
    summaries = load_analysis_summaries()

    if not cells:
        print(f"No cells found in {RESULTS_DIR}/")
        return 1

    print(f"Loaded {len(cells)} cells, {len(summaries)} summaries, manifest={'yes' if manifest else 'no'}")

    if summaries:
        write_table_per_cell(summaries, PAPER_DIR / "table_per_cell.tex")
        write_table_hypothesis(summaries, PAPER_DIR / "table_hypothesis.tex")
        print(f"Wrote {PAPER_DIR / 'table_per_cell.tex'}")
        print(f"Wrote {PAPER_DIR / 'table_hypothesis.tex'}")
    write_table_models(manifest, cells, PAPER_DIR / "table_models.tex")
    print(f"Wrote {PAPER_DIR / 'table_models.tex'}")
    write_reproducibility_appendix(manifest, cells, PAPER_DIR / "reproducibility_appendix.md")
    print(f"Wrote {PAPER_DIR / 'reproducibility_appendix.md'}")
    write_api_calls_csv(cells, PAPER_DIR / "all_api_calls.csv")
    print(f"Wrote {PAPER_DIR / 'all_api_calls.csv'}")
    write_constructs_catalogue(cells, PAPER_DIR / "all_constructs.csv")
    print(f"Wrote {PAPER_DIR / 'all_constructs.csv'}")
    write_freeresponse_catalogue(cells, PAPER_DIR / "all_free_responses.md")
    print(f"Wrote {PAPER_DIR / 'all_free_responses.md'}")

    # Also copy biplots from analysis/
    if ANALYSIS_DIR.exists():
        plots_dir = PAPER_DIR / "plots"
        plots_dir.mkdir(exist_ok=True)
        for cell_dir in ANALYSIS_DIR.iterdir():
            if cell_dir.is_dir():
                for plot in cell_dir.glob("*.png"):
                    shutil.copy(plot, plots_dir / f"{cell_dir.name}_{plot.name}")
        print(f"Copied PNGs to {plots_dir}")

    if not args.skip_tarball:
        tarball = Path("supplementary_materials.tar.gz")
        make_supplementary_tarball(tarball)
        print(f"\nWrote {tarball} - upload this as supplementary materials with the paper")

    print(f"\nDone. Files in {PAPER_DIR}/ are paper-ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
