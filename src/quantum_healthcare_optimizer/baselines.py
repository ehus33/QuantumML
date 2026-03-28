from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from time import perf_counter

from .data import Patient
from .model import ObjectiveBreakdown, evaluate_solution


@dataclass(slots=True)
class SolverResult:
    name: str
    picked: list[int]
    breakdown: ObjectiveBreakdown
    runtime_seconds: float


def brute_force_baseline(
    patients: list[Patient],
    capacity: int,
    throughput_weight: float,
    capacity_penalty: float,
    dependency_penalty: float,
    fairness_penalty: float = 0.0,
) -> SolverResult:
    start = perf_counter()
    best_pick: list[int] | None = None
    best_breakdown: ObjectiveBreakdown | None = None

    for bits in product([0, 1], repeat=len(patients)):
        picked = list(bits)
        breakdown = evaluate_solution(
            patients,
            picked,
            capacity,
            throughput_weight,
            capacity_penalty,
            dependency_penalty,
            fairness_penalty,
        )
        if best_breakdown is None or breakdown.score > best_breakdown.score:
            best_pick = picked
            best_breakdown = breakdown

    runtime = perf_counter() - start
    assert best_pick is not None and best_breakdown is not None
    return SolverResult("brute_force", best_pick, best_breakdown, runtime)


def greedy_baseline(
    patients: list[Patient],
    capacity: int,
    throughput_weight: float,
    capacity_penalty: float,
    dependency_penalty: float,
    fairness_penalty: float = 0.0,
) -> SolverResult:
    start = perf_counter()
    scored = []
    for p in patients:
        ratio = (p.benefit + throughput_weight) / p.resource_cost
        if p.depends_on is not None:
            ratio -= 0.5
        scored.append((ratio, p.patient_id))

    picked = [0] * len(patients)
    used = 0
    for _, patient_id in sorted(scored, reverse=True):
        p = patients[patient_id]
        if used + p.resource_cost <= capacity:
            if p.depends_on is None or picked[p.depends_on] == 1:
                picked[patient_id] = 1
                used += p.resource_cost

    breakdown = evaluate_solution(
        patients,
        picked,
        capacity,
        throughput_weight,
        capacity_penalty,
        dependency_penalty,
        fairness_penalty,
    )
    runtime = perf_counter() - start
    return SolverResult("greedy", picked, breakdown, runtime)
