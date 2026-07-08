#!/usr/bin/env python3
"""
Archipelago-for-Agents - cross-model orchestration.

Runs the full experimental pipeline defined in PROTOCOL.md and config.yaml.
- Pre-flight checks (API key, model availability, cost estimate)
- 4-phase pipeline per cell: free response -> anonymization -> constructs -> ratings
- Resumable: checkpoints after each phase
- Cost tracking with hard stop
- Detailed logging
- Dry-run mode for validation without API spend

Run:
    python run_experiment.py                       # full run
    python run_experiment.py --dry-run             # validate config, no API calls
    python run_experiment.py --resume              # resume from last checkpoint
    python run_experiment.py --cell A_N_run1       # run only this cell

Requires OPENROUTER_API_KEY in environment.
"""
from __future__ import annotations
import argparse
import json
import os
import random
import re
import sys
import time
import traceback
from dataclasses import dataclass, field, asdict
from datetime import datetime
from itertools import combinations
from pathlib import Path
from typing import Any

try:
    import yaml
    import requests
except ImportError as exc:
    print(f"Missing dependency: {exc.name}. Run: pip install -r requirements.txt")
    sys.exit(1)


# ============================================================
# Logging
# ============================================================
class Logger:
    def __init__(self, log_dir: Path):
        log_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = log_dir / f"run_{ts}.log"

    def _write(self, level: str, msg: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {level}: {msg}"
        print(line)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def info(self, msg: str) -> None: self._write("INFO", msg)
    def warn(self, msg: str) -> None: self._write("WARN", msg)
    def error(self, msg: str) -> None: self._write("ERR ", msg)
    def debug(self, msg: str) -> None: self._write("DBG ", msg)


# ============================================================
# State and checkpoint
# ============================================================
@dataclass
class CellResult:
    cell_id: str
    task: str
    condition: str
    run_idx: int
    status: str = "pending"                  # pending | running | complete | failed
    started_at: str = ""                     # ISO timestamp when cell run began
    completed_at: str = ""                   # ISO timestamp when cell run finished
    random_seed: int = 0                     # seed for triad assignment and element shuffle
    free_responses: dict = field(default_factory=dict)   # {short_name: text}
    element_mapping: dict = field(default_factory=dict)  # {En: short_name}
    element_summaries: dict = field(default_factory=dict)  # {En: summary}
    triad_assignments: dict = field(default_factory=dict)  # {short_name: [[E1,E2,E3], ...]}
    constructs: dict = field(default_factory=dict)         # {short_name: [{...}, ...]}
    constructs_raw: dict = field(default_factory=dict)     # {short_name: {raw_content, n_parsed, n_expected, finish_reason}}
    ratings: dict = field(default_factory=dict)            # {short_name: {construct_id: {En: rating}}}
    # Per-call audit trail (one entry per API call across all phases)
    api_calls: list = field(default_factory=list)
    # Per-model cost/token breakdown for analysis
    per_model_cost: dict = field(default_factory=dict)   # {short_name: float}
    per_model_tokens: dict = field(default_factory=dict) # {short_name: {prompt, completion}}
    cost_usd: float = 0.0
    tokens_in: int = 0
    tokens_out: int = 0
    errors: list = field(default_factory=list)


class State:
    """Tracks all cells, costs, and checkpoint persistence."""

    def __init__(self, state_file: Path):
        self.state_file = state_file
        self.cells: dict[str, CellResult] = {}
        self.total_cost_usd: float = 0.0
        self.started_at: str = ""

    def save(self) -> None:
        """Atomic write with fsync and verification.

        Previous version silently corrupted state.json on Windows when
        Defender/antivirus locked the file during rename. Now we:
        1. Write to .tmp with explicit fsync
        2. Atomic rename
        3. Read back and verify JSON parses
        4. Raise if verification fails (don't pretend success)
        """
        import os as _os
        data = {
            "started_at": self.started_at,
            "total_cost_usd": self.total_cost_usd,
            "cells": {cid: asdict(c) for cid, c in self.cells.items()},
        }
        tmp = self.state_file.with_suffix(".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.flush()
            _os.fsync(f.fileno())
        tmp.replace(self.state_file)
        # Verify the file was actually written correctly
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                json.load(f)
        except (json.JSONDecodeError, OSError) as exc:
            raise RuntimeError(
                f"state.json write verification FAILED: {exc}. "
                f"File at {self.state_file} is corrupted - aborting to prevent data loss."
            )

    def load(self) -> bool:
        if not self.state_file.exists():
            return False
        with open(self.state_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.started_at = data.get("started_at", "")
        self.total_cost_usd = data.get("total_cost_usd", 0.0)
        for cid, cdata in data.get("cells", {}).items():
            self.cells[cid] = CellResult(**cdata)
        return True


# ============================================================
# OpenRouter API client with retry and cost tracking
# ============================================================
class OpenRouterClient:
    def __init__(self, api_key: str, config: dict, logger: Logger):
        self.api_key = api_key
        self.base_url = config["openrouter"]["base_url"]
        self.retries = config["openrouter"]["retries_per_call"]
        self.backoff = config["openrouter"]["retry_backoff_seconds"]
        self.timeout = config["openrouter"]["request_timeout_seconds"]
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://archplg.co.uk",
            "X-Title": "Archipelago-for-Agents experiment",
        })

    def list_models(self) -> dict[str, dict]:
        """Return mapping of model_id -> metadata (pricing, context length, etc.)."""
        r = self.session.get(f"{self.base_url}/models", timeout=self.timeout)
        r.raise_for_status()
        data = r.json().get("data", [])
        return {m["id"]: m for m in data}

    def chat(
        self,
        model_id: str,
        fallback_id: str | None,
        messages: list[dict],
        temperature: float,
        max_tokens: int,
    ) -> dict:
        """
        Return rich result dict for reproducibility logging:
        {
            "content": str,             # the text response
            "usage": dict,              # prompt_tokens, completion_tokens
            "model_id_used": str,       # which model actually responded
            "model_id_requested": str,  # the primary requested
            "used_fallback": bool,
            "attempts": int,            # how many attempts before success
            "latency_ms": int,
            "timestamp_iso": str,
            "raw_response_json": dict,  # full API response for audit
            "request_payload": dict,    # what we sent (without auth)
        }
        Raises RuntimeError if all attempts fail.
        """
        timestamp_iso = datetime.now().isoformat()
        attempt_total = 0
        last_error = None
        for model_to_try in [model_id, fallback_id] if fallback_id else [model_id]:
            if model_to_try is None:
                continue
            for attempt in range(self.retries):
                attempt_total += 1
                payload = {
                    "model": model_to_try,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }
                start = time.monotonic()
                try:
                    r = self.session.post(
                        f"{self.base_url}/chat/completions",
                        json=payload,
                        timeout=self.timeout,
                    )
                    latency_ms = int((time.monotonic() - start) * 1000)
                    if r.status_code == 429:
                        wait = self.backoff[min(attempt, len(self.backoff) - 1)]
                        self.logger.warn(f"Rate limit on {model_to_try}, wait {wait}s")
                        time.sleep(wait)
                        last_error = f"HTTP 429 after {latency_ms}ms"
                        continue
                    if r.status_code >= 400:
                        self.logger.warn(
                            f"{model_to_try} HTTP {r.status_code}: {r.text[:300]}"
                        )
                        last_error = f"HTTP {r.status_code}: {r.text[:300]}"
                        if attempt < self.retries - 1:
                            time.sleep(self.backoff[attempt])
                            continue
                        break
                    data = r.json()
                    content = data["choices"][0]["message"]["content"]
                    usage = data.get("usage", {})
                    # Some models return None/empty content (content filter, safety
                    # block, or empty completion). Treat as retryable error so we
                    # try again rather than corrupting downstream phases.
                    if content is None or (isinstance(content, str) and not content.strip()):
                        try:
                            finish_reason = data.get("choices", [{}])[0].get("finish_reason", "?")
                        except (IndexError, AttributeError, TypeError):
                            finish_reason = "?"
                        self.logger.warn(
                            f"{model_to_try} returned empty/None content "
                            f"(finish_reason={finish_reason}); treating as retryable"
                        )
                        last_error = f"empty content (finish_reason={finish_reason})"
                        if attempt < self.retries - 1:
                            time.sleep(self.backoff[attempt])
                            continue
                        break
                    return {
                        "content": content,
                        "usage": usage,
                        "model_id_used": model_to_try,
                        "model_id_requested": model_id,
                        "used_fallback": model_to_try != model_id,
                        "attempts": attempt_total,
                        "latency_ms": latency_ms,
                        "timestamp_iso": timestamp_iso,
                        "raw_response_json": data,
                        "request_payload": payload,
                    }
                except (requests.RequestException, KeyError) as exc:
                    latency_ms = int((time.monotonic() - start) * 1000)
                    last_error = f"{type(exc).__name__}: {exc}"
                    self.logger.warn(
                        f"{model_to_try} attempt {attempt+1} error: {exc}"
                    )
                    if attempt < self.retries - 1:
                        time.sleep(self.backoff[attempt])
            self.logger.warn(f"Primary {model_to_try} exhausted, trying fallback")
        raise RuntimeError(f"All attempts failed for {model_id}; last error: {last_error}")


# ============================================================
# Cost calculation
# ============================================================
def calculate_cost(usage: dict, model_meta: dict, model_id_for_log: str = "?") -> float:
    """Return USD cost for an OpenRouter chat completion.

    Order of preference (corrected 29.05.2026 after Phase 2J cost-tracking bug):
      1) usage.cost - precomputed by OpenRouter, ALREADY accounts for reasoning
         tokens, cached tokens, audio tokens, and any pricing tier the provider
         actually applied. This is the source of truth.
      2) usage.cost_details.upstream_inference_cost - fallback if usage.cost
         is absent but the breakdown is present.
      3) manual calculation from /models catalog pricing - last resort, used
         only when the API response doesn't return cost (e.g. degraded provider
         or older API version). May undercount reasoning tokens.

    Before 29.05.2026, step 3 was the ONLY path. That undercounted reasoning
    tokens for thinking models (DeepSeek, Kimi, Gemini, GPT-5.5) and recorded
    $0 for any model whose slug was an alias not present in /models catalog
    (e.g. dated-version alias `anthropic/claude-4.8-opus-20260528`).
    """
    import logging

    # Step 1: prefer OpenRouter's own cost field
    if isinstance(usage, dict):
        api_cost = usage.get("cost")
        if api_cost is not None:
            try:
                return float(api_cost)
            except (TypeError, ValueError):
                pass
        # Step 2: cost_details breakdown
        cd = usage.get("cost_details") or {}
        upstream = cd.get("upstream_inference_cost")
        if upstream is not None:
            try:
                return float(upstream)
            except (TypeError, ValueError):
                pass

    # Step 3: manual calculation from catalog
    pricing = model_meta.get("pricing", {}) if isinstance(model_meta, dict) else {}
    prompt_price = float(pricing.get("prompt", "0") or "0")
    completion_price = float(pricing.get("completion", "0") or "0")
    pt = usage.get("prompt_tokens", 0) if isinstance(usage, dict) else 0
    ct = usage.get("completion_tokens", 0) if isinstance(usage, dict) else 0

    # Defensive: warn loudly if we fall through to manual and pricing is empty
    if (prompt_price == 0 and completion_price == 0) and (pt > 0 or ct > 0):
        logging.warning(
            f"[COST-TRACK] model_id='{model_id_for_log}': no usage.cost from API "
            f"AND no pricing in catalog, but {pt}+{ct} tokens used. "
            f"Recording cost=$0.00 - real cost likely NON-zero. "
            f"Hint: use canonical slug not dated-version alias."
        )

    return pt * prompt_price + ct * completion_price


def record_api_call(
    cell: CellResult,
    phase: str,
    short_name: str,
    persona_or_neutral: str,
    sys_prompt: str,
    user_prompt: str,
    api_result: dict,
    cost: float,
    parsed_summary: str,
    config: dict,
) -> None:
    """
    Persist a single API call to disk for reproducibility and pejabat audit.
    Each call writes a complete JSON to logs/api_calls/<cell>/<phase>_<model>_<n>.json
    AND appends a compact record to cell.api_calls (in-memory + state.json).
    """
    audit_dir = Path(config["experiment"]["log_dir"]) / "api_calls" / cell.cell_id
    audit_dir.mkdir(parents=True, exist_ok=True)
    # Number this call's file (so retries do not overwrite)
    existing = list(audit_dir.glob(f"{phase}_{short_name}_*.json"))
    n = len(existing) + 1
    audit_file = audit_dir / f"{phase}_{short_name}_{n:02d}.json"

    full_record = {
        "cell_id": cell.cell_id,
        "task": cell.task,
        "condition": cell.condition,
        "run_idx": cell.run_idx,
        "phase": phase,
        "model_short_name": short_name,
        "persona_or_neutral": persona_or_neutral,
        "system_prompt": sys_prompt,
        "user_prompt": user_prompt,
        "model_id_requested": api_result["model_id_requested"],
        "model_id_used": api_result["model_id_used"],
        "used_fallback": api_result["used_fallback"],
        "attempts": api_result["attempts"],
        "latency_ms": api_result["latency_ms"],
        "timestamp_iso": api_result["timestamp_iso"],
        "raw_response_content": api_result["content"],
        "raw_response_full": api_result["raw_response_json"],
        "usage": api_result["usage"],
        "finish_reason": _extract_finish_reason(api_result),
        "tokens_reasoning": _extract_reasoning_tokens(api_result),
        "cost_usd": cost,
        "parsed_summary": parsed_summary,
        "request_payload": api_result["request_payload"],
    }
    with open(audit_file, "w", encoding="utf-8") as f:
        json.dump(full_record, f, indent=2, ensure_ascii=False)

    # Compact version into cell.api_calls (everything except full raw payloads)
    cell.api_calls.append({
        "phase": phase,
        "model_short_name": short_name,
        "persona_or_neutral": persona_or_neutral,
        "model_id_used": api_result["model_id_used"],
        "used_fallback": api_result["used_fallback"],
        "attempts": api_result["attempts"],
        "latency_ms": api_result["latency_ms"],
        "timestamp_iso": api_result["timestamp_iso"],
        "prompt_tokens": api_result["usage"].get("prompt_tokens", 0),
        "completion_tokens": api_result["usage"].get("completion_tokens", 0),
        "reasoning_tokens": _extract_reasoning_tokens(api_result),
        "finish_reason": _extract_finish_reason(api_result),
        "cost_usd": cost,
        "audit_file": str(audit_file.relative_to(Path(config["experiment"]["log_dir"]).parent)),
    })


def _extract_finish_reason(api_result: dict) -> str:
    """Pull finish_reason from raw response. Returns '?' if unavailable."""
    try:
        choices = api_result.get("raw_response_json", {}).get("choices", [])
        if choices and isinstance(choices[0], dict):
            return choices[0].get("finish_reason") or choices[0].get("native_finish_reason") or "?"
    except (AttributeError, TypeError, IndexError):
        pass
    return "?"


def _extract_reasoning_tokens(api_result: dict) -> int:
    """Pull reasoning_tokens (thinking-model internal tokens) from usage.
    OpenRouter exposes this in usage.completion_tokens_details.reasoning_tokens
    OR as a top-level reasoning_tokens field, depending on the provider."""
    usage = api_result.get("usage", {})
    if not isinstance(usage, dict):
        return 0
    # Most common location
    details = usage.get("completion_tokens_details", {})
    if isinstance(details, dict) and "reasoning_tokens" in details:
        return int(details.get("reasoning_tokens") or 0)
    # Alternative location
    if "reasoning_tokens" in usage:
        return int(usage.get("reasoning_tokens") or 0)
    return 0


# ============================================================
# Persona prompts
# ============================================================
PERSONA_PROMPTS = {
    "Q": (
        "You are an analyst with a quantitative-empiricist epistemological frame. "
        "You prefer measurable evidence and falsifiable claims, and you are skeptical "
        "of frameworks that cannot be operationalized. Your default question is 'what "
        "is the data?'. Your decision heuristic is expected value under uncertainty "
        "with explicit confidence intervals. Generate analysis from this frame."
    ),
    "S": (
        "You are an analyst with a systems-strategist epistemological frame. "
        "You think in feedback loops, second-order effects, and long horizons. "
        "You see the situation as a network of interacting forces, not a set of "
        "options. Your decision heuristic is to identify leverage points and avoid "
        "actions that increase systemic fragility. Generate analysis from this frame."
    ),
    "E": (
        "You are an analyst with a first-principles-engineering epistemological "
        "frame. You reduce to fundamentals. You ask 'what is the actual mechanism?'. "
        "You are suspicious of analogy and prefer efficient, minimal solutions. "
        "Your decision heuristic is to identify the binding constraint, address "
        "it directly, ignore the rest. Generate analysis from this frame."
    ),
    "H": (
        "You are an analyst with a humanist-ethicist epistemological frame. "
        "You center stakeholders, dignity, and distributional consequences. "
        "You see economic framings as incomplete. Your default question is "
        "'who is affected and how?'. Your decision heuristic is to minimize "
        "unjustified harm to vulnerable parties, then optimize. Generate analysis "
        "from this frame."
    ),
    "C": (
        "You are an analyst with a contrarian-skeptic epistemological frame. "
        "You identify hidden assumptions and ask 'what if everyone is wrong?'. "
        "You are a devil's advocate by construction. Your decision heuristic is "
        "to prefer reversible moves and to trust the contrarian signal in "
        "unanimous consensus. Generate analysis from this frame."
    ),
}

NEUTRAL_PROMPT = (
    "You are an analyst. Read the brief carefully and provide your best-reasoned "
    "recommendation."
)


# ============================================================
# Triad assignment - balanced across agents
# ============================================================
def assign_triads(n_agents: int, n_elements: int, n_triads_per_agent: int, seed: int) -> list[list[tuple[int, ...]]]:
    """
    Return list of length n_agents; each element is a list of n_triads_per_agent
    triads. A triad is a tuple of 3 element indices (0..n_elements-1).
    Tries to spread triads across all C(n_elements, 3) combinations.
    """
    rng = random.Random(seed)
    all_triads = list(combinations(range(n_elements), 3))
    # Repeat list to have enough triads
    needed = n_agents * n_triads_per_agent
    pool = list(all_triads) * ((needed // len(all_triads)) + 1)
    rng.shuffle(pool)
    assignments = []
    for i in range(n_agents):
        agent_triads = pool[i * n_triads_per_agent : (i + 1) * n_triads_per_agent]
        assignments.append(agent_triads)
    return assignments


# ============================================================
# Phase implementations
# ============================================================
def load_task_brief(task_id: str, config: dict) -> str:
    for t in config["tasks"]:
        if t["id"] == task_id:
            with open(t["brief_file"], "r", encoding="utf-8") as f:
                return f.read()
    raise KeyError(f"Task {task_id} not found in config")


def get_system_prompt(model_short_name: str, task_id: str, condition_cfg: dict) -> str:
    if not condition_cfg["use_personas"]:
        return condition_cfg["system_prompt"]
    persona_id = condition_cfg["persona_assignment"][task_id][model_short_name]
    return PERSONA_PROMPTS[persona_id]


def _persona_id_for(short_name: str, task_id: str, condition_cfg: dict) -> str:
    if not condition_cfg["use_personas"]:
        return "neutral"
    return condition_cfg["persona_assignment"][task_id][short_name]


def phase1_free_response(
    cell: CellResult,
    config: dict,
    client: OpenRouterClient,
    model_meta: dict[str, dict],
    state: State,
    logger: Logger,
) -> None:
    """Each model generates a free-form recommendation."""
    logger.info(f"[{cell.cell_id}] Phase 1: free response")
    task_brief = load_task_brief(cell.task, config)
    condition_cfg = next(c for c in config["conditions"] if c["id"] == cell.condition)
    params = config["parameters"]["free_response"]

    for model in config["models"]:
        sn = model["short_name"]
        # Validate existing entry: skip only if it's a non-empty string.
        # Previous runs may have stored None (thinking-models burning all
        # tokens on reasoning) or empty strings - we must NOT skip those,
        # otherwise the cell stays broken forever.
        existing = cell.free_responses.get(sn)
        if isinstance(existing, str) and existing.strip():
            continue
        if sn in cell.free_responses:
            logger.warn(f"  {sn}: prior entry invalid ({type(existing).__name__}, "
                        f"{'empty' if not existing else len(existing)} chars); re-calling")
            # Clear stale invalid entry so we don't accumulate errors
            cell.free_responses.pop(sn, None)
        sys_prompt = get_system_prompt(sn, cell.task, condition_cfg)
        user_msg = (
            f"{task_brief}\n\n"
            "Provide your recommendation in 200-400 words. Advocate for a "
            "specific position; do not enumerate all options."
        )
        try:
            res = client.chat(
                model_id=model["id"],
                fallback_id=model.get("fallback_id"),
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_msg},
                ],
                temperature=params["temperature"],
                max_tokens=params["max_tokens"],
            )
            # Validate content before storing - some models can return None
            # (content filter, safety block, empty completion, etc.). Storing None
            # would crash phase2_anonymize on re.split. Raise to skip this model.
            content = res.get("content")
            if not isinstance(content, str) or not content.strip():
                try:
                    finish_reason = res.get("raw_response_json", {}).get(
                        "choices", [{}])[0].get("finish_reason", "?")
                except (IndexError, AttributeError, TypeError):
                    finish_reason = "?"
                raise ValueError(
                    f"empty/None content (got {type(content).__name__}, "
                    f"finish_reason={finish_reason})"
                )
            cell.free_responses[sn] = content
            cost = calculate_cost(res["usage"], model_meta.get(res["model_id_used"], {}))
            cell.cost_usd += cost
            cell.tokens_in += res["usage"].get("prompt_tokens", 0)
            cell.tokens_out += res["usage"].get("completion_tokens", 0)
            cell.per_model_cost[sn] = cell.per_model_cost.get(sn, 0.0) + cost
            pmt = cell.per_model_tokens.setdefault(sn, {"prompt": 0, "completion": 0})
            pmt["prompt"] += res["usage"].get("prompt_tokens", 0)
            pmt["completion"] += res["usage"].get("completion_tokens", 0)
            state.total_cost_usd += cost
            record_api_call(
                cell, "phase1_freeresponse", sn,
                _persona_id_for(sn, cell.task, condition_cfg),
                sys_prompt, user_msg, res, cost,
                parsed_summary=f"free_response captured ({len(content)} chars)",
                config=config,
            )
            fr = _extract_finish_reason(res)
            rt = _extract_reasoning_tokens(res)
            logger.info(
                f"  {sn} ({res['model_id_used']}{'/FB' if res['used_fallback'] else ''}) "
                f"ok, {res['latency_ms']}ms, ${cost:.4f}, "
                f"finish={fr}, reasoning_toks={rt}, out_toks={res['usage'].get('completion_tokens', 0)}"
            )
            state.save()
        except Exception as exc:
            cell.errors.append(f"phase1 {sn}: {exc}")
            logger.error(f"  {sn}: {exc}")
            state.save()


def phase2_anonymize(cell: CellResult, logger: Logger) -> None:
    """Shuffle responses, label E1-EN, generate summaries.
    Defensively filters out any None/empty responses that may have slipped
    through phase1 (older runs without the validation patch).

    NOTE: previously, a partial-crash in this function left element_mapping
    populated but element_summaries incomplete. The next run would short-circuit
    on `if cell.element_mapping: return` and leave the cell broken.
    Now we re-do phase 2 fully if summaries don't match mapping."""
    if cell.element_mapping and len(cell.element_summaries) == len(cell.element_mapping):
        return
    if cell.element_mapping:
        logger.warn(
            f"  Phase 2 was previously incomplete "
            f"({len(cell.element_summaries)}/{len(cell.element_mapping)} summaries). "
            f"Redoing phase 2 from scratch."
        )
        cell.element_mapping = {}
        cell.element_summaries = {}
    logger.info(f"[{cell.cell_id}] Phase 2: anonymize")
    # Defensive: drop any non-string or empty entries
    valid = {sn: text for sn, text in cell.free_responses.items()
             if isinstance(text, str) and text.strip()}
    skipped = [sn for sn in cell.free_responses if sn not in valid]
    if skipped:
        logger.warn(f"  Skipping models with empty/None content: {skipped}")
        cell.errors.append(f"phase2 dropped empty responses from: {skipped}")
        cell.free_responses = valid
    if not valid:
        logger.error(f"  No valid responses to anonymize; aborting phase2")
        cell.errors.append("phase2: no valid responses (all models returned None/empty)")
        return
    short_names = list(valid.keys())
    rng = random.Random(hash(cell.cell_id) % (2 ** 32))
    rng.shuffle(short_names)
    cell.element_mapping = {f"E{i+1}": sn for i, sn in enumerate(short_names)}
    # Generate short summaries (first 3 sentences of each response)
    for ek, sn in cell.element_mapping.items():
        text = cell.free_responses[sn]
        sentences = re.split(r"(?<=[.!?])\s+", text)
        summary = " ".join(sentences[:3]).strip()
        if len(summary) > 600:
            summary = summary[:600] + "..."
        cell.element_summaries[ek] = summary


def _parse_constructs(text: str, expected_count: int) -> list[dict]:
    """Parse model output for triadic constructs.

    Accepts multiple formats:
      1. 'Triad N:' header + 'Left pole:' / 'Right pole:' (canonical)
      2. Markdown bold variants: **Triad N**, **Left pole:**, **Right pole:**
      3. Headers like '## Triad N' or '### Triad N: ...'
      4. 'pole 1' / 'pole 2' or 'pole A' / 'pole B'
      5. 'X vs Y' / 'X | Y' / 'X / Y' on a numbered line (fallback)
    """
    constructs = []
    # Strip markdown bold markers globally so they don't break regex
    cleaned = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)
    # Split into per-triad blocks. Accept Triad/TRIAD/## with optional bold/colon/number
    blocks = re.split(
        r"\n\s*(?:#{1,3}\s*)?(?:Triad|TRIAD|##)\s*\d+[:\.\s\-]",
        "\n" + cleaned,
    )
    for block in blocks[1:]:
        # Canonical: Left pole / Right pole
        left_match = re.search(
            r"(?:[Ll]eft[ \-_]?[Pp]ole|[Pp]ole\s*[1A]|[Ll]eft)\s*[:\-]\s*(.+)",
            block,
        )
        right_match = re.search(
            r"(?:[Rr]ight[ \-_]?[Pp]ole|[Pp]ole\s*[2B]|[Rr]ight)\s*[:\-]\s*(.+)",
            block,
        )
        if left_match and right_match:
            left = left_match.group(1).strip().split("\n")[0].strip(" .,*")
            right = right_match.group(1).strip().split("\n")[0].strip(" .,*")
            if left and right and left != right:
                constructs.append({"left": left, "right": right})
    if len(constructs) >= expected_count:
        return constructs[:expected_count]
    # Fallback 1: 'X vs Y' / 'X | Y' / 'X / Y' on a numbered or bullet line
    if len(constructs) < expected_count:
        for line in cleaned.split("\n"):
            m = re.search(
                r"^\s*(?:[-*•]|\d+[\.\)])?\s*(.+?)\s*(?:↔|<->|<>|\|\||\bvs\.?\b|/)\s*(.+)$",
                line,
                re.IGNORECASE,
            )
            if m:
                left = m.group(1).strip(" .,*")
                right = m.group(2).strip(" .,*")
                # filter out obviously bogus matches
                if 3 <= len(left) <= 140 and 3 <= len(right) <= 140:
                    # avoid duplicates already captured
                    if not any(c["left"] == left and c["right"] == right for c in constructs):
                        constructs.append({"left": left, "right": right})
    return constructs[:expected_count]


