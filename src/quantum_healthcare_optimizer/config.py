from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path


@dataclass(slots=True)
class ExperimentConfig:
    seed: int = 42
    num_patients: int = 6
    capacity: int = 3
    throughput_weight: float = 1.5
    capacity_penalty: float = 12.0
    dependency_penalty: float = 8.0
    fairness_penalty: float = 0.0
    qaoa_reps: int = 1
    optimizer_maxiter: int = 60
    output_dir: str = "results"

    @classmethod
    def from_json(cls, path: str | Path) -> "ExperimentConfig":
        data = json.loads(Path(path).read_text())
        return cls(**data)
