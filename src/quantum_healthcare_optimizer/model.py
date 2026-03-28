from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from docplex.mp.model import Model
from qiskit_optimization import QuadraticProgram
from qiskit_optimization.translators import from_docplex_mp

from .data import Patient


@dataclass(slots=True)
class ObjectiveBreakdown:
    benefit_term: float
    throughput_term: float
    capacity_overflow: int
    dependency_violations: int
    fairness_gap: int
    score: float


def build_docplex_qubo(
    patients: list[Patient],
    capacity: int,
    throughput_weight: float,
    capacity_penalty: float,
    dependency_penalty: float,
    fairness_penalty: float = 0.0,
) -> Model:
    """Build an unconstrained binary quadratic model.

    Maximize:
      total benefit
      + throughput_weight * number treated
      - capacity_penalty * overflow^2
      - dependency_penalty * dependency violations
      - fairness_penalty * treatment-group imbalance^2

    `overflow` is modeled with a square penalty over the difference between
    total used resources and capacity.
    """
    mdl = Model(name="healthcare_qubo")
    x = [mdl.binary_var(name=f"x_{p.patient_id}") for p in patients]

    total_benefit = mdl.sum(p.benefit * x[i] for i, p in enumerate(patients))
    throughput = mdl.sum(x)
    used_resources = mdl.sum(p.resource_cost * x[i] for i, p in enumerate(patients))
    overflow_penalty = (used_resources - capacity) * (used_resources - capacity)

    dependency_penalties = []
    for i, p in enumerate(patients):
        if p.depends_on is not None:
            dependency_penalties.append(x[i] * (1 - x[p.depends_on]))

    if dependency_penalties:
        dependency_penalty_term = mdl.sum(dependency_penalties)
    else:
        dependency_penalty_term = 0

    fairness_penalty_term = 0
    if fairness_penalty > 0:
        treated_group0 = mdl.sum(x[i] for i, p in enumerate(patients) if p.group == 0)
        treated_group1 = mdl.sum(x[i] for i, p in enumerate(patients) if p.group == 1)
        fairness_penalty_term = (treated_group0 - treated_group1) * (treated_group0 - treated_group1)

    objective = (
        total_benefit
        + throughput_weight * throughput
        - capacity_penalty * overflow_penalty
        - dependency_penalty * dependency_penalty_term
        - fairness_penalty * fairness_penalty_term
    )
    mdl.maximize(objective)
    return mdl


def build_quadratic_program(
    patients: list[Patient],
    capacity: int,
    throughput_weight: float,
    capacity_penalty: float,
    dependency_penalty: float,
    fairness_penalty: float = 0.0,
) -> QuadraticProgram:
    mdl = build_docplex_qubo(
        patients=patients,
        capacity=capacity,
        throughput_weight=throughput_weight,
        capacity_penalty=capacity_penalty,
        dependency_penalty=dependency_penalty,
        fairness_penalty=fairness_penalty,
    )
    return from_docplex_mp(mdl)


def decode_solution(bitstring: Iterable[int | float]) -> list[int]:
    return [int(round(v)) for v in bitstring]


def evaluate_solution(
    patients: list[Patient],
    picked: list[int],
    capacity: int,
    throughput_weight: float,
    capacity_penalty: float,
    dependency_penalty: float,
    fairness_penalty: float = 0.0,
) -> ObjectiveBreakdown:
    benefit_term = sum(p.benefit * picked[i] for i, p in enumerate(patients))
    throughput_term = throughput_weight * sum(picked)
    used_resources = sum(p.resource_cost * picked[i] for i, p in enumerate(patients))
    capacity_overflow = max(0, used_resources - capacity)

    dependency_violations = 0
    for i, p in enumerate(patients):
        if p.depends_on is not None and picked[i] == 1 and picked[p.depends_on] == 0:
            dependency_violations += 1

    fairness_gap = 0
    if fairness_penalty > 0:
        treated_group0 = sum(picked[i] for i, p in enumerate(patients) if p.group == 0)
        treated_group1 = sum(picked[i] for i, p in enumerate(patients) if p.group == 1)
        fairness_gap = abs(treated_group0 - treated_group1)

    score = (
        benefit_term
        + throughput_term
        - capacity_penalty * (capacity_overflow**2)
        - dependency_penalty * dependency_violations
        - fairness_penalty * (fairness_gap**2)
    )
    return ObjectiveBreakdown(
        benefit_term=benefit_term,
        throughput_term=throughput_term,
        capacity_overflow=capacity_overflow,
        dependency_violations=dependency_violations,
        fairness_gap=fairness_gap,
        score=score,
    )