def phase3_constructs(
    cell: CellResult,
    config: dict,
    client: OpenRouterClient,
    model_meta: dict[str, dict],
    state: State,
    logger: Logger,
) -> None:
    """Each model produces N constructs via triadic elicitation."""
    logger.info(f"[{cell.cell_id}] Phase 3: triadic construct elicitation")
    n_triads = config["pipeline"]["n_triads_per_agent"]
    # Use actual element count (may be less than configured if some models
    # returned None in phase1 and were filtered out in phase2)
    actual_n_elements = len(cell.element_summaries)
    configured_n_elements = config["pipeline"]["n_elements"]
    if actual_n_elements < configured_n_elements:
        logger.warn(
            f"  Only {actual_n_elements} elements (config wants {configured_n_elements}); "
            f"adapting triad assignment to actual count"
        )
    if actual_n_elements < 3:
        logger.error(f"  Need >=3 elements for triadic elicitation, have {actual_n_elements}. Skipping phase 3.")
        cell.errors.append(f"phase3 skipped: only {actual_n_elements} elements available")
        return
    n_elements = actual_n_elements
    seed = hash(cell.cell_id) % (2 ** 32)
    triad_assignments = assign_triads(
        n_agents=len(config["models"]),
        n_elements=n_elements,
        n_triads_per_agent=n_triads,
        seed=seed,
    )
    params = config["parameters"]["constructs"]

    condition_cfg = next(c for c in config["conditions"] if c["id"] == cell.condition)
    elements_block = "\n\n".join(
        f"**{ek}:** {cell.element_summaries[ek]}"
        for ek in sorted(cell.element_summaries.keys())
    )

    for i, model in enumerate(config["models"]):
        sn = model["short_name"]
        # Validate existing entry: must have n_triads items each with non-empty poles.
        existing = cell.constructs.get(sn, [])
        valid_existing = [
            c for c in existing
            if isinstance(c, dict)
            and isinstance(c.get("left"), str) and c["left"].strip()
            and isinstance(c.get("right"), str) and c["right"].strip()
        ]
        if len(valid_existing) >= n_triads:
            continue
        if sn in cell.constructs:
            logger.warn(f"  {sn}: prior constructs invalid ({len(valid_existing)}/{n_triads} valid); re-calling")
            cell.constructs.pop(sn, None)
        sys_prompt = get_system_prompt(sn, cell.task, condition_cfg)
        my_triads = triad_assignments[i]
        cell.triad_assignments[sn] = [
            [f"E{idx+1}" for idx in triad] for triad in my_triads
        ]
        triad_list_text = "\n".join(
            f"Triad {ti+1}: {', '.join(f'E{idx+1}' for idx in triad)}"
            for ti, triad in enumerate(my_triads)
        )
        user_msg = (
            f"You are presented with {n_elements} anonymous responses to the same brief. "
            f"They are labeled E1 through E{n_elements}.\n\n"
            f"{elements_block}\n\n"
            f"Your task: for each of the following triads of 3 responses, "
            f"identify a single bipolar construct that distinguishes them. "
            f"Specifically, identify how TWO of the three are similar to each "
            f"other in a way that distinguishes them from the THIRD. Name the "
            f"two poles of that dimension.\n\n"
            f"Triads to analyze:\n{triad_list_text}\n\n"
            f"For each triad, output EXACTLY this format with no markdown, "
            f"no bold, no bullets, no numbered lists:\n"
            f"Triad 1:\nLeft pole: <short phrase, max 12 words>\nRight pole: <short phrase, max 12 words>\n\n"
            f"Triad 2:\nLeft pole: <short phrase, max 12 words>\nRight pole: <short phrase, max 12 words>\n\n"
            f"Triad 3:\nLeft pole: <short phrase, max 12 words>\nRight pole: <short phrase, max 12 words>\n\n"
            f"Be specific. Avoid generic dichotomies like 'good vs bad'. "
            f"Use plain text labels (Triad N, Left pole, Right pole) without any markdown formatting."
        )
        try:
            res = client.chat(
                model_id=model["id"],
                fallback_id=model.get("fallback_id"),
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_msg},
                ],
                temperature=params["temperature"],
                max_tokens=params["max_tokens"],
            )
            content = res["content"]
            parsed = _parse_constructs(content, n_triads)
            if len(parsed) < n_triads:
                cell.errors.append(
                    f"phase3 {sn}: parsed only {len(parsed)} constructs from output"
                )
                logger.warn(f"  {sn}: parsed {len(parsed)}/{n_triads} - keeping what we got")
            cell.constructs[sn] = [
                {"id": f"C_{sn}_{j+1}", "left": c["left"], "right": c["right"],
                 "triad": cell.triad_assignments[sn][j] if j < len(cell.triad_assignments[sn]) else None,
                 "raw_output_excerpt": content[:200]}
                for j, c in enumerate(parsed)
            ]
            # Save raw response separately for debugging parser failures
            cell.constructs_raw[sn] = {
                "n_parsed": len(parsed),
                "n_expected": n_triads,
                "raw_content": content[:2500] if content else "",
                "finish_reason": res.get("finish_reason", "unknown"),
            }
            cost = calculate_cost(res["usage"], model_meta.get(res["model_id_used"], {}))
            cell.cost_usd += cost
            cell.tokens_in += res["usage"].get("prompt_tokens", 0)
            cell.tokens_out += res["usage"].get("completion_tokens", 0)
            cell.per_model_cost[sn] = cell.per_model_cost.get(sn, 0.0) + cost
            pmt = cell.per_model_tokens.setdefault(sn, {"prompt": 0, "completion": 0})
            pmt["prompt"] += res["usage"].get("prompt_tokens", 0)
            pmt["completion"] += res["usage"].get("completion_tokens", 0)
            state.total_cost_usd += cost
            record_api_call(
                cell, "phase3_constructs", sn,
                _persona_id_for(sn, cell.task, condition_cfg),
                sys_prompt, user_msg, res, cost,
                parsed_summary=f"parsed {len(parsed)}/{n_triads} constructs",
                config=config,
            )
            fr = _extract_finish_reason(res)
            rt = _extract_reasoning_tokens(res)
            logger.info(
                f"  {sn} ({res['model_id_used']}{'/FB' if res['used_fallback'] else ''}) "
                f"ok, {len(parsed)} constructs, {res['latency_ms']}ms, ${cost:.4f}, "
                f"finish={fr}, reasoning_toks={rt}"
            )
            state.save()
        except Exception as exc:
            cell.errors.append(f"phase3 {sn}: {exc}")
            logger.error(f"  {sn}: {exc}")
            state.save()


