from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any
import random


@dataclass(slots=True)
class Patient:
    patient_id: int
    benefit: float
    resource_cost: int
    group: int
    depends_on: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def generate_patient_cohort(num_patients: int, seed: int = 42) -> list[Patient]:
    """Generate a small synthetic cohort.

    The setup is intentionally toy-sized so QAOA on a simulator remains feasible.
    `group` can later support fairness experiments.
    `depends_on` encodes prerequisite treatment links.
    """
    rng = random.Random(seed)
    patients: list[Patient] = []
    for idx in range(num_patients):
        benefit = round(rng.uniform(4.0, 10.0), 2)
        resource_cost = rng.randint(1, 2)
        group = rng.randint(0, 1)

        depends_on: int | None = None
        if idx >= 2 and rng.random() < 0.25:
            depends_on = rng.randint(0, idx - 1)

        patients.append(
            Patient(
                patient_id=idx,
                benefit=benefit,
                resource_cost=resource_cost,
                group=group,
                depends_on=depends_on,
            )
        )
    return patients
