#!/usr/bin/env python3
"""
Diagnose Phase 2F cell.json corruption.

Reproduces the EXACT write pattern from run_experiment.py without making
any API calls. Tests multiple hypotheses:

1. Is it consistent file-system corruption (any large JSON gets truncated)?
2. Does it happen only with Unicode content (em-dashes, smart quotes)?
3. Does it happen with atomic rename + fsync?
4. Does it happen with direct write?
5. Does it happen during concurrent file operations (mimicking script loop)?

Each test writes a real cell-like JSON and verifies the file was saved
correctly. Truncation is detected by:
- Final size != expected size
- JSON fails to parse after write

Run on user's Windows machine:
    python diagnose_write_corruption.py

Saves report to: diagnose_write_corruption_report.md
"""
from __future__ import annotations
import json
import os
import sys
import time
import platform
import shutil
from pathlib import Path


OUT_DIR = Path("diagnose_write_test")


def make_test_cell(cell_id: str, m1_length: int = 2400) -> dict:
    """Build a fake cell.json-like dict with realistic content."""
    # Realistic M1 response with em-dashes (common in LLM output)
    m1_filler = (
        "# Recommendation: Option B — Treatment-court diversion\n\n"
        "Option B is the right framework because it threads every constraint "
        "the legislature actually faces. A moderate governor can sign a bill "
        "framed as 'tough accountability with a path out': offenders are still "
        "arrested, charged, and supervised, but routed toward outcomes that "
        "empirically reduce reoffending by 25–45%. That framing survives "
        "the editorial-board test and the sheriff's-association test in a "
        "way decriminalization does not. " * 5
    )
    m1_filler = m1_filler[:m1_length]
    return {
        "cell_id": cell_id,
        "task": "TEST",
        "condition": "N",
        "run_idx": 1,
        "status": "complete_with_errors",
        "started_at": "2026-05-26T20:00:00.000000",
        "completed_at": "2026-05-26T20:15:00.000000",
        "random_seed": 1234567890,
        "free_responses": {
            "M1": m1_filler,
            "M2": m1_filler[:1800],
            "M3": m1_filler[:1900],
            "M4": m1_filler[:1700],
            "M5": m1_filler[:2000],
        },
        "element_mapping": {f"E{i+1}": f"M{i+1}" for i in range(5)},
        "constructs": {f"M{i+1}": [
            {"id": f"C_M{i+1}_{j+1}", "left": f"left pole {j}", "right": f"right pole {j}"}
            for j in range(3)
        ] for i in range(5)},
    }


def test_write_atomic_with_fsync(cell_id: str) -> dict:
    """Mimics run_experiment.py save_cell_artifacts exactly."""
    out_dir = OUT_DIR / cell_id
    out_dir.mkdir(parents=True, exist_ok=True)
    final = out_dir / "cell.json"
    tmp = out_dir / "cell.json.tmp"
    data = make_test_cell(cell_id)
    expected_bytes = len(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))

    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(final)

    actual_bytes = os.path.getsize(final)
    try:
        with open(final, encoding="utf-8") as f:
            json.load(f)
        parse_ok = True
        parse_err = None
    except Exception as e:
        parse_ok = False
        parse_err = str(e)[:120]

    return {
        "cell": cell_id, "expected_bytes": expected_bytes, "actual_bytes": actual_bytes,
        "ok": (actual_bytes == expected_bytes) and parse_ok,
        "parse_ok": parse_ok, "parse_err": parse_err,
    }