def _parse_ratings(text: str, construct_ids: list[str], element_labels: list[str]) -> dict:
    """Extract integer ratings 1-7 from model output. Tolerates various formats."""
    out: dict[str, dict[str, int]] = {}
    for cid in construct_ids:
        out[cid] = {}
    # Look for lines like "C_M1_1, E1: 5" or "C_M1_1 E1=5" or CSV-like
    pattern = re.compile(
        r"(C_[A-Z0-9_]+)\s*[,\s|:]\s*(E[1-9])\s*[=:\-,]\s*([1-7])"
    )
    for match in pattern.finditer(text):
        cid, ek, val = match.group(1), match.group(2), int(match.group(3))
        if cid in out and ek in element_labels:
            out[cid][ek] = val
    # Also try CSV-style table parse: "C_xx,1,5,3,7,2"
    csv_pattern = re.compile(
        r"(C_[A-Z0-9_]+)\s*[,|\t]\s*([1-7])\s*[,|\t]\s*([1-7])\s*[,|\t]\s*([1-7])\s*[,|\t]\s*([1-7])\s*[,|\t]\s*([1-7])"
    )
    for match in csv_pattern.finditer(text):
        cid = match.group(1)
        if cid in out:
            for i, ek in enumerate(element_labels):
                if ek not in out[cid]:
                    out[cid][ek] = int(match.group(i + 2))
    return out


