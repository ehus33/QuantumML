from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
from typing import Any

from .baselines import SolverResult, brute_force_baseline, greedy_baseline
from .config import ExperimentConfig
from .data import generate_patient_cohort
from .metrics import compare_results, patients_to_table
from .quantum_solver import qaoa_solve


def run_experiment(config: ExperimentConfig) -> dict[str, Any]:
    patients = generate_patient_cohort(config.num_patients, config.seed)

    greedy = greedy_baseline(
        patients,
        config.capacity,
        config.throughput_weight,
        config.capacity_penalty,
        config.dependency_penalty,
        config.fairness_penalty,
    )
    brute = brute_force_baseline(
        patients,
        config.capacity,
        config.throughput_weight,
        config.capacity_penalty,
        config.dependency_penalty,
        config.fairness_penalty,
    )
    qaoa = qaoa_solve(
        patients,
        config.capacity,
        config.throughput_weight,
        config.capacity_penalty,
        config.dependency_penalty,
        config.fairness_penalty,
        reps=config.qaoa_reps,
        maxiter=config.optimizer_maxiter,
        seed=config.seed,
    )

    results: list[SolverResult] = [greedy, brute, qaoa]
    payload = {
        "config": asdict(config),
        "patients": patients_to_table(patients),
        "results": compare_results(results),
    }
    return payload


def save_experiment(payload: dict[str, Any], output_dir: str | Path) -> Path:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    filename = output_path / "experiment_results.json"
    filename.write_text(json.dumps(payload, indent=2))
    return filename
