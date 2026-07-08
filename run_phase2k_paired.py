#!/usr/bin/env python3
"""
run_phase2k_paired.py - paired-design replication of the Lab>Persona finding.

Strategy: re-use Phase 2J N cell artifacts (free_responses, element_summaries,
constructs) as FIXED INPUT, then make each model RE-RATE the same elements on
the same constructs under its assigned persona. This produces ratings that are
directly comparable to Phase 2J N ratings (same construct, same element, same
model) - the paired design needed for replicating the 2.3x Lab>Persona ratio
from Phase 1 at scale (n_models=11 instead of 5).

Why not modify run_experiment.py? This script does ONLY Phase 4 (rating). It
skips Phases 1-3 by reusing Phase 2J N cell outputs. Much simpler, much faster,
much cheaper (~$10 vs $15+ for full run).

Output: results_phase2k/<task>_K_run1/cell.json (one cell per task)
        Cell schema matches Phase 2J for downstream compatibility.

Run:
    python run_phase2k_paired.py --config config_phase2k.yaml
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import requests
import yaml


# ============================================================
# Persona prompts (copied from run_experiment.py PERSONA_PROMPTS)
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


def log(level: str, msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {level}: {msg}", flush=True)


def load_phase2j_n_cell(input_dir: Path, task: str):
    """Load the Phase 2J N cell for the given task."""
    p = input_dir / f"{task}_N_run1" / "cell.json"
    if not p.exists():
        log("ERR", f"Phase 2J N cell not found: {p}")
        return None
    return json.loads(p.read_text(encoding="utf-8"))


def build_rating_prompt(cell_data: dict) -> tuple[str, list[str], list[str]]:
    """Construct the rating user_msg from Phase 2J N cell data.
    Returns (user_msg, construct_ids, element_labels) tuple."""
    constructs = cell_data.get("constructs", {})
    all_constructs = []
    for sn in sorted(constructs.keys()):
        all_constructs.extend(constructs[sn])
    construct_ids = [c["id"] for c in all_constructs]
    element_summaries = cell_data.get("element_summaries", {})
    element_labels = sorted(element_summaries.keys())

    elements_block = "\n\n".join(
        f"**{ek}:** {element_summaries[ek]}" for ek in element_labels
    )
    constructs_block = "\n".join(
        f"  {c['id']}: '{c['left']}'  (1) ↔ (7)  '{c['right']}'"
        for c in all_constructs
    )
    n_el = len(element_labels)
    labels_range = f"{element_labels[0]}-{element_labels[-1]}" if n_el > 0 else "(none)"
    expected_lines = len(construct_ids) * n_el
    example_lines = "\n".join(
        f"{construct_ids[0]},{ek},{(i % 7) + 1}"
        for i, ek in enumerate(element_labels[:min(3, n_el)])
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
    return user_msg, construct_ids, element_labels


def parse_ratings(text: str, construct_ids: list[str], element_labels: list[str]) -> dict:
    """Parse `cid,element,rating` lines into nested dict {cid: {element: rating}}."""
    result = {cid: {} for cid in construct_ids}
    if not text:
        return result
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(",")
        if len(parts) < 3:
            continue
        cid = parts[0].strip()
        ek = parts[1].strip()
        try:
            r = int(parts[2].strip())
            if 1 <= r <= 7:
                if cid in result:
                    result[cid][ek] = r
        except (ValueError, IndexError):
            continue
    return result


def call_model(api_key: str, model_id: str, sys_prompt: str, user_msg: str,
               temperature: float, max_tokens: int,
               retries: int = 3, timeout: int = 180) -> dict:
    """Single API call with retries. Returns dict with content, usage, cost."""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://archplg.co.uk",
        "X-Title": "Archipelago Phase 2K paired-design",
    }
    payload = {
        "model": model_id,
        "messages": [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": user_msg},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    last_err = None
    for attempt in range(retries):
        try:
            t0 = time.time()
            r = requests.post(url, headers=headers, json=payload, timeout=timeout)
            r.raise_for_status()
            data = r.json()
            latency_ms = int((time.time() - t0) * 1000)
            choices = data.get("choices", [])
            if not choices:
                last_err = "no choices in response"
                continue
            content = choices[0].get("message", {}).get("content", "") or ""
            usage = data.get("usage", {})
            # Prefer OpenRouter's pre-computed usage.cost (per cost-audit lesson)
            cost = float(usage.get("cost", 0.0))
            return {
                "content": content,
                "usage": usage,
                "cost_usd": cost,
                "latency_ms": latency_ms,
                "finish_reason": choices[0].get("finish_reason", ""),
                "attempts": attempt + 1,
                "raw_response_full": data,
            }
        except Exception as e:
            last_err = str(e)
            log("WARN", f"  Retry {attempt+1}/{retries} after error: {e}")
            time.sleep(2 ** attempt)
    raise RuntimeError(f"All {retries} attempts failed: {last_err}")


def run_phase2k(config_path: str):
    cfg = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
    api_key = os.environ.get(cfg["openrouter"]["api_key_env"])
    if not api_key:
        log("ERR", f"API key env var {cfg['openrouter']['api_key_env']} not set")
        return 1

    input_dir = Path(cfg["experiment"]["input_phase"])
    output_dir = Path(cfg["experiment"]["output_dir"])
    log_dir = Path(cfg["experiment"]["log_dir"])
    output_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    budget_cap = cfg["experiment"]["total_budget_usd"]
    rating_params = cfg["parameters"]["ratings"]

    total_cost = 0.0
    total_calls = 0
    log("INFO", f"Phase 2K paired design starting. Budget cap ${budget_cap}.")
    log("INFO", f"Reading Phase 2J N cells from {input_dir}")
    log("INFO", f"Output to {output_dir}")

    for task in cfg["tasks"]:
        log("INFO", f"=== Task {task} ===")
        n_cell = load_phase2j_n_cell(input_dir, task)
        if n_cell is None:
            continue
        user_msg, construct_ids, element_labels = build_rating_prompt(n_cell)
        log("INFO", f"  {len(construct_ids)} constructs × {len(element_labels)} elements = {len(construct_ids)*len(element_labels)} ratings/model")

        cell_out = {
            "cell_id": f"{task}_K_run1",
            "task": task,
            "condition": "K",  # paired-K-design marker
            "run_idx": 0,
            "status": "started",
            "started_at": datetime.now().isoformat(),
            "completed_at": None,
            "random_seed": None,
            "free_responses": n_cell.get("free_responses", {}),
            "element_mapping": n_cell.get("element_mapping", {}),
            "element_summaries": n_cell.get("element_summaries", {}),
            "constructs": n_cell.get("constructs", {}),
            "constructs_raw": n_cell.get("constructs_raw", {}),
            "ratings": {},
            "api_calls": [],
            "per_model_cost": {},
            "per_model_tokens": {},
            "cost_usd": 0.0,
            "tokens_in": 0,
            "tokens_out": 0,
            "errors": [],
            "phase2k_persona_assignment": {},
        }

        for model in cfg["models"]:
            sn = model["short_name"]
            persona_id = cfg["persona_assignment"][task][sn]
            cell_out["phase2k_persona_assignment"][sn] = persona_id
            sys_prompt = PERSONA_PROMPTS[persona_id]

            if total_cost > budget_cap:
                log("ERR", f"Budget cap exceeded at ${total_cost:.2f}")
                cell_out["errors"].append(f"budget_cap_reached_before_{sn}")
                break

            try:
                result = call_model(
                    api_key, model["id"],
                    sys_prompt, user_msg,
                    rating_params["temperature"],
                    rating_params["max_tokens"],
                    retries=cfg["openrouter"]["retries_per_call"],
                    timeout=cfg["openrouter"]["request_timeout_seconds"],
                )
            except Exception as e:
                log("ERR", f"  {sn}: failed - {e}")
                # Try fallback
                if model.get("fallback_id"):
                    try:
                        result = call_model(
                            api_key, model["fallback_id"],
                            sys_prompt, user_msg,
                            rating_params["temperature"],
                            rating_params["max_tokens"],
                        )
                        log("WARN", f"  {sn}: fallback {model['fallback_id']} succeeded")
                    except Exception as e2:
                        log("ERR", f"  {sn}: fallback also failed - {e2}")
                        cell_out["errors"].append(f"{sn}: {e} (fallback: {e2})")
                        continue
                else:
                    cell_out["errors"].append(f"{sn}: {e}")
                    continue

            ratings = parse_ratings(result["content"], construct_ids, element_labels)
            n_parsed = sum(len(v) for v in ratings.values())
            cell_out["ratings"][sn] = ratings
            cell_out["per_model_cost"][sn] = result["cost_usd"]
            cell_out["per_model_tokens"][sn] = {
                "in": result["usage"].get("prompt_tokens", 0),
                "out": result["usage"].get("completion_tokens", 0),
            }
            cell_out["api_calls"].append({
                "phase": "phase4_ratings_paired",
                "model_short_name": sn,
                "persona": persona_id,
                "model_id_used": model["id"],
                "n_ratings_parsed": n_parsed,
                "n_ratings_expected": len(construct_ids) * len(element_labels),
                "prompt_tokens": result["usage"].get("prompt_tokens", 0),
                "completion_tokens": result["usage"].get("completion_tokens", 0),
                "reasoning_tokens": result["usage"].get("completion_tokens_details", {}).get("reasoning_tokens", 0),
                "cost_usd": result["cost_usd"],
                "latency_ms": result["latency_ms"],
                "finish_reason": result["finish_reason"],
                "timestamp_iso": datetime.now().isoformat(),
            })
            cell_out["cost_usd"] += result["cost_usd"]
            total_cost += result["cost_usd"]
            total_calls += 1
            log("INFO", f"  {sn} (persona {persona_id}): {n_parsed}/{len(construct_ids)*len(element_labels)} ratings, ${result['cost_usd']:.4f}")

        cell_out["status"] = "complete" if not cell_out["errors"] else "complete_with_errors"
        cell_out["completed_at"] = datetime.now().isoformat()

        # Save cell
        cell_dir = output_dir / cell_out["cell_id"]
        cell_dir.mkdir(parents=True, exist_ok=True)
        with open(cell_dir / "cell.json", "w", encoding="utf-8") as f:
            json.dump(cell_out, f, indent=2, ensure_ascii=False)
        log("INFO", f"  Saved {cell_dir}/cell.json. Cell cost: ${cell_out['cost_usd']:.4f}. Total so far: ${total_cost:.4f}")

    log("INFO", f"\nPhase 2K complete. Total calls: {total_calls}. Total cost: ${total_cost:.4f}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config_phase2k.yaml")
    args = ap.parse_args()
    return run_phase2k(args.config)


if __name__ == "__main__":
    sys.exit(main())