def phase4_ratings(
    cell: CellResult,
    config: dict,
    client: OpenRouterClient,
    model_meta: dict[str, dict],
    state: State,
    logger: Logger,
) -> None:
    """Each model rates all 5 elements on all collected constructs."""
    logger.info(f"[{cell.cell_id}] Phase 4: ratings")
    # Aggregate ALL constructs from all agents
    all_constructs = []
    for sn in sorted(cell.constructs.keys()):
        all_constructs.extend(cell.constructs[sn])
    if not all_constructs:
        logger.warn(f"  no constructs to rate")
        return
    construct_ids = [c["id"] for c in all_constructs]
    element_labels = sorted(cell.element_summaries.keys())
    params = config["parameters"]["ratings"]
    condition_cfg = next(c for c in config["conditions"] if c["id"] == cell.condition)
    elements_block = "\n\n".join(
        f"**{ek}:** {cell.element_summaries[ek]}" for ek in element_labels
    )
    constructs_block = "\n".join(
        f"  {c['id']}: '{c['left']}'  (1) ↔ (7)  '{c['right']}'"
        for c in all_constructs
    )

    for model in config["models"]:
        sn = model["short_name"]
        # Validate existing entry: must have ratings for >=80% of (construct,element) pairs.
        existing = cell.ratings.get(sn, {})
        if isinstance(existing, dict):
            n_existing_pairs = sum(
                len(v) for v in existing.values()
                if isinstance(v, dict)
            )
        else:
            n_existing_pairs = 0
        expected_pairs_total = len(construct_ids) * len(element_labels)
        if n_existing_pairs >= int(0.8 * expected_pairs_total):
            continue
        if sn in cell.ratings:
            logger.warn(f"  {sn}: prior ratings invalid ({n_existing_pairs}/{expected_pairs_total} pairs); re-calling")
            cell.ratings.pop(sn, None)
        sys_prompt = get_system_prompt(sn, cell.task, condition_cfg)
        n_el = len(element_labels)
        labels_range = f"{element_labels[0]}-{element_labels[-1]}" if n_el > 0 else "(none)"
        expected_lines = len(construct_ids) * n_el
        # Concrete examples covering more than the first construct so models
        # can pattern-match across constructs. Keeps the format unambiguous.
        example_lines = "\n".join(
            f"{construct_ids[0]},{ek},{(i % 7) + 1}" for i, ek in enumerate(element_labels[:min(3, n_el)])
        )
        if len(construct_ids) > 1:
            example_lines += f"\n{construct_ids[1]},{element_labels[0]},4"
        user_msg = (
            f"You are presented with {n_el} anonymous responses ({labels_range}) and "
            f"{len(construct_ids)} bipolar constructs. Rate each response on each "
            f"construct on a 1-7 scale: 1 = strongly the LEFT pole, 7 = strongly the "
            f"RIGHT pole, 4 = neutral or mixed.\n\n"
            f"Responses:\n{elements_block}\n\n"
            f"Constructs (id : left pole ↔ right pole):\n{constructs_block}\n\n"
            f"OUTPUT FORMAT (strict). Write exactly {expected_lines} lines, no "
            f"commentary, no markdown fences, no headers. One line per "
            f"(construct, element) pair, in this exact format:\n"
            f"<construct_id>,<element>,<rating>\n\n"
            f"Example (showing the format only - your numbers will differ):\n"
            f"{example_lines}\n...\n\n"
            f"Constraints:\n"
            f"- rating is an integer from 1 to 7\n"
            f"- iterate all {len(construct_ids)} constructs in the order listed, "
            f"and within each construct all {n_el} elements in order ({labels_range})\n"
            f"- produce {expected_lines} lines total\n"
            f"- output ONLY the lines, nothing before or after"
        )
        try:
            res = client.chat(
                model_id=model["id"],
                fallback_id=model.get("fallback_id"),
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": user_msg},
                ],
                temperature=params["temperature"],
                max_tokens=params["max_tokens"],
            )
            content = res["content"]
            parsed = _parse_ratings(content, construct_ids, element_labels)
            cell.ratings[sn] = parsed
            # Count missing
            expected = len(construct_ids) * len(element_labels)
            got = sum(len(v) for v in parsed.values())
            if got < expected:
                cell.errors.append(
                    f"phase4 {sn}: got {got}/{expected} ratings"
                )
                logger.warn(f"  {sn}: parsed {got}/{expected} ratings")
            cost = calculate_cost(res["usage"], model_meta.get(res["model_id_used"], {}))
            cell.cost_usd += cost
            cell.tokens_in += res["usage"].get("prompt_tokens", 0)
            cell.tokens_out += res["usage"].get("completion_tokens", 0)
            cell.per_model_cost[sn] = cell.per_model_cost.get(sn, 0.0) + cost
            pmt = cell.per_model_tokens.setdefault(sn, {"prompt": 0, "completion": 0})
            pmt["prompt"] += res["usage"].get("prompt_tokens", 0)
            pmt["completion"] += res["usage"].get("completion_tokens", 0)
            state.total_cost_usd += cost
            record_api_call(
                cell, "phase4_ratings", sn,
                _persona_id_for(sn, cell.task, condition_cfg),
                sys_prompt, user_msg, res, cost,
                parsed_summary=f"parsed {got}/{expected} ratings",
                config=config,
            )
            fr = _extract_finish_reason(res)
            rt = _extract_reasoning_tokens(res)
            logger.info(
                f"  {sn} ({res['model_id_used']}{'/FB' if res['used_fallback'] else ''}) "
                f"ok, {got}/{expected} ratings, {res['latency_ms']}ms, ${cost:.4f}, "
                f"finish={fr}, reasoning_toks={rt}"
            )
            state.save()
        except Exception as exc:
            cell.errors.append(f"phase4 {sn}: {exc}")
            logger.error(f"  {sn}: {exc}")
            state.save()


