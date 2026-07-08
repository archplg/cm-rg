#!/usr/bin/env python3
"""
verify_phase2j.py - окончательная проверка Phase 2J.

Запускается один раз, печатает PASS/FAIL по 7 проверкам:
  1. M11 в audit-файлах реально вернул Opus 4.8 (не silent fallback)
  2. Реальная стоимость Phase 2J из usage.cost совпадает с моей оценкой
  3. По моделям с reasoning виден ожидаемый недосчёт (доказательство гипотезы)
  4. M11 ratings count корректен (проверка против H2)
  5. Cluster stability H1 устойчива (M1 ↔ M11 < 1.0)
  6. PCA робастна без проблемной M3 (52% покрытие)
  7. H2 не маскирует task-conditional эффект (per-task разбивка)

Зависимости: numpy, scikit-learn (уже стоят после Phase 2H).
Запуск: python verify_phase2j.py
"""
from __future__ import annotations
import json
import os
import sys
from pathlib import Path
from collections import defaultdict

import numpy as np

# ============================================================
# Constants
# ============================================================
PHASE2J_DIR = Path("results_phase2j")
AUDIT_DIR = Path("logs_phase2j/api_calls")

EXPECTED_OPUS_48_SLUG = "anthropic/claude-4.8-opus-20260528"
EXPECTED_PROVIDER = "Anthropic"

# Models with reasoning support (where we expect undercount in old script)
REASONING_MODELS = {"M3", "M4", "M5", "M9"}  # Gemini, DeepSeek, Kimi, Llama
NO_REASONING_MODELS = {"M1", "M2", "M6", "M7", "M8", "M10"}

# Colors for terminal (ANSI codes work on Windows 10+)
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"


def ok(msg):  return f"{GREEN}[PASS]{RESET} {msg}"
def fail(msg): return f"{RED}[FAIL]{RESET} {msg}"
def warn(msg): return f"{YELLOW}[WARN]{RESET} {msg}"
def hdr(msg): return f"\n{BOLD}=== {msg} ==={RESET}"


# ============================================================
# Helpers
# ============================================================
def load_audit_files():
    """Yield (cell_id, phase, model_short, audit_data) for each audit JSON."""
    if not AUDIT_DIR.exists():
        return
    for cell_dir in sorted(AUDIT_DIR.iterdir()):
        if not cell_dir.is_dir(): continue
        cell_id = cell_dir.name
        for audit_file in sorted(cell_dir.glob("*.json")):
            try:
                data = json.loads(audit_file.read_text(encoding='utf-8'))
            except Exception:
                continue
            stem = audit_file.stem
            parts = stem.split("_")
            phase = "_".join(parts[:-2])  # phase1_freeresponse etc
            ms = next((p for p in parts if p.startswith("M") and p[1:].isdigit()), "M?")
            yield cell_id, phase, ms, data


def load_cells():
    """Yield (cell_id, task, condition, cell_data) for each Phase 2J cell."""
    if not PHASE2J_DIR.exists():
        return
    for cell_dir in sorted(PHASE2J_DIR.iterdir()):
        if not cell_dir.is_dir(): continue
        cj = cell_dir / "cell.json"
        if not cj.exists(): continue
        try:
            data = json.loads(cj.read_text(encoding='utf-8'))
        except Exception:
            continue
        parts = cell_dir.name.split("_")
        task = parts[0]
        cond = parts[1]
        yield cell_dir.name, task, cond, data


# ============================================================
# Check 1: M11 really returned Opus 4.8
# ============================================================
def check_1_m11_is_real_opus48():
    print(hdr("Проверка 1. M11 реально вернул Opus 4.8 (не silent fallback)"))
    m11_audits = [(cid, ph, d) for cid, ph, ms, d in load_audit_files() if ms == "M11"]
    if not m11_audits:
        print(fail("Нет M11 audit-файлов. Проверьте, что logs_phase2j/api_calls/ существует."))
        return False
    bad = []
    sample_seen = set()
    for cid, ph, d in m11_audits:
        raw = d.get("raw_response_full", {}) or {}
        model = raw.get("model", "")
        provider = raw.get("provider", "")
        if EXPECTED_OPUS_48_SLUG not in model:
            bad.append((cid, ph, f"model={model!r}"))
        elif provider != EXPECTED_PROVIDER:
            bad.append((cid, ph, f"provider={provider!r}"))
        else:
            if cid not in sample_seen and len(sample_seen) < 3:
                sample_seen.add(cid)
                print(f"  {cid} / {ph}: model={model}, provider={provider}")
    if not bad:
        print(ok(f"Все {len(m11_audits)} M11 вызовов вернулись от {EXPECTED_OPUS_48_SLUG} через {EXPECTED_PROVIDER}."))
        return True
    print(fail(f"{len(bad)} M11 вызовов имеют неожиданный model/provider:"))
    for cid, ph, info in bad[:5]:
        print(f"  {cid} / {ph}: {info}")
    return False


