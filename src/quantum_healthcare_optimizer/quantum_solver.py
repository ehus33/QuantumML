from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from qiskit.primitives import StatevectorSampler
from qiskit_algorithms import QAOA
from qiskit_algorithms.optimizers import COBYLA
from qiskit_optimization.algorithms import MinimumEigenOptimizer

from .baselines import SolverResult
from .data import Patient
from .model import build_quadratic_program, decode_solution, evaluate_solution


@dataclass(slots=True)
class QAOAConfig:
    reps: int = 1
    maxiter: int = 60
    seed: int = 42


def qaoa_solve(
    patients: list[Patient],
    capacity: int,
    throughput_weight: float,
    capacity_penalty: float,
    dependency_penalty: float,
    fairness_penalty: float = 0.0,
    reps: int = 1,
    maxiter: int = 60,
    seed: int = 42,
) -> SolverResult:
    qp = build_quadratic_program(
        patients=patients,
        capacity=capacity,
        throughput_weight=throughput_weight,
        capacity_penalty=capacity_penalty,
        dependency_penalty=dependency_penalty,
        fairness_penalty=fairness_penalty,
    )

    sampler = StatevectorSampler(seed=seed)
    optimizer = COBYLA(maxiter=maxiter)
    qaoa = QAOA(sampler=sampler, optimizer=optimizer, reps=reps)
    minimum_eigen_optimizer = MinimumEigenOptimizer(qaoa)

    start = perf_counter()
    result = minimum_eigen_optimizer.solve(qp)
    runtime = perf_counter() - start

    picked = decode_solution(result.x)
    breakdown = evaluate_solution(
        patients,
        picked,
        capacity,
        throughput_weight,
        capacity_penalty,
        dependency_penalty,
        fairness_penalty,
    )
    return SolverResult("qaoa", picked, breakdown, runtime)
