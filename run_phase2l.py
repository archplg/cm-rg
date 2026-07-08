"""
Phase 2L · Main pipeline runner.

4-phase Cross-Model Repertory Grid (CM-RG) experiment:
  Phase 1 · Free response (each model writes 200-400 word recommendation per (task, condition))
  Phase 2 · Blind anonymization (computational, strips model signatures)
  Phase 3 · Triadic elicitation (each model extracts constructs from 3 anonymized responses)
  Phase 4 · Cross-rating (each model rates all responses on all constructs)

All defenses from pre-flight checks:
  - Atomic writes (.tmp -> fsync -> rename + backups, Check 4)
  - Retry with [10,30,90]s backoff on 429/500/timeout (Check 6)
  - usage.cost tracked + alert on $0 (Check 2)
  - Strict parser validation (Check 3)
  - Per-provider spend caps with auto-halt
  - Live state.json updates for dashboard (Check 5)
  - Resume capability - skips cells that already exist with valid data

Usage:
    set OPENROUTER_API_KEY=sk-or-...
    python run_phase2l.py --phase 1          # Phase 1 only
    python run_phase2l.py --phase 2          # Phase 2 only
    python run_phase2l.py --phase 3          # Phase 3 only
    python run_phase2l.py --phase 4          # Phase 4 only
    python run_phase2l.py --phase all        # All phases sequentially
    python run_phase2l.py --phase 1 --pilot K  # Pilot: single task only
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import random
import re
import shutil
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

try:
    import yaml
    import requests
except ImportError as e:
    print(f"ERROR: missing dependency ({e}). Run: pip install pyyaml requests")
    sys.exit(1)


# ============================================================================
# Atomic write helpers (from Check 4)
# ============================================================================

def atomic_write_json(target: Path, data: dict | list, keep_backups: int = 3) -> None:
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        backup_dir = target.parent / "_backups"
        backup_dir.mkdir(exist_ok=True)
        ts = int(time.time() * 1000)
        backup_path = backup_dir / f"{target.stem}_{ts}.json"
        try:
            shutil.copy2(target, backup_path)
            backups = sorted(backup_dir.glob(f"{target.stem}_*.json"))
            for old in backups[:-keep_backups]:
                try:
                    old.unlink()
                except (FileNotFoundError, PermissionError):
                    pass
        except (FileNotFoundError, PermissionError):
            pass

    tmp_path = target.with_suffix(target.suffix + ".tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.flush()
        try:
            os.fsync(f.fileno())
        except OSError:
            pass
    os.replace(tmp_path, target)


def _safe_atomic_write_json(target: Path, data: dict | list, max_retries: int = 5) -> None:
    """Wrapper for atomic_write_json that retries on Windows PermissionError.

    On Windows, file scanners (Defender), backup services, or even Explorer can briefly
    lock newly-created files. Retry up to 5 times with short backoffs (0.05-0.5s) before
    giving up. Total worst case: ~1.5s delay if all 5 retries used.
    """
    for attempt in range(max_retries):
        try:
            atomic_write_json(target, data)
            return
        except (PermissionError, OSError) as e:
            if attempt == max_retries - 1:
                # Last try - swallow it. Worst case: this one save() lost but data
                # is in memory and will be persisted on next successful save.
                print(f"    [STATE_WRITE_LOST] {type(e).__name__} after {max_retries} retries: {str(e)[:80]}")
                return
            time.sleep(0.05 * (attempt + 1))  # 50ms, 100ms, 150ms, 200ms


def cell_exists_valid(path: Path, min_size: int = 100) -> bool:
    """Check if cell file exists and has valid JSON above min size."""
    if not path.exists():
        return False
    try:
        if path.stat().st_size < min_size:
            return False
        json.loads(path.read_text(encoding="utf-8"))
        return True
    except (json.JSONDecodeError, OSError):
        return False


# ============================================================================
# OpenRouter API client with retry (from Check 6)
# ============================================================================

RETRY_STATUS_CODES = {429, 500, 502, 503, 504}
NO_RETRY_STATUS_CODES = {400, 401, 403, 404}


def call_openrouter_with_retry(
    *, api_key: str, base_url: str, model_slug: str,
    system_prompt: str, user_prompt: str,
    max_tokens: int, temperature: float, timeout: int,
    retries: int, backoffs: list[int],
) -> dict[str, Any]:
    url = base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://crossmodelrg.org",
        "X-Title": "CM-RG Phase 2L",
    }
    payload = {
        "model": model_slug,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": temperature,
        "usage": {"include": True},
    }

    # Broader catch-all for network issues:
    # - Timeout, ConnectionError (initial connect failed)
    # - ChunkedEncodingError (connection broke mid-response - what killed us before)
    # - ProtocolError, IncompleteRead (TLS/HTTP protocol corruption)
    # - ConnectionResetError, BrokenPipeError, OSError (low-level socket failures)
    # - generic RequestException as catch-all for any requests-layer issue
    RETRY_EXC = (
        requests.exceptions.Timeout,
        requests.exceptions.ConnectionError,
        requests.exceptions.ChunkedEncodingError,
        requests.exceptions.ContentDecodingError,
        requests.exceptions.RequestException,  # base class catch-all
        ConnectionResetError,
        ConnectionAbortedError,
        BrokenPipeError,
        OSError,  # low-level socket
    )

    attempts = 0
    last_error = None
    while attempts <= retries:
        attempts += 1
        try:
            t0 = time.time()
            resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
            latency_ms = int((time.time() - t0) * 1000)
            if resp.status_code == 200:
                # Wrap body read - ChunkedEncodingError can fire here too
                try:
                    body = resp.json()
                except Exception as je:
                    if attempts <= retries:
                        backoff = backoffs[min(attempts - 1, len(backoffs) - 1)]
                        print(f"      retry {attempts}/{retries+1}: body parse failed ({type(je).__name__}), backoff {backoff}s")
                        time.sleep(backoff)
                        continue
                    return {"status": 200, "body": None, "latency_ms": latency_ms,
                            "attempts": attempts, "error": f"body_parse: {je}"}
                return {"status": 200, "body": body, "latency_ms": latency_ms, "attempts": attempts}
            if resp.status_code in NO_RETRY_STATUS_CODES:
                try:
                    body = resp.json() if resp.content else None
                except Exception:
                    body = None
                return {"status": resp.status_code, "body": body,
                        "latency_ms": latency_ms, "attempts": attempts, "error": "client_error"}
            if resp.status_code in RETRY_STATUS_CODES and attempts <= retries:
                backoff = backoffs[min(attempts - 1, len(backoffs) - 1)]
                print(f"      retry {attempts}/{retries+1}: HTTP {resp.status_code}, backoff {backoff}s")
                time.sleep(backoff)
                continue
            try:
                body = resp.json() if resp.content else None
            except Exception:
                body = None
            return {"status": resp.status_code, "body": body,
                    "latency_ms": latency_ms, "attempts": attempts, "error": "server_error"}
        except RETRY_EXC as e:
            last_error = f"{type(e).__name__}: {e}"
            if attempts <= retries:
                backoff = backoffs[min(attempts - 1, len(backoffs) - 1)]
                print(f"      retry {attempts}/{retries+1}: {type(e).__name__}: {str(e)[:80]}, backoff {backoff}s")
                time.sleep(backoff)
                continue
            return {"status": 0, "body": None, "latency_ms": 0, "attempts": attempts, "error": last_error}
        except Exception as e:
            # Unknown error - don't kill the script, log and move on
            last_error = f"{type(e).__name__}: {e}"
            print(f"      UNEXPECTED {type(e).__name__}: {str(e)[:120]} (skipping)")
            return {"status": 0, "body": None, "latency_ms": 0, "attempts": attempts, "error": last_error}

    return {"status": 0, "body": None, "latency_ms": 0, "attempts": attempts, "error": last_error}


def extract_cost(body: dict | None) -> float:
    if not body:
        return 0.0
    usage = body.get("usage") or {}
    if not isinstance(usage, dict):
        return 0.0
    c = usage.get("cost")
    if c is not None:
        try:
            return float(c)
        except (TypeError, ValueError):
            pass
    cd = usage.get("cost_details") or {}
    if isinstance(cd, dict):
        up = cd.get("upstream_inference_cost")
        if up is not None:
            try:
                return float(up)
            except (TypeError, ValueError):
                pass
    return 0.0


def extract_content(body: dict | None) -> str:
    if not body:
        return ""
    choices = body.get("choices") or []
    if not choices:
        return ""
    msg = choices[0].get("message") or {}
    return msg.get("content") or ""


# ============================================================================
# State management (for live dashboard)
# ============================================================================

class State:
    def __init__(self, state_path: Path, cells_total: int):
        self.path = state_path
        self._lock = threading.Lock()  # thread-safe for parallel workers
        self.data = {
            "started_at_ms": int(time.time() * 1000),
            "cells_total": cells_total,
            "cells_completed": 0,
            "calls_total": 0,
            "errors_count": 0,
            "total_cost_usd": 0.0,
            "providers": {},
            "recent_activity": [],
        }
        self.save()

    def save(self):
        with self._lock:
            _safe_atomic_write_json(self.path, dict(self.data))

    def record_call(self, *, family: str, slug: str, short: str, tier: str,
                    task: str, cond: str, phase: int,
                    status: str, cost_usd: float, latency_ms: int):
        # Hold lock throughout mutation AND write - prevents Windows WinError 32
        # on state.json.tmp -> state.json rename race
        with self._lock:
            self.data["calls_total"] += 1
            self.data["total_cost_usd"] += cost_usd
            if status != "OK":
                self.data["errors_count"] += 1
            prov = self.data["providers"].setdefault(family, {"calls": 0, "cost_usd": 0.0})
            prov["calls"] += 1
            prov["cost_usd"] += cost_usd
            self.data["recent_activity"].append({
                "ts": dt.datetime.now().strftime("%H:%M:%S"),
                "short": short, "tier": tier, "slug": slug,
                "task": task, "cond": cond, "phase": phase,
                "status": status, "cost_usd": cost_usd, "latency_ms": latency_ms,
            })
            self.data["recent_activity"] = self.data["recent_activity"][-50:]
            _safe_atomic_write_json(self.path, dict(self.data))

    def record_cell_done(self):
        with self._lock:
            self.data["cells_completed"] += 1
            _safe_atomic_write_json(self.path, dict(self.data))

    def check_provider_cap(self, family: str, cap_usd: float) -> bool:
        with self._lock:
            prov = self.data["providers"].get(family, {})
            return (prov.get("cost_usd") or 0) >= cap_usd

    def consecutive_network_failures(self, window: int = 10) -> int:
        """Return how many of the last `window` calls were HTTP_0 (network down)."""
        with self._lock:
            recent = list(self.data["recent_activity"][-window:])
        return sum(1 for r in recent if str(r.get("status", "")).startswith("HTTP_0"))

    def phase_success_rate(self, phase: int) -> tuple[int, int]:
        """Return (ok_count, total) for given phase from recent_activity."""
        with self._lock:
            phase_calls = [r for r in self.data["recent_activity"] if r.get("phase") == phase]
        ok = sum(1 for r in phase_calls if r.get("status") == "OK")
        return ok, len(phase_calls)

    def total_cost(self) -> float:
        with self._lock:
            return float(self.data.get("total_cost_usd") or 0)


def check_network_alive(state: State, threshold: int = 5) -> bool:
    """Check if we should bail because internet seems dead.

    If last `threshold` consecutive calls all failed with HTTP_0, sleep long, then
    return False to abort current phase. User can resume after fixing internet.
    """
    failures = state.consecutive_network_failures(window=threshold)
    if failures >= threshold:
        print(f"\n  ABORT PHASE: {failures} consecutive network failures detected.")
        print(f"  Check internet connection. Re-run command to resume (resume logic will skip done cells).")
        return False
    return True


# ============================================================================
# Phase 1: Free response
# ============================================================================

PHASE1_TEMPLATE_NEUTRAL = (
    "You are an analyst. Read the brief carefully. "
    "Provide your best-reasoned recommendation in 300-500 words. "
    "Be specific - advocate clearly for one approach. "
    "Brief follows.\n\n"
)

PHASE1_TEMPLATE_PERSONA = {
    "Q": "You are a Quantitative analyst. Prioritize data, models, and measurable outcomes. ",
    "S": "You are a Strategic advisor. Prioritize long-term positioning and competitive dynamics. ",
    "E": "You are an Ethical evaluator. Prioritize stakeholder welfare and fairness. ",
    "H": "You are a Humanistic counselor. Prioritize relationships, identity, and meaning. ",
    "C": "You are a Conservative steward. Prioritize risk reduction and continuity. ",
}


def run_phase1(config: dict, api_key: str, results_dir: Path, state: State,
               pilot_task: str | None = None) -> None:
    print(f"\n{'='*100}\n  PHASE 1 · Free response\n{'='*100}\n")
    free_p = config["parameters"]["free_response"]
    or_cfg = config["openrouter"]
    cap = float(config["experiment"]["spend_cap_per_provider_usd"])

    persona_list = ["Q", "S", "E", "H", "C"]

    for task in config["tasks"]:
        tid = str(task["id"])
        if pilot_task and tid != pilot_task:
            continue
        brief_path = Path(task["brief_file"])
        if not brief_path.exists():
            print(f"  [SKIP] task {tid}: brief file missing ({brief_path})")
            continue
        brief = brief_path.read_text(encoding="utf-8")

        for cond in config["conditions"]:
            cid = cond["id"]
            cond_name = cond["name"]
            use_personas = cond.get("use_personas", False)

            print(f"\n  Task={tid}  Condition={cid} ({cond_name})")

            for i, m in enumerate(config["models"]):
                slug = m["id"]
                fallback = m.get("fallback_id")
                short = m["short_name"]
                family = m["family"]
                tier = m["tier"]

                # Persona assignment via simple round-robin (Latin square equivalent)
                if use_personas:
                    persona_code = persona_list[i % 5]
                    system_prompt = PHASE1_TEMPLATE_PERSONA[persona_code] + (
                        "Provide your best-reasoned recommendation in 300-500 words. "
                        "Be specific - advocate clearly for one approach. "
                        "Brief follows.\n\n"
                    )
                else:
                    persona_code = "N"
                    system_prompt = PHASE1_TEMPLATE_NEUTRAL

                # Resume: skip if cell exists
                cell_path = results_dir / "phase1_free_response" / tid / cid / f"{short}.json"
                if cell_exists_valid(cell_path):
                    print(f"    [SKIP] {short:<6} (already done)")
                    continue

                # Provider cap check
                if state.check_provider_cap(family, cap):
                    print(f"    [HALT] {short:<6} - {family} hit ${cap} cap")
                    continue

                # Network outage check
                if not check_network_alive(state):
                    return

                user_prompt = brief

                # Try primary, then fallback on 400/404
                used_slug = slug
                result = call_openrouter_with_retry(
                    api_key=api_key, base_url=or_cfg["base_url"], model_slug=slug,
                    system_prompt=system_prompt, user_prompt=user_prompt,
                    max_tokens=int(free_p["max_tokens"]), temperature=float(free_p["temperature"]),
                    timeout=int(or_cfg["request_timeout_seconds"]),
                    retries=int(or_cfg["retries_per_call"]),
                    backoffs=or_cfg["retry_backoff_seconds"],
                )
                if result["status"] in NO_RETRY_STATUS_CODES and fallback:
                    print(f"    [FB ] {short:<6} primary failed HTTP{result['status']}, trying {fallback}")
                    result = call_openrouter_with_retry(
                        api_key=api_key, base_url=or_cfg["base_url"], model_slug=fallback,
                        system_prompt=system_prompt, user_prompt=user_prompt,
                        max_tokens=int(free_p["max_tokens"]), temperature=float(free_p["temperature"]),
                        timeout=int(or_cfg["request_timeout_seconds"]),
                        retries=int(or_cfg["retries_per_call"]),
                        backoffs=or_cfg["retry_backoff_seconds"],
                    )
                    used_slug = fallback

                content = extract_content(result["body"])
                cost = extract_cost(result["body"])
                status = "OK" if result["status"] == 200 else f"HTTP_{result['status']}"

                cell = {
                    "task": tid, "condition": cid, "persona": persona_code,
                    "model_slug": used_slug, "fallback_used": used_slug != slug,
                    "family": family, "tier": tier, "short_name": short,
                    "system_prompt": system_prompt,
                    "user_prompt": user_prompt,
                    "response": content,
                    "usage": (result["body"] or {}).get("usage", {}),
                    "cost_usd": cost,
                    "latency_ms": result["latency_ms"],
                    "attempts": result["attempts"],
                    "timestamp": dt.datetime.now().isoformat(),
                }
                if status == "OK":
                    atomic_write_json(cell_path, cell)
                state.record_call(family=family, slug=used_slug, short=short, tier=tier,
                                  task=tid, cond=cid, phase=1, status=status,
                                  cost_usd=cost, latency_ms=result["latency_ms"])

                cost_str = f"${cost:.4f}"
                print(f"    [{status:<8}] {short:<6} {family:<10} {used_slug:<48} {cost_str:>9}  {result['latency_ms']:>5}ms")


# ============================================================================
# Phase 2: Blind anonymization (computational, no API)
# ============================================================================

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
    # Collapse whitespace
    out = re.sub(r"\s+", " ", out).strip()
    return out


def run_phase2(config: dict, results_dir: Path, state: State, pilot_task: str | None = None) -> None:
    print(f"\n{'='*100}\n  PHASE 2 · Anonymization (computational)\n{'='*100}\n")
    phase1_dir = results_dir / "phase1_free_response"
    if not phase1_dir.exists():
        print("  ERROR: phase1 results missing. Run --phase 1 first.")
        return

    total = 0
    for task in config["tasks"]:
        tid = str(task["id"])
        if pilot_task and tid != pilot_task:
            continue
        for cond in config["conditions"]:
            cid = cond["id"]
            for m in config["models"]:
                short = m["short_name"]
                p1 = phase1_dir / tid / cid / f"{short}.json"
                if not cell_exists_valid(p1):
                    continue
                p2 = results_dir / "phase2_anonymized" / tid / cid / f"{short}.json"
                if cell_exists_valid(p2):
                    continue
                data = json.loads(p1.read_text(encoding="utf-8"))
                anon = anonymize_text(data.get("response") or "")
                out = {
                    "task": tid, "condition": cid, "short_name": short,
                    "anonymized_text": anon,
                    "original_length": len(data.get("response") or ""),
                    "anonymized_length": len(anon),
                    "source_file": str(p1),
                }
                atomic_write_json(p2, out)
                total += 1
    print(f"  Anonymized {total} cells.")


# ============================================================================
# Phase 3: Triadic elicitation
# ============================================================================

PHASE3_SYSTEM = (
    "You are participating in a Personal Constructs research study. You will see three "
    "anonymized advisory responses to the same brief. Your task: identify constructs - "
    "bipolar dimensions on which responses differ. Use the triadic method: for each "
    "construct, two responses share a quality that the third lacks.\n\n"
    "Output ONLY valid JSON in this format:\n"
    '[{"pole_a": "decisive", "pole_b": "deliberative", "context": "decision style"}, ...]\n\n'
    "Provide 8-12 constructs. Each pole should be a single adjective or short noun phrase. "
    "Do not include any text outside the JSON array."
)


def run_phase3(config: dict, api_key: str, results_dir: Path, state: State,
               pilot_task: str | None = None) -> None:
    print(f"\n{'='*100}\n  PHASE 3 · Triadic elicitation\n{'='*100}\n")
    phase2_dir = results_dir / "phase2_anonymized"
    if not phase2_dir.exists():
        print("  ERROR: phase2 results missing. Run --phase 2 first.")
        return
    cons_p = config["parameters"]["constructs"]
    or_cfg = config["openrouter"]
    cap = float(config["experiment"]["spend_cap_per_provider_usd"])

    rng = random.Random(42)

    for task in config["tasks"]:
        tid = str(task["id"])
        if pilot_task and tid != pilot_task:
            continue
        for cond in config["conditions"]:
            cid = cond["id"]
            print(f"\n  Task={tid}  Condition={cid}")

            # Gather all anonymized responses for this (task, cond)
            anon_paths = sorted((phase2_dir / tid / cid).glob("*.json"))
            anon_map = {}  # short -> text
            for p in anon_paths:
                d = json.loads(p.read_text(encoding="utf-8"))
                anon_map[d["short_name"]] = d["anonymized_text"]

            if len(anon_map) < 3:
                print(f"    [SKIP] only {len(anon_map)} anonymized responses, need 3+")
                continue

            for m in config["models"]:
                slug = m["id"]
                short = m["short_name"]
                family = m["family"]
                tier = m["tier"]
                fallback = m.get("fallback_id")

                cell_path = results_dir / "phase3_constructs" / tid / cid / f"{short}.json"
                if cell_exists_valid(cell_path):
                    print(f"    [SKIP] {short:<6} (already done)")
                    continue
                if state.check_provider_cap(family, cap):
                    print(f"    [HALT] {short:<6} - {family} hit cap")
                    continue
                if not check_network_alive(state):
                    return

                # Pick 3 random responses from OTHER models (exclude self)
                candidates = [s for s in anon_map if s != short]
                if len(candidates) < 3:
                    print(f"    [SKIP] {short:<6} - not enough other responses")
                    continue
                triad = rng.sample(candidates, 3)
                triad_text = ""
                for i, s in enumerate(triad):
                    triad_text += f"\n\n=== Response {chr(65+i)} ===\n{anon_map[s]}"

                user_prompt = f"Three anonymized responses:{triad_text}\n\nIdentify 8-12 constructs."

                used_slug = slug
                result = call_openrouter_with_retry(
                    api_key=api_key, base_url=or_cfg["base_url"], model_slug=slug,
                    system_prompt=PHASE3_SYSTEM, user_prompt=user_prompt,
                    max_tokens=int(cons_p["max_tokens"]), temperature=float(cons_p["temperature"]),
                    timeout=int(or_cfg["request_timeout_seconds"]),
                    retries=int(or_cfg["retries_per_call"]),
                    backoffs=or_cfg["retry_backoff_seconds"],
                )
                if result["status"] in NO_RETRY_STATUS_CODES and fallback:
                    result = call_openrouter_with_retry(
                        api_key=api_key, base_url=or_cfg["base_url"], model_slug=fallback,
                        system_prompt=PHASE3_SYSTEM, user_prompt=user_prompt,
                        max_tokens=int(cons_p["max_tokens"]), temperature=float(cons_p["temperature"]),
                        timeout=int(or_cfg["request_timeout_seconds"]),
                        retries=int(or_cfg["retries_per_call"]),
                        backoffs=or_cfg["retry_backoff_seconds"],
                    )
                    used_slug = fallback

                content = extract_content(result["body"])
                cost = extract_cost(result["body"])
                status = "OK" if result["status"] == 200 else f"HTTP_{result['status']}"

                # Parse constructs (use improved parser - strips reasoning tags)
                from check3_parser_test import parse_constructs
                constructs = parse_constructs(content)

                cell = {
                    "task": tid, "condition": cid,
                    "rater_short": short, "rater_slug": used_slug,
                    "rater_family": family, "rater_tier": tier,
                    "triad": triad,
                    "raw_response": content,
                    "constructs": constructs,
                    "n_constructs": len(constructs),
                    "usage": (result["body"] or {}).get("usage", {}),
                    "cost_usd": cost,
                    "latency_ms": result["latency_ms"],
                    "timestamp": dt.datetime.now().isoformat(),
                }
                # Write only if API call succeeded AND parser got reasonable constructs.
                # n_constructs=0 means parser failed - don't pollute resume logic.
                if status == "OK" and len(constructs) >= 1:
                    atomic_write_json(cell_path, cell)
                state.record_call(family=family, slug=used_slug, short=short, tier=tier,
                                  task=tid, cond=cid, phase=3, status=status,
                                  cost_usd=cost, latency_ms=result["latency_ms"])
                print(f"    [{status:<8}] {short:<6} n_constructs={len(constructs):<3} ${cost:.4f}  {result['latency_ms']}ms")


# ============================================================================
# Phase 4: Cross-rating
# ============================================================================

PHASE4_SYSTEM = (
    "You are rating advisory responses on a personal constructs grid. "
    "You will see a list of CONSTRUCTS (bipolar dimensions) and a list of anonymized RESPONSES. "
    "Rate each response on each construct using a 1-7 scale where 1=strongly pole_a, 7=strongly pole_b, 4=neutral.\n\n"
    'Output ONLY valid JSON: {"ratings": [[1, 4, 7, ...], ...]} where outer array is per-response, '
    'inner array is per-construct in the listed order. No text outside the JSON.'
)

PHASE4_CONSTRUCTS_PER_BATCH = 50  # to keep output under max_tokens


def parse_ratings_json(content: str) -> list:
    """Robust parser for Phase 4 ratings response.

    Handles:
      - <thinking> / <reasoning> tags from reasoning models
      - ```json ... ``` markdown fences
      - Extra prose before/after JSON
      - Multiple JSON objects (picks the one with "ratings" key)
      - Balanced bracket extraction (no greedy regex)
    """
    if not content:
        return []
    # 1. Strip reasoning tags
    cleaned = re.sub(r"<(thinking|reasoning|analysis|reflection|scratchpad)>[\s\S]*?</\1>",
                     "", content, flags=re.IGNORECASE)
    cleaned = re.sub(r"</?(thinking|reasoning|analysis|reflection|scratchpad)>",
                     "", cleaned, flags=re.IGNORECASE)
    # 2. Strip markdown fences
    cleaned = re.sub(r"```(?:json|JSON)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```", "", cleaned)

    # 3. Find "ratings" keyword, walk back to matching {, walk forward to matching }
    idx = cleaned.find('"ratings"')
    if idx == -1:
        idx = cleaned.find("'ratings'")
    if idx == -1:
        # Try direct JSON parse - maybe whole content is just the array
        try:
            obj = json.loads(cleaned.strip())
            if isinstance(obj, dict):
                return obj.get("ratings", []) or []
            if isinstance(obj, list):
                return obj  # raw array of arrays
        except json.JSONDecodeError:
            pass
        return []

    start = cleaned.rfind('{', 0, idx)
    if start == -1:
        return []

    # Balanced bracket walk
    depth = 0
    in_string = False
    escape = False
    end = -1
    for i in range(start, len(cleaned)):
        c = cleaned[i]
        if escape:
            escape = False
            continue
        if c == '\\' and in_string:
            escape = True
            continue
        if c == '"':
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                end = i
                break

    if end == -1:
        return []
    try:
        obj = json.loads(cleaned[start:end + 1])
        return obj.get("ratings", []) or []
    except json.JSONDecodeError:
        return []


def _process_rater_phase4(
    *, m: dict, anon_list: list, all_constructs: list, n_batches: int,
    api_key: str, or_cfg: dict, ratings_p: dict, cap: float,
    state: State, results_dir: Path, tid: str, cid: str,
    budget_cap_usd: float | None = None,
) -> dict:
    """Process ONE rater's complete cross-rating cell (all batches).

    Designed to run inside a ThreadPoolExecutor worker. Returns summary dict.
    """
    slug = m["id"]
    short = m["short_name"]
    family = m["family"]
    tier = m["tier"]
    fallback = m.get("fallback_id")

    cell_path = results_dir / "phase4_ratings" / tid / cid / f"{short}.json"
    if cell_exists_valid(cell_path):
        return {"short": short, "status": "SKIP", "msg": "already done"}
    if state.check_provider_cap(family, cap):
        return {"short": short, "status": "HALT_CAP", "msg": f"{family} hit cap"}
    if not check_network_alive(state):
        return {"short": short, "status": "NETWORK_DOWN", "msg": "abort"}
    if budget_cap_usd is not None and state.total_cost() >= budget_cap_usd:
        return {"short": short, "status": "BUDGET_CAP", "msg": f"total spend reached ${budget_cap_usd}"}

    all_ratings_for_rater = []
    total_cost = 0.0
    total_latency = 0
    ok_count = 0

    for batch_i in range(n_batches):
        batch_constructs = all_constructs[batch_i * PHASE4_CONSTRUCTS_PER_BATCH:
                                          (batch_i + 1) * PHASE4_CONSTRUCTS_PER_BATCH]
        cons_str = "\n".join([f"{i+1}. {c['pole_a']} (1) vs {c['pole_b']} (7) [{c.get('context','')}]"
                              for i, c in enumerate(batch_constructs)])
        resp_str = "\n\n".join([f"=== Response {chr(65+i)} ({r['short']}) ===\n{r['text']}"
                                for i, r in enumerate(anon_list)])
        user_prompt = (
            f"CONSTRUCTS ({len(batch_constructs)}):\n{cons_str}\n\n"
            f"RESPONSES ({len(anon_list)}):\n{resp_str}\n\n"
            f'Return JSON {{"ratings": [[<{len(batch_constructs)} ints>], ...]}} '
            f"with {len(anon_list)} response arrays."
        )

        used_slug = slug
        result = call_openrouter_with_retry(
            api_key=api_key, base_url=or_cfg["base_url"], model_slug=slug,
            system_prompt=PHASE4_SYSTEM, user_prompt=user_prompt,
            max_tokens=int(ratings_p["max_tokens"]), temperature=float(ratings_p["temperature"]),
            timeout=int(or_cfg["request_timeout_seconds"]),
            retries=int(or_cfg["retries_per_call"]),
            backoffs=or_cfg["retry_backoff_seconds"],
        )
        if result["status"] in NO_RETRY_STATUS_CODES and fallback:
            result = call_openrouter_with_retry(
                api_key=api_key, base_url=or_cfg["base_url"], model_slug=fallback,
                system_prompt=PHASE4_SYSTEM, user_prompt=user_prompt,
                max_tokens=int(ratings_p["max_tokens"]), temperature=float(ratings_p["temperature"]),
                timeout=int(or_cfg["request_timeout_seconds"]),
                retries=int(or_cfg["retries_per_call"]),
                backoffs=or_cfg["retry_backoff_seconds"],
            )
            used_slug = fallback

        content = extract_content(result["body"])
        cost = extract_cost(result["body"])
        total_cost += cost
        total_latency += result["latency_ms"]

        # Robust parser: strips reasoning tags, markdown fences, balanced brackets
        batch_ratings = parse_ratings_json(content)
        if batch_ratings:
            all_ratings_for_rater.append({
                "batch": batch_i,
                "constructs": batch_constructs,
                "ratings": batch_ratings,
                "raw_content": content[:1000],  # keep for re-parse if needed
            })
            if result["status"] == 200:
                ok_count += 1
        else:
            all_ratings_for_rater.append({
                "batch": batch_i, "constructs": batch_constructs,
                "parse_error": True,
                "raw_content": content[:2000],  # keep full raw for re-parse
            })
        state.record_call(family=family, slug=used_slug, short=short, tier=tier,
                          task=tid, cond=cid, phase=4,
                          status="OK" if result["status"] == 200 else f"HTTP_{result['status']}",
                          cost_usd=cost, latency_ms=result["latency_ms"])

    cell = {
        "task": tid, "condition": cid,
        "rater_short": short, "rater_slug": slug,
        "rater_family": family, "rater_tier": tier,
        "rated_responses": [r["short"] for r in anon_list],
        "batches": all_ratings_for_rater,
        "n_batches": n_batches,
        "n_constructs_total": len(all_constructs),
        "total_cost_usd": total_cost,
        "total_latency_ms": total_latency,
        "ok_batches": ok_count,
        "timestamp": dt.datetime.now().isoformat(),
    }
    atomic_write_json(cell_path, cell)
    return {"short": short, "status": "DONE", "ok_count": ok_count,
            "n_batches": n_batches, "total_cost": total_cost, "total_latency": total_latency}


def run_phase4(config: dict, api_key: str, results_dir: Path, state: State,
               pilot_task: str | None = None, workers: int = 4,
               budget_cap_usd: float | None = None) -> None:
    print(f"\n{'='*100}\n  PHASE 4 · Cross-rating (workers={workers})\n{'='*100}\n")
    phase2_dir = results_dir / "phase2_anonymized"
    phase3_dir = results_dir / "phase3_constructs"
    if not phase2_dir.exists() or not phase3_dir.exists():
        print("  ERROR: phase2 or phase3 missing. Run earlier phases first.")
        return
    ratings_p = config["parameters"]["ratings"]
    or_cfg = config["openrouter"]
    cap = float(config["experiment"]["spend_cap_per_provider_usd"])

    for task in config["tasks"]:
        tid = str(task["id"])
        if pilot_task and tid != pilot_task:
            continue
        for cond in config["conditions"]:
            cid = cond["id"]
            print(f"\n  Task={tid}  Condition={cid}")

            anon_paths = sorted((phase2_dir / tid / cid).glob("*.json"))
            anon_list = []
            for p in anon_paths:
                d = json.loads(p.read_text(encoding="utf-8"))
                anon_list.append({"short": d["short_name"], "text": d["anonymized_text"]})

            cons_paths = sorted((phase3_dir / tid / cid).glob("*.json"))
            all_constructs = []
            for p in cons_paths:
                d = json.loads(p.read_text(encoding="utf-8"))
                for c in d.get("constructs", []):
                    all_constructs.append({**c, "from_rater": d["rater_short"]})

            if not anon_list or not all_constructs:
                print(f"    [SKIP] missing data: {len(anon_list)} anons, {len(all_constructs)} constructs")
                continue

            print(f"    {len(anon_list)} responses x {len(all_constructs)} constructs to rate")
            n_batches = (len(all_constructs) + PHASE4_CONSTRUCTS_PER_BATCH - 1) // PHASE4_CONSTRUCTS_PER_BATCH

            # Submit all raters to thread pool
            with ThreadPoolExecutor(max_workers=workers, thread_name_prefix="rater") as pool:
                futures = {}
                for m in config["models"]:
                    f = pool.submit(
                        _process_rater_phase4,
                        m=m, anon_list=anon_list, all_constructs=all_constructs, n_batches=n_batches,
                        api_key=api_key, or_cfg=or_cfg, ratings_p=ratings_p, cap=cap,
                        state=state, results_dir=results_dir, tid=tid, cid=cid,
                        budget_cap_usd=budget_cap_usd,
                    )
                    futures[f] = m["short_name"]

                # Collect results as they complete - print in arrival order
                for f in as_completed(futures):
                    short_name = futures[f]
                    try:
                        r = f.result()
                    except Exception as e:
                        print(f"    [WORKER_ERR] {short_name:<6} {type(e).__name__}: {e}")
                        continue

                    if r["status"] == "DONE":
                        print(f"    [{r['ok_count']}/{r['n_batches']}] {r['short']:<6} "
                              f"${r['total_cost']:.4f}  {r['total_latency']}ms")
                    elif r["status"] == "SKIP":
                        print(f"    [SKIP] {r['short']:<6} {r['msg']}")
                    elif r["status"] in ("HALT_CAP", "BUDGET_CAP", "NETWORK_DOWN"):
                        print(f"    [{r['status']}] {r['short']:<6} {r['msg']}")

            # After each (task, cond), report cumulative spend
            print(f"    cumulative total: ${state.total_cost():.2f}")
            if budget_cap_usd is not None and state.total_cost() >= budget_cap_usd:
                print(f"\n  ABORT: total spend ${state.total_cost():.2f} >= ${budget_cap_usd} cap.")
                return


# ============================================================================
# Main
# ============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 2L main runner")
    parser.add_argument("--config", default="config_phase2l.yaml")
    parser.add_argument("--phase", choices=["1", "2", "3", "4", "all"], default="all")
    parser.add_argument("--pilot", default=None, help="Run only one task (e.g. --pilot K)")
    parser.add_argument("--workers", type=int, default=4,
                        help="Parallel workers for Phase 4 cross-rating (default 4, 1=sequential)")
    parser.add_argument("--budget-cap", type=float, default=None,
                        help="Hard stop if total spend reaches this $$$ (e.g. --budget-cap 190)")
    args = parser.parse_args()

    with open(args.config, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY not set.")
        return 2

    results_dir = Path(config["experiment"]["output_dir"])
    results_dir.mkdir(parents=True, exist_ok=True)

    n_models = len(config["models"])
    n_tasks = 1 if args.pilot else len(config["tasks"])
    n_conds = len(config["conditions"])
    cells_total = n_models * n_tasks * n_conds * 4
    state_path = Path(config["experiment"]["state_file"])
    state = State(state_path, cells_total)

    print(f"Phase 2L starting: {n_models} models x {n_tasks} tasks x {n_conds} conditions")
    print(f"State: {state_path}")
    print(f"Results: {results_dir}")
    print(f"Budget: ${config['experiment']['total_budget_usd']}, per-provider cap: ${config['experiment']['spend_cap_per_provider_usd']}")
    if args.pilot:
        print(f"PILOT MODE: only task {args.pilot}")
    if args.budget_cap:
        print(f"BUDGET HARD CAP: ${args.budget_cap}")

    def check_phase_success_before_next(phase_n: int, min_rate: float = 0.7) -> bool:
        ok, total = state.phase_success_rate(phase_n)
        if total == 0:
            return True
        rate = ok / total
        if rate < min_rate:
            print(f"\n  ABORT: Phase {phase_n} success rate {ok}/{total} ({rate:.0%}) < {min_rate:.0%}.")
            return False
        print(f"\n  Phase {phase_n} success rate: {ok}/{total} ({rate:.0%}) - proceeding.")
        return True

    if args.phase in ("1", "all"):
        run_phase1(config, api_key, results_dir, state, args.pilot)
        if args.phase == "all" and not check_phase_success_before_next(1):
            return 1
    if args.phase in ("2", "all"):
        run_phase2(config, results_dir, state, args.pilot)
    if args.phase in ("3", "all"):
        run_phase3(config, api_key, results_dir, state, args.pilot)
        if args.phase == "all" and not check_phase_success_before_next(3):
            return 1
    if args.phase in ("4", "all"):
        run_phase4(config, api_key, results_dir, state, args.pilot,
                   workers=args.workers, budget_cap_usd=args.budget_cap)

    print(f"\n{'='*100}")
    print(f"Done. Total spend: ${state.total_cost():.4f}")
    print(f"State saved: {state_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
