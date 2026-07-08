"""
Phase 2L · Triage: audit current state of results_phase2l/.

Shows for each phase × task × condition:
  - cells_present (file exists)
  - cells_valid (file >= 100 bytes, valid JSON)
  - cells_good (phase-specific quality: response non-empty for P1, constructs>=5 for P3, etc.)
  - cells_to_redo (present but garbage - should be deleted before resume)

Cost: $0.
Usage: python triage_phase2l.py
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

RESULTS_DIR = Path("./results_phase2l")
MIN_GOOD_CONSTRUCTS = 5  # below this, treat as parse failure
MIN_RESPONSE_LEN = 50    # below this, treat as truncated/empty


def audit_phase1(p: Path) -> str:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        resp = d.get("response") or ""
        if not resp or len(resp) < MIN_RESPONSE_LEN:
            return "BAD_EMPTY"
        if d.get("cost_usd", 0) == 0 and not resp:
            return "BAD_ZERO"
        return "GOOD"
    except (json.JSONDecodeError, OSError):
        return "BAD_PARSE"


def audit_phase2(p: Path) -> str:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        return "GOOD" if d.get("anonymized_text") else "BAD_EMPTY"
    except (json.JSONDecodeError, OSError):
        return "BAD_PARSE"


def audit_phase3(p: Path) -> str:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        n = d.get("n_constructs", 0)
        if n == 0:
            # Check if raw_response exists - parser failure, recoverable
            if d.get("raw_response"):
                return "BAD_PARSE_FAIL"
            return "BAD_EMPTY"
        if n < MIN_GOOD_CONSTRUCTS:
            return "BAD_FEW"
        return "GOOD"
    except (json.JSONDecodeError, OSError):
        return "BAD_PARSE"


def audit_phase4(p: Path) -> str:
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        ok = d.get("ok_batches", 0)
        n = d.get("n_batches", 0)
        if n == 0:
            return "BAD_EMPTY"
        if ok == 0:
            return "BAD_ALL_FAIL"
        if ok < n:
            return f"PARTIAL_{ok}/{n}"
        return "GOOD"
    except (json.JSONDecodeError, OSError):
        return "BAD_PARSE"


PHASES = {
    "phase1_free_response": audit_phase1,
    "phase2_anonymized": audit_phase2,
    "phase3_constructs": audit_phase3,
    "phase4_ratings": audit_phase4,
}


def main() -> int:
    if not RESULTS_DIR.exists():
        print(f"ERROR: {RESULTS_DIR} not found.")
        return 2

    print(f"Phase 2L Triage Report")
    print(f"Scanning: {RESULTS_DIR}")
    print("=" * 100)

    per_phase = {}
    for phase_dir, auditor in PHASES.items():
        d = RESULTS_DIR / phase_dir
        if not d.exists():
            per_phase[phase_dir] = {"GOOD": 0, "MISSING": 0}
            continue
        counts = defaultdict(int)
        bad_cells = []
        for cell in d.rglob("*.json"):
            if "_backups" in cell.parts:
                continue
            status = auditor(cell)
            counts[status] += 1
            if status != "GOOD" and not status.startswith("PARTIAL"):
                bad_cells.append((cell, status))
        per_phase[phase_dir] = {"counts": dict(counts), "bad": bad_cells}

    # Print summary
    for phase_dir in PHASES:
        d = per_phase[phase_dir]
        print(f"\n{phase_dir}:")
        if "counts" not in d:
            print(f"  (directory missing)")
            continue
        total = sum(d["counts"].values())
        for status, n in sorted(d["counts"].items(), key=lambda kv: -kv[1]):
            pct = 100 * n / total if total else 0
            marker = "OK" if status == "GOOD" else "BAD"
            print(f"  [{marker}] {status:<20} {n:>4}  ({pct:.0f}%)")
        print(f"  Total: {total} cells")

    # Coverage by task × condition for phase1 (the foundation)
    print(f"\n{'='*100}")
    print(f"Phase 1 coverage by task × condition (need 36/36 for full data)")
    print(f"{'='*100}")
    p1_dir = RESULTS_DIR / "phase1_free_response"
    if p1_dir.exists():
        task_cond_counts = defaultdict(lambda: defaultdict(int))
        task_cond_good = defaultdict(lambda: defaultdict(int))
        for task_dir in sorted(p1_dir.iterdir()):
            if not task_dir.is_dir():
                continue
            for cond_dir in sorted(task_dir.iterdir()):
                if not cond_dir.is_dir():
                    continue
                for cell in cond_dir.glob("*.json"):
                    status = audit_phase1(cell)
                    task_cond_counts[task_dir.name][cond_dir.name] += 1
                    if status == "GOOD":
                        task_cond_good[task_dir.name][cond_dir.name] += 1
        print(f"  {'Task':<8} {'N (good/total)':<18} {'P (good/total)':<18} Complete?")
        for task in sorted(task_cond_counts.keys()):
            n_total = task_cond_counts[task].get("N", 0)
            n_good = task_cond_good[task].get("N", 0)
            p_total = task_cond_counts[task].get("P", 0)
            p_good = task_cond_good[task].get("P", 0)
            complete = "YES" if n_good == 36 and p_good == 36 else "NO"
            print(f"  {task:<8} {n_good}/{n_total:<16} {p_good}/{p_total:<16} {complete}")

    # Cost so far
    state_path = RESULTS_DIR / "state.json"
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        print(f"\nstate.json says:")
        print(f"  total_cost_usd: ${state.get('total_cost_usd', 0):.4f}")
        print(f"  calls_total:    {state.get('calls_total', 0)}")
        print(f"  errors_count:   {state.get('errors_count', 0)}")

    # Recommend cleanup
    p3_bad = [(c, s) for c, s in per_phase.get("phase3_constructs", {}).get("bad", [])]
    p4_bad = [(c, s) for c, s in per_phase.get("phase4_ratings", {}).get("bad", [])]
    if p3_bad or p4_bad:
        print(f"\n{'='*100}")
        print(f"RECOMMENDED CLEANUP (run delete commands to redo with patched runner):")
        print(f"{'='*100}")
        print(f"  Phase 3 bad cells to redo: {len(p3_bad)}")
        print(f"  Phase 4 bad cells to redo: {len(p4_bad)}")
        print(f"\nDeletion script saved to: cleanup_bad_cells.ps1")
        with open("cleanup_bad_cells.ps1", "w", encoding="utf-8") as f:
            f.write("# Delete bad Phase 3/4 cells so resume re-fetches them with patched runner\n")
            f.write("# Run: powershell -ExecutionPolicy Bypass -File cleanup_bad_cells.ps1\n\n")
            for c, s in p3_bad + p4_bad:
                f.write(f'Remove-Item "{c}" -ErrorAction SilentlyContinue   # {s}\n')
        print(f"Total cells to delete: {len(p3_bad) + len(p4_bad)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
