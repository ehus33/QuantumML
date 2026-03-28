from quantum_healthcare_optimizer.data import Patient
from quantum_healthcare_optimizer.model import evaluate_solution


def test_evaluate_solution_basic() -> None:
    patients = [
        Patient(patient_id=0, benefit=10.0, resource_cost=1, group=0, depends_on=None),
        Patient(patient_id=1, benefit=5.0, resource_cost=1, group=1, depends_on=0),
    ]
    breakdown = evaluate_solution(
        patients=patients,
        picked=[1, 1],
        capacity=2,
        throughput_weight=1.0,
        capacity_penalty=5.0,
        dependency_penalty=4.0,
    )
    assert breakdown.benefit_term == 15.0
    assert breakdown.capacity_overflow == 0
    assert breakdown.dependency_violations == 0
    assert breakdown.score == 17.0
