from quantum_healthcare_optimizer.data import generate_patient_cohort
from quantum_healthcare_optimizer.model import build_quadratic_program


def test_build_quadratic_program() -> None:
    patients = generate_patient_cohort(num_patients=4, seed=7)
    qp = build_quadratic_program(
        patients=patients,
        capacity=2,
        throughput_weight=1.5,
        capacity_penalty=10.0,
        dependency_penalty=8.0,
    )
    assert qp.get_num_binary_vars() == 4
