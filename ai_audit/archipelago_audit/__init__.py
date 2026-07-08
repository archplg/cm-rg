"""
archipelago_audit - Cognitive diversity audit for multi-agent LLM systems.

Quick start:
    from archipelago_audit import AuditResult

    # Load an audit produced by the experimental pipeline
    result = AuditResult.load("operator_outputs/B_P_run1/operator_insight.json")
    print(result.headline)
    print(result.severity)

    # Block deployment if severity is high
    if result.is_blocking():
        raise RuntimeError(f"Ensemble audit failed: {result.headline}")
"""
from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AuditResult:
    """Loaded operator_insight.json with convenient accessors."""
    raw: dict

    @classmethod
    def load(cls, path: str | Path) -> "AuditResult":
        with open(path, "r", encoding="utf-8") as f:
            return cls(raw=json.load(f))

    @property
    def cell_id(self) -> str:
        return self.raw.get("cell_id", "?")

    @property
    def headline(self) -> str:
        return self.raw.get("headline", "")

    @property
    def consensus_strength(self) -> str:
        return self.raw["consensus_map"].get("consensus_strength", "unknown")

    @property
    def reasoning_diversity_score(self) -> float:
        return float(self.raw["hidden_disagreement"].get("reasoning_diversity_score", 0))

    @property
    def severity(self) -> str:
        if self.consensus_strength == "strong" and self.reasoning_diversity_score > 1.0:
            return "HIGH"
        if self.consensus_strength == "strong" and self.reasoning_diversity_score < 0.3:
            return "LOW"
        if self.consensus_strength == "split":
            return "INFO"
        return "MEDIUM"

    def is_blocking(self) -> bool:
        return self.severity == "HIGH"

    def operator_questions(self) -> list[str]:
        return self.raw.get("operator_questions", [])

    def blind_spots(self) -> list[dict]:
        return self.raw["blind_spots"].get("low_discrimination_constructs", [])


__all__ = ["AuditResult"]