# ============================================================
# Check 2: Real Phase 2J cost from usage.cost matches my estimate
# ============================================================
def check_2_real_cost():
    print(hdr("Проверка 2. Реальная стоимость Phase 2J из usage.cost"))
    cost_by_model = defaultdict(float)
    script_by_model = defaultdict(float)
    files_count = 0
    for cid, ph, ms, d in load_audit_files():
        files_count += 1
        usage = (d.get("raw_response_full") or {}).get("usage", {}) or d.get("usage", {})
        real = usage.get("cost")
        if real is None:
            cd = usage.get("cost_details") or {}
            real = cd.get("upstream_inference_cost", 0.0)
        try:
            cost_by_model[ms] += float(real or 0)
        except (TypeError, ValueError):
            pass
        try:
            script_by_model[ms] += float(d.get("cost_usd") or 0)
        except (TypeError, ValueError):
            pass
    real_total = sum(cost_by_model.values())
    script_total = sum(script_by_model.values())
    print(f"  Audit-файлов прошито: {files_count}")
    print(f"  Реальная стоимость (sum usage.cost):  ${real_total:.4f}")
    print(f"  Стоимость по старому скрипту:         ${script_total:.4f}")
    print(f"  Недосчёт:                              ${real_total - script_total:+.4f}")

    if abs(real_total - 15.32) < 0.5:
        print(ok(f"Реальная стоимость ${real_total:.2f} совпадает с моей оценкой $15.32 ± $0.50."))
        ret = True
    else:
        print(warn(f"Реальная стоимость ${real_total:.2f} отличается от моей оценки $15.32 (отличие > $0.50). Проверьте."))
        ret = False

    print(f"\n  Разбивка по моделям:")
    print(f"  {'Model':<6} {'Real':>10} {'Script':>10} {'Diff':>10}")
    for ms in sorted(cost_by_model.keys(), key=lambda x: int(x[1:]) if x[1:].isdigit() else 99):
        r = cost_by_model[ms]; s = script_by_model[ms]
        print(f"  {ms:<6} ${r:>9.4f} ${s:>9.4f} ${r-s:>+9.4f}")
    return ret


# ============================================================
# Check 3: Reasoning models show expected undercount
# ============================================================
def check_3_reasoning_undercount():
    print(hdr("Проверка 3. Reasoning tokens действительно не учитывались скриптом"))
    cost_by_model = defaultdict(float)
    script_by_model = defaultdict(float)
    for cid, ph, ms, d in load_audit_files():
        usage = (d.get("raw_response_full") or {}).get("usage", {}) or d.get("usage", {})
        real = usage.get("cost")
        if real is None:
            real = (usage.get("cost_details") or {}).get("upstream_inference_cost", 0.0)
        try:
            cost_by_model[ms] += float(real or 0)
            script_by_model[ms] += float(d.get("cost_usd") or 0)
        except (TypeError, ValueError):
            pass

    fail_models = []
    for ms in NO_REASONING_MODELS:
        if ms == "M11":
            continue
        diff = cost_by_model[ms] - script_by_model[ms]
        if abs(diff) > 0.05:
            fail_models.append((ms, diff))
            print(warn(f"  {ms} (no reasoning) diff=${diff:+.4f} - ожидался ~$0"))
        else:
            print(ok(f"  {ms} (no reasoning) diff=${diff:+.4f} - ожидался ~$0 ✓"))

    pass_models = []
    for ms in REASONING_MODELS:
        diff = cost_by_model[ms] - script_by_model[ms]
        if diff > 0.005:
            pass_models.append((ms, diff))
            print(ok(f"  {ms} (reasoning) diff=${diff:+.4f} - ожидался > $0 ✓"))
        else:
            print(warn(f"  {ms} (reasoning) diff=${diff:+.4f} - ожидался > $0"))

    if not fail_models and pass_models:
        print(ok("Подтверждено: расхождение ТОЛЬКО у моделей с reasoning. Гипотеза верна."))
        return True
    print(warn("Картина смешанная. Возможно, есть другие причины расхождения."))
    return False