def test_write_direct(cell_id: str) -> dict:
    """Direct write without tmp+rename."""
    out_dir = OUT_DIR / cell_id
    out_dir.mkdir(parents=True, exist_ok=True)
    final = out_dir / "cell.json"
    data = make_test_cell(cell_id)
    expected_bytes = len(json.dumps(data, indent=2, ensure_ascii=False).encode("utf-8"))

    with open(final, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    actual_bytes = os.path.getsize(final)
    try:
        with open(final, encoding="utf-8") as f:
            json.load(f)
        parse_ok = True
        parse_err = None
    except Exception as e:
        parse_ok = False
        parse_err = str(e)[:120]

    return {
        "cell": cell_id, "expected_bytes": expected_bytes, "actual_bytes": actual_bytes,
        "ok": (actual_bytes == expected_bytes) and parse_ok,
        "parse_ok": parse_ok, "parse_err": parse_err,
    }


def main():
    # Clean previous test
    if OUT_DIR.exists():
        shutil.rmtree(OUT_DIR)
    OUT_DIR.mkdir()

    print(f"Diagnosing on: {platform.platform()}")
    print(f"Python: {sys.version}")
    print(f"CWD: {os.getcwd()}")
    print(f"Test dir: {OUT_DIR.resolve()}")
    print()

    # OneDrive check
    onedrive = os.environ.get("OneDrive", "")
    project = str(OUT_DIR.resolve())
    if onedrive and onedrive.lower() in project.lower():
        print(f"WARNING: test folder IS in OneDrive: {onedrive}")
    else:
        print(f"OK: test folder not in OneDrive (OneDrive at: {onedrive or '(not set)'})")
    print()

    # Test 1: Single atomic write
    print("=== TEST 1: Single atomic write ===")
    r = test_write_atomic_with_fsync("TEST_atomic_1")
    print(f"  Expected: {r['expected_bytes']}, Actual: {r['actual_bytes']}, OK: {r['ok']}")
    if not r['ok']:
        print(f"  Parse: {r['parse_ok']}, Error: {r['parse_err']}")
    test1 = r

    # Test 2: Direct write
    print("\n=== TEST 2: Direct write (no tmp+rename) ===")
    r = test_write_direct("TEST_direct_1")
    print(f"  Expected: {r['expected_bytes']}, Actual: {r['actual_bytes']}, OK: {r['ok']}")
    if not r['ok']:
        print(f"  Parse: {r['parse_ok']}, Error: {r['parse_err']}")
    test2 = r

    # Test 3: 30 cells in sequence (simulate Phase 2F loop)
    print("\n=== TEST 3: 30 sequential atomic writes (simulating Phase 2F loop) ===")
    test3_results = []
    for i in range(30):
        cell_id = f"TEST_seq_{i:02d}"
        r = test_write_atomic_with_fsync(cell_id)
        test3_results.append(r)
        if not r['ok']:
            print(f"  FAIL at cell {i}: {r['cell']} - {r['actual_bytes']}/{r['expected_bytes']} bytes")
        time.sleep(0.05)  # mimic API pacing
    failures3 = [r for r in test3_results if not r['ok']]
    print(f"  Total: 30, Failures: {len(failures3)}")
    if failures3:
        print(f"  Failed sizes: {[r['actual_bytes'] for r in failures3[:5]]}")

    # Test 4: Re-read after 5 seconds (does external process corrupt?)
    print("\n=== TEST 4: Re-read 30 files after 5-second delay ===")
    print("  Waiting 5 seconds for any background process to interfere...")
    time.sleep(5)
    test4_corrupted = []
    for r in test3_results:
        if not r['ok']:
            continue
        cell_id = r['cell']
        final = OUT_DIR / cell_id / "cell.json"
        try:
            actual_bytes = os.path.getsize(final)
            with open(final, encoding="utf-8") as f:
                json.load(f)
            if actual_bytes != r['expected_bytes']:
                test4_corrupted.append({
                    "cell": cell_id,
                    "was": r['expected_bytes'],
                    "now": actual_bytes,
                })
        except Exception as e:
            test4_corrupted.append({"cell": cell_id, "was": r['expected_bytes'], "now": "PARSE FAIL"})
    print(f"  Files corrupted after delay: {len(test4_corrupted)}")
    if test4_corrupted:
        for c in test4_corrupted[:5]:
            print(f"    {c['cell']}: was {c['was']}, now {c['now']}")

    # Test 5: Large file (simulate full cell with ratings)
    print("\n=== TEST 5: Large file write (50KB) ===")
    out = OUT_DIR / "TEST_large.json"
    big_data = {f"key_{i}": "long string " * 200 for i in range(50)}
    big_data["large_string"] = "x" * 30000
    expected = len(json.dumps(big_data, indent=2, ensure_ascii=False).encode("utf-8"))
    with open(out, "w", encoding="utf-8") as f:
        json.dump(big_data, f, indent=2, ensure_ascii=False)
        f.flush()
        os.fsync(f.fileno())
    actual = os.path.getsize(out)
    test5_ok = actual == expected
    print(f"  Expected: {expected}, Actual: {actual}, OK: {test5_ok}")

    # Summary
    print("\n=== SUMMARY ===")
    print(f"Test 1 (atomic single): {'PASS' if test1['ok'] else 'FAIL'}")
    print(f"Test 2 (direct single): {'PASS' if test2['ok'] else 'FAIL'}")
    print(f"Test 3 (30 atomic seq):  {'PASS' if len(failures3) == 0 else 'FAIL'} ({len(failures3)}/30 failed)")
    print(f"Test 4 (delayed re-read): {'PASS' if len(test4_corrupted) == 0 else 'FAIL'} ({len(test4_corrupted)} corrupted)")
    print(f"Test 5 (large file):     {'PASS' if test5_ok else 'FAIL'}")

    # Diagnose
    print("\n=== DIAGNOSIS ===")
    if test1['ok'] and test2['ok'] and len(failures3) == 0 and len(test4_corrupted) == 0:
        print("All tests passed. Corruption is NOT reproducible in isolation.")
        print("Possible causes: long-running script context, network-related interrupts,")
        print("intermittent system load, or interaction with running API client.")
    elif len(test4_corrupted) > 0:
        print("Files are corrupted AFTER write succeeds (delayed corruption).")
        print("This is consistent with OneDrive sync, antivirus, or backup software")
        print("modifying files post-write. Recommendation:")
        print("  - Move project OUT of any synced folder")
        print("  - Add Windows Defender exclusion for project folder")
        print("  - Disable backup software temporarily")
    elif len(failures3) > 0:
        print(f"Sequential writes fail. {len(failures3)}/30 corrupted at write time.")
        print("This is filesystem / OS-level. Recommendation:")
        print("  - Check disk space, disk health")
        print("  - Try writing to D:\\ or other drive")
        print("  - Check Windows Event Viewer for filesystem errors")

    # Write report
    report_path = Path("diagnose_write_corruption_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# Phase 2F write corruption diagnosis\n\n")
        f.write(f"- Platform: {platform.platform()}\n")
        f.write(f"- Python: {sys.version}\n")
        f.write(f"- Test dir: {OUT_DIR.resolve()}\n")
        f.write(f"- OneDrive env: {onedrive or 'not set'}\n\n")
        f.write(f"## Results\n\n")
        f.write(f"| Test | Result | Detail |\n|---|---|---|\n")
        f.write(f"| 1. Atomic single | {'PASS' if test1['ok'] else 'FAIL'} | {test1['actual_bytes']}/{test1['expected_bytes']} bytes |\n")
        f.write(f"| 2. Direct single | {'PASS' if test2['ok'] else 'FAIL'} | {test2['actual_bytes']}/{test2['expected_bytes']} bytes |\n")
        f.write(f"| 3. 30 sequential | {'PASS' if len(failures3) == 0 else 'FAIL'} | {len(failures3)}/30 failed |\n")
        f.write(f"| 4. Delayed re-read | {'PASS' if len(test4_corrupted) == 0 else 'FAIL'} | {len(test4_corrupted)} corrupted |\n")
        f.write(f"| 5. Large file | {'PASS' if test5_ok else 'FAIL'} | {actual}/{expected} bytes |\n")
        if failures3:
            f.write(f"\n## Test 3 failure sizes\n\n")
            for r in failures3[:10]:
                f.write(f"- {r['cell']}: {r['actual_bytes']} bytes (expected {r['expected_bytes']})\n")
        if test4_corrupted:
            f.write(f"\n## Test 4 delayed corruption\n\n")
            for c in test4_corrupted[:10]:
                f.write(f"- {c['cell']}: was {c['was']}, now {c['now']}\n")

    print(f"\nReport saved: {report_path.resolve()}")


if __name__ == "__main__":
    main()