# ============================================================
# Cells: enumerate all (task, condition, run_idx) cells per protocol
# ============================================================
def enumerate_cells(config: dict) -> list[tuple[str, str, int]]:
    cells = []
    for task in config["tasks"]:
        for cond in config["conditions"]:
            cells.append((task["id"], cond["id"], 1))
        if task.get("is_repeat_task"):
            extra = config["repetitions"]["extra_runs_for_repeat_task"]
            for cond in config["conditions"]:
                for k in range(2, 2 + extra):
                    cells.append((task["id"], cond["id"], k))
    return cells


def cell_id(task: str, cond: str, run_idx: int) -> str:
    return f"{task}_{cond}_run{run_idx}"


# ============================================================
# Pre-flight
# ============================================================
def preflight(config: dict, client: OpenRouterClient, logger: Logger) -> dict[str, dict]:
    logger.info("Pre-flight checks")
    pf = config["preflight"]
    model_meta: dict[str, dict] = {}
    if pf["verify_model_ids"]:
        try:
            available = client.list_models()
        except Exception as exc:
            logger.error(f"Cannot reach OpenRouter: {exc}")
            raise
        logger.info(f"  {len(available)} models available on OpenRouter")
        for m in config["models"]:
            for mid in [m["id"], m.get("fallback_id")]:
                if mid and mid in available:
                    model_meta[mid] = available[mid]
                elif mid:
                    logger.warn(f"  {mid} NOT FOUND in OpenRouter catalog")
        for m in config["models"]:
            if m["id"] not in model_meta and m.get("fallback_id") not in model_meta:
                raise RuntimeError(
                    f"Both primary ({m['id']}) and fallback ({m.get('fallback_id')}) "
                    f"unavailable. Update config.yaml."
                )
    if pf["estimate_cost"]:
        cells = enumerate_cells(config)
        n_trials = len(cells) * len(config["models"])
        # Heuristic per trial: ~10K input + 1.5K output (worst case)
        avg_in = 10000
        avg_out = 1500
        total_cost = 0.0
        for m in config["models"]:
            mid = m["id"] if m["id"] in model_meta else m.get("fallback_id")
            if mid and mid in model_meta:
                pr = model_meta[mid].get("pricing", {})
                p_in = float(pr.get("prompt", "0") or "0")
                p_out = float(pr.get("completion", "0") or "0")
                # 3 phases per trial
                trial_cost = (avg_in * p_in + avg_out * p_out) * 3
                total_cost += trial_cost * len(cells)
                logger.info(
                    f"  {m['short_name']} ({mid}): "
                    f"${p_in*1e6:.2f}/M in, ${p_out*1e6:.2f}/M out, "
                    f"est ${trial_cost*len(cells):.2f} total"
                )
        logger.info(f"  {len(cells)} cells x {len(config['models'])} models = {n_trials} trials")
        logger.info(f"  Estimated total cost: ${total_cost:.2f}")
        logger.info(f"  Hard cap: ${config['experiment']['total_budget_usd']}")
        if total_cost > config["experiment"]["total_budget_usd"]:
            logger.error("Estimated cost exceeds hard cap.")
            raise RuntimeError("Cost cap exceeded in estimate. Aborting.")
    return model_meta