# ============================================================
# Check 4: M11 ratings count is correct for H2
# ============================================================
def check_4_m11_ratings_count():
    print(hdr("Проверка 4. M11 имеет достаточно оценок для H2 (>3000)"))
    m11_ratings = []
    m1_ratings = []
    for cid, task, cond, d in load_cells():
        for rater, constructs in d.get("ratings", {}).items():
            if rater not in ("M1", "M11"):
                continue
            for cid_c, ele_map in constructs.items():
                if isinstance(ele_map, dict):
                    for v in ele_map.values():
                        if isinstance(v, (int, float)) and 1 <= v <= 7:
                            (m11_ratings if rater == "M11" else m1_ratings).append(v)
    print(f"  M1 ratings:  n={len(m1_ratings)}, mean={np.mean(m1_ratings):.3f}")
    print(f"  M11 ratings: n={len(m11_ratings)}, mean={np.mean(m11_ratings):.3f}")
    print(f"  Delta means: {np.mean(m11_ratings) - np.mean(m1_ratings):+.4f}")
    if len(m11_ratings) > 3000 and len(m1_ratings) > 3000:
        print(ok(f"Достаточная статистическая мощность для H2 (n > 3000 на каждую модель)."))
        return True
    print(fail(f"Низкая мощность: M1 n={len(m1_ratings)}, M11 n={len(m11_ratings)}. H2 ненадёжна."))
    return False


# ============================================================
# Check 5: H1 cluster stability holds with full data
# ============================================================
def check_5_h1_stability():
    print(hdr("Проверка 5. H1 - M1 и M11 в одном кластере (расстояние < 1.0)"))
    # Reload from analyze_phase2j metrics if available
    metrics_file = Path("analysis_phase2j/metrics.json")
    if not metrics_file.exists():
        print(fail("analysis_phase2j/metrics.json не найден. Запустите analyze_phase2j.py."))
        return False
    m = json.loads(metrics_file.read_text())
    h1 = m.get("H1", {})
    dist = h1.get("euclidean_2d_distance")
    if dist is None:
        print(fail("H1.euclidean_2d_distance отсутствует в metrics.json."))
        return False
    print(f"  Расстояние M1 ↔ M11 (2D): {dist:.4f}")
    print(f"  Медиана попарных расстояний в ядре: {h1.get('median_core_pairwise_dist', 'N/A'):.4f}")
    if dist < 1.0:
        print(ok(f"H1 SUPPORTED: M11 в кластере с M1 (расстояние {dist:.2f} < 1.0)."))
        return True
    print(fail(f"H1 SHAKY: расстояние {dist:.2f} > 1.0. Кластер стабильность под вопросом."))
    return False


# ============================================================
# Check 6: PCA robust without M3 (52% coverage)
# ============================================================
def check_6_robustness_without_m3():
    print(hdr("Проверка 6. H1 робастна без проблемной M3 (Gemini, 52% покрытие)"))
    # Build rating matrix excluding M3, run PCA, compute M1↔M11 distance
    try:
        from sklearn.decomposition import PCA
    except ImportError:
        print(fail("sklearn не установлен. pip install scikit-learn --break-system-packages"))
        return False

    cells = []
    for cid, t, c, d in load_cells():
        cells.append(d)

    construct_keys = []
    for cell in cells:
        for owner_model, items in cell.get("constructs", {}).items():
            for item in items:
                cid_c = item.get("id")
                if cid_c and item.get("left", "").strip() and item.get("right", "").strip():
                    construct_keys.append((cell["cell_id"], cid_c))

    models = [f"M{i}" for i in range(1, 12) if i != 3]  # exclude M3
    n = len(models); k = len(construct_keys)
    X = np.full((n, k), np.nan)
    cell_by_id = {c["cell_id"]: c for c in cells}
    for ci, (cell_id, c_id) in enumerate(construct_keys):
        cell = cell_by_id.get(cell_id, {})
        for mi, m in enumerate(models):
            rats = cell.get("ratings", {}).get(m, {}).get(c_id, {})
            if isinstance(rats, dict) and rats:
                vals = [v for v in rats.values() if isinstance(v, (int, float))]
                if vals:
                    X[mi, ci] = float(np.mean(vals))
    # Impute
    col_means = np.nanmean(X, axis=0)
    inds = np.where(np.isnan(X))
    X[inds] = np.take(col_means, inds[1])
    X[np.isnan(X)] = float(np.nanmean(X[~np.isnan(X)])) if np.any(~np.isnan(X)) else 0.0

    Xc = X - X.mean(axis=0, keepdims=True)
    pca = PCA(n_components=min(n-1, 5))
    coords = pca.fit_transform(Xc)
    i1 = models.index("M1"); i11 = models.index("M11")
    dist = float(np.hypot(coords[i1,0]-coords[i11,0], coords[i1,1]-coords[i11,1]))
    print(f"  Без M3: M1=PC1={coords[i1,0]:.3f}, PC2={coords[i1,1]:.3f}")
    print(f"  Без M3: M11=PC1={coords[i11,0]:.3f}, PC2={coords[i11,1]:.3f}")
    print(f"  Расстояние M1 ↔ M11 (без M3): {dist:.4f}")
    if dist < 1.0:
        print(ok(f"H1 РОБАСТНА: M11 ↔ M1 = {dist:.2f} даже без M3."))
        return True
    print(fail(f"H1 чувствительна к M3: расстояние без M3 = {dist:.2f}."))
    return False


