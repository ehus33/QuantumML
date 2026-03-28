from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .baselines import SolverResult
from .data import Patient


def patients_to_table(patients: list[Patient]) -> list[dict[str, Any]]:
    return [p.to_dict() for p in patients]


def result_to_dict(result: SolverResult) -> dict[str, Any]:
    return {
        "name": result.name,
        "picked": result.picked,
        "runtime_seconds": result.runtime_seconds,
        "breakdown": asdict(result.breakdown),
    }


def compare_results(results: list[SolverResult]) -> list[dict[str, Any]]:
    return [result_to_dict(r) for r in results]