# ============================================================
# Main run loop
# ============================================================
def run_cell(
    cell: CellResult,
    config: dict,
    client: OpenRouterClient,
    model_meta: dict[str, dict],
    state: State,
    logger: Logger,
) -> None:
    cell.status = "running"
    cell.started_at = datetime.now().isoformat()
    # Capture the seed actually used (was computed inline before, now recorded)
    cell.random_seed = hash(cell.cell_id) % (2 ** 32)
    state.save()
    try:
        phase1_free_response(cell, config, client, model_meta, state, logger)
        phase2_anonymize(cell, logger)
        phase3_constructs(cell, config, client, model_meta, state, logger)
        phase4_ratings(cell, config, client, model_meta, state, logger)
        cell.status = "complete" if not cell.errors else "complete_with_errors"
    except Exception as exc:
        logger.error(f"[{cell.cell_id}] cell failed: {exc}")
        logger.error(traceback.format_exc())
        cell.status = "failed"
        cell.errors.append(f"cell-level: {exc}")
    cell.completed_at = datetime.now().isoformat()
    state.save()
    save_cell_artifacts(cell, config)


def save_cell_artifacts(cell: CellResult, config: dict) -> None:
    """INSTRUMENTED VERSION - detailed logging to diagnose Phase 2F corruption.

    Writes to multiple parallel locations (atomic, direct, sidecar) to isolate
    where truncation happens. Logs byte counts at every step to stderr.
    """
    import os as _os
    import sys
    import time
    out_dir = Path(config["experiment"]["output_dir"]) / cell.cell_id
    out_dir.mkdir(parents=True, exist_ok=True)
    final = out_dir / "cell.json"
    tmp = out_dir / "cell.json.tmp"
    backup = out_dir / "cell.json.backup"  # second copy via different code path
    sidecar = out_dir / "cell.json.sidecar.txt"  # raw text

    # Generate JSON string in memory first - we know exactly what we INTEND to write
    data_dict = asdict(cell)
    json_str = json.dumps(data_dict, indent=2, ensure_ascii=False)
    intended_chars = len(json_str)
    intended_utf8_bytes = len(json_str.encode("utf-8"))

    def _log(msg):
        sys.stderr.write(f"[INSTRUMENT {cell.cell_id}] {msg}\n")
        sys.stderr.flush()

    _log(f"START intended_chars={intended_chars} intended_utf8_bytes={intended_utf8_bytes}")

    # Step 1: write to tmp via json.dump (original method)
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data_dict, f, indent=2, ensure_ascii=False)
            f.flush()
            _os.fsync(f.fileno())
        tmp_size = _os.path.getsize(tmp)
        _log(f"AFTER json.dump+fsync tmp_size={tmp_size}")
    except Exception as exc:
        _log(f"EXCEPTION during json.dump: {exc}")
        raise

    # Step 2: atomic rename
    try:
        tmp.replace(final)
        final_size_immediate = _os.path.getsize(final)
        _log(f"AFTER rename final_size={final_size_immediate}")
    except Exception as exc:
        _log(f"EXCEPTION during rename: {exc}")
        raise

    # Step 3: verify by reading back IMMEDIATELY
    try:
        with open(final, "r", encoding="utf-8") as f:
            verify_data = json.load(f)
        _log(f"VERIFY_IMMEDIATE OK json_loaded keys={list(verify_data.keys())[:3]}...")
    except Exception as exc:
        _log(f"VERIFY_IMMEDIATE FAILED: {exc}")
        # Continue anyway to compare with sidecar
        verify_data = None

    # Step 4: write sidecar via DIFFERENT code path (no atomic, no fsync, direct)
    try:
        with open(sidecar, "w", encoding="utf-8") as f:
            f.write(json_str)
        sidecar_size = _os.path.getsize(sidecar)
        _log(f"SIDECAR write done size={sidecar_size}")
    except Exception as exc:
        _log(f"SIDECAR write failed: {exc}")

    # Step 5: write backup via write_text (Path method)
    try:
        backup.write_text(json_str, encoding="utf-8")
        backup_size = _os.path.getsize(backup)
        _log(f"BACKUP write_text done size={backup_size}")
    except Exception as exc:
        _log(f"BACKUP write_text failed: {exc}")

    # Step 6: re-check final file size after delay (catches delayed corruption)
    time.sleep(0.5)
    final_size_delayed = _os.path.getsize(final)
    _log(f"AFTER 0.5s delay final_size={final_size_delayed} (was {final_size_immediate})")
    if final_size_delayed != final_size_immediate:
        _log(f"SIZE CHANGED during 0.5s - external process modifying file!")

    # Step 7: list all files in dir to confirm
    files_in_dir = sorted(_os.listdir(out_dir))
    file_sizes = {f: _os.path.getsize(out_dir / f) for f in files_in_dir}
    _log(f"DIR CONTENTS: {file_sizes}")

    # Step 8: final verification
    try:
        with open(final, "r", encoding="utf-8") as f:
            json.load(f)
        _log(f"FINAL_VERIFY OK")
    except (json.JSONDecodeError, OSError) as exc:
        _log(f"FINAL_VERIFY FAILED: {exc}")
        # Don't raise - we want to see all cells' results
        # raise RuntimeError(
        #     f"cell.json write verification FAILED for {cell.cell_id}: {exc}. "
        # )