# ============================================================
# Check 7: Per-task breakdown of H2
# ============================================================
def check_7_per_task_h2():
    print(hdr("Проверка 7. H2 не скрывает task-conditional эффект"))
    by_task = defaultdict(lambda: {"M1": [], "M11": []})
    for cid, task, cond, d in load_cells():
        for rater, constructs in d.get("ratings", {}).items():
            if rater not in ("M1", "M11"):
                continue
            for cid_c, ele_map in constructs.items():
                if isinstance(ele_map, dict):
                    for v in ele_map.values():
                        if isinstance(v, (int, float)) and 1 <= v <= 7:
                            by_task[task][rater].append(v)
    print(f"  {'Task':<6} {'M1 mean':>9} {'M11 mean':>9} {'delta':>8} {'n_M1':>6} {'n_M11':>6}")
    max_delta = 0
    for task in sorted(by_task.keys()):
        m1 = np.array(by_task[task]["M1"])
        m11 = np.array(by_task[task]["M11"])
        if len(m1) == 0 or len(m11) == 0:
            continue
        d = m11.mean() - m1.mean()
        max_delta = max(max_delta, abs(d))
        flag = " ⚠" if abs(d) > 0.3 else ""
        print(f"  {task:<6} {m1.mean():>9.3f} {m11.mean():>9.3f} {d:>+8.3f} {len(m1):>6} {len(m11):>6}{flag}")
    if max_delta < 0.3:
        print(ok(f"Ни на одной задаче |delta| > 0.3 (max={max_delta:.3f}). H2 устойчива."))
        return True
    print(warn(f"На одной из задач |delta| = {max_delta:.3f} > 0.3. H2 нужно переформулировать в task-specific."))
    return False


# ============================================================
# Main
# ============================================================
def main():
    print(f"{BOLD}=========================================")
    print(f"  Phase 2J Final Verification")
    print(f"========================================={RESET}")
    if not PHASE2J_DIR.exists():
        print(fail(f"{PHASE2J_DIR}/ не найден. Запускайте из C:\\Users\\Sergey\\archipelago_cross_model"))
        return 1

    results = []
    results.append(("1. M11 = real Opus 4.8", check_1_m11_is_real_opus48()))
    results.append(("2. Real Phase 2J cost = $15.32", check_2_real_cost()))
    results.append(("3. Reasoning undercount confirmed", check_3_reasoning_undercount()))
    results.append(("4. H2 statistical power ok", check_4_m11_ratings_count()))
    results.append(("5. H1 cluster stability holds", check_5_h1_stability()))
    results.append(("6. PCA robust without M3", check_6_robustness_without_m3()))
    results.append(("7. H2 no per-task masking", check_7_per_task_h2()))

    print(f"\n{BOLD}=== FINAL SUMMARY ==={RESET}")
    n_pass = sum(1 for _, r in results if r)
    for name, r in results:
        marker = f"{GREEN}PASS{RESET}" if r else f"{RED}FAIL{RESET}"
        print(f"  [{marker}] {name}")
    print(f"\n{BOLD}Result: {n_pass}/{len(results)} checks passed.{RESET}")
    if n_pass == len(results):
        print(f"{GREEN}All checks passed. Phase 2J готова к публикации.{RESET}")
        return 0
    else:
        print(f"{YELLOW}Some checks failed - см. подробности выше.{RESET}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