def _file_sha256(path: Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def write_run_manifest(config: dict, model_meta: dict, config_path: str) -> None:
    """
    Writes a manifest file with everything needed for reproducibility:
    - script and config SHA-256 hashes
    - model_meta snapshot at run start (prices, context windows)
    - python and package versions
    - all 10 cell IDs to be run
    - timezone and start time
    """
    import platform
    out_dir = Path(config["experiment"]["output_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_file = out_dir / "run_manifest.json"

    script_path = Path(__file__).resolve()
    analyze_path = script_path.parent / "analyze.py"

    # Capture installed package versions for the libraries we depend on
    pkg_versions = {}
    for pkg in ["requests", "yaml", "pandas", "numpy",
                "sklearn", "scipy", "matplotlib", "seaborn"]:
        try:
            mod = __import__(pkg)
            pkg_versions[pkg] = getattr(mod, "__version__", "unknown")
        except Exception:
            pkg_versions[pkg] = "not-installed"

    manifest = {
        "run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "started_at": datetime.now().isoformat(),
        "timezone": time.strftime("%Z"),
        "script_sha256": _file_sha256(script_path),
        "config_sha256": _file_sha256(Path(config_path)),
        "analyze_sha256": _file_sha256(analyze_path) if analyze_path.exists() else None,
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "package_versions": pkg_versions,
        "experiment_name": config["experiment"]["name"],
        "total_budget_usd": config["experiment"]["total_budget_usd"],
        "estimated_budget_usd": config["experiment"]["estimated_budget_usd"],
        "n_models": len(config["models"]),
        "n_tasks": len(config["tasks"]),
        "n_conditions": len(config["conditions"]),
        "cells_planned": [cell_id(t, c, r) for t, c, r in enumerate_cells(config)],
        "models_snapshot": [
            {
                "short_name": m["short_name"],
                "family": m["family"],
                "primary_id": m["id"],
                "fallback_id": m.get("fallback_id"),
                "primary_pricing": model_meta.get(m["id"], {}).get("pricing", {}),
                "primary_context_length": model_meta.get(m["id"], {}).get("context_length"),
            }
            for m in config["models"]
        ],
        "config_full_snapshot": config,
    }
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False, default=str)
    return manifest_file


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--config", default="config.yaml")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--resume", action="store_true")
    p.add_argument("--cell", default=None, help="Run only this cell (id like A_N_run1)")
    args = p.parse_args()

    with open(args.config, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    if args.dry_run:
        config["preflight"]["dry_run_mode"] = True

    logger = Logger(Path(config["experiment"]["log_dir"]))
    logger.info(f"Archipelago cross-model run starting")
    logger.info(f"Config: {args.config}")

    api_key = os.environ.get(config["openrouter"]["api_key_env"])
    if not api_key and not args.dry_run:
        logger.error(
            f"Set {config['openrouter']['api_key_env']} environment variable "
            f"(e.g., in PowerShell: $env:OPENROUTER_API_KEY=\"sk-or-...\")."
        )
        return 2

    client = OpenRouterClient(api_key or "dry-run", config, logger)

    try:
        model_meta = preflight(config, client, logger)
    except Exception as exc:
        logger.error(f"Pre-flight failed: {exc}")
        return 3

    if args.dry_run:
        logger.info("DRY RUN complete - no API spend.")
        return 0

    # No interactive prompt. Safety relies on:
    #   1. The hard budget cap in config.yaml (BUDGET HARD STOP)
    #   2. The wrapper script (reshoot_5cells.ps1 / run_all.ps1) which asks
    #      ONCE before invoking us. Asking again here is just noise.
    #   3. Ctrl+C still works at any time; state.json checkpoints after every call.
    if config["preflight"]["require_user_confirmation"] and not args.cell:
        logger.info(
            f"Starting full run (no interactive prompt). "
            f"Budget hard cap: ${config['experiment']['total_budget_usd']}. "
            f"Press Ctrl+C to abort."
        )

    manifest_file = write_run_manifest(config, model_meta, args.config)
    logger.info(f"Wrote reproducibility manifest: {manifest_file}")

    state_file = Path(config["experiment"]["output_dir"]) / "state.json"
    state_file.parent.mkdir(parents=True, exist_ok=True)
    state = State(state_file)
    if args.resume and state.load():
        logger.info(f"Resumed: total cost so far ${state.total_cost_usd:.2f}")
    else:
        state.started_at = datetime.now().isoformat()

    cells_to_run = enumerate_cells(config)
    if args.cell:
        cells_to_run = [(t, c, r) for (t, c, r) in cells_to_run if cell_id(t, c, r) == args.cell]
        if not cells_to_run:
            logger.error(f"Cell {args.cell} not found. Available:")
            for t, c, r in enumerate_cells(config):
                logger.error(f"  {cell_id(t, c, r)}")
            return 4

    # Wall-clock timing per cell + ETA based on rolling average
    run_start = time.monotonic()
    cell_durations = []
    cells_planned = len(cells_to_run)
    cells_done = 0
    for task, cond, run_idx in cells_to_run:
        cid = cell_id(task, cond, run_idx)
        if cid not in state.cells:
            state.cells[cid] = CellResult(cell_id=cid, task=task, condition=cond, run_idx=run_idx)
        cell = state.cells[cid]
        if cell.status in ("complete", "complete_with_errors") and not args.cell:
            logger.info(f"[{cid}] already complete, skipping")
            cells_done += 1
            continue
        if state.total_cost_usd > config["experiment"]["total_budget_usd"]:
            logger.error(f"BUDGET HARD STOP at ${state.total_cost_usd:.2f}")
            return 5
        cell_t0 = time.monotonic()
        run_cell(cell, config, client, model_meta, state, logger)
        cell_elapsed = time.monotonic() - cell_t0
        cell_durations.append(cell_elapsed)
        cells_done += 1
        total_elapsed = time.monotonic() - run_start
        avg = sum(cell_durations) / len(cell_durations)
        remaining_cells = cells_planned - cells_done
        eta_sec = avg * remaining_cells
        logger.info(
            f"[{cid}] done. cell cost: ${cell.cost_usd:.4f}. "
            f"total: ${state.total_cost_usd:.4f}. "
            f"cell_time: {cell_elapsed/60:.1f}min, "
            f"elapsed: {total_elapsed/60:.1f}min, "
            f"ETA: ~{eta_sec/60:.1f}min ({cells_done}/{cells_planned} cells)"
        )

    total_elapsed = time.monotonic() - run_start
    logger.info(f"All cells processed. Final cost: ${state.total_cost_usd:.4f}, wall time: {total_elapsed/60:.1f}min")
    logger.info(f"Output: {config['experiment']['output_dir']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
