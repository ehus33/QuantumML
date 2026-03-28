# Quantum Healthcare Optimizer

A Qiskit-based starter repo for a high-risk AI-in-healthcare project.

This project models a small healthcare resource-allocation problem as a QUBO:

- maximize expected patient health benefit
- maximize the number of patients treated
- penalize capacity violations
- penalize dependency violations, such as a treatment that requires another step first

The repo includes:

- synthetic patient generation for a toy healthcare optimization task
- a QUBO builder using Docplex and Qiskit Optimization
- classical baselines: brute force and greedy
- a quantum optimizer path using QAOA on a simulator
- result export to JSON for your ACM report and presentation

## Why this project fits the course

It is high-risk because it combines healthcare optimization with quantum methods that may not outperform classical methods. Even if QAOA does not win, the project still produces a strong reportable result about feasibility, scaling limits, and tradeoffs.

## Problem statement

Given a set of patients, limited treatment resources, and dependency links between interventions, choose which patients to treat in order to optimize both total health benefit and treatment throughput.

## Repo layout

```text
quantum-healthcare-optimizer/
  configs/
    default.json
  docs/
    project_spec.md
  scripts/
    run_experiment.py
  src/quantum_healthcare_optimizer/
    __init__.py
    config.py
    data.py
    model.py
    baselines.py
    quantum_solver.py
    metrics.py
    experiment.py
  tests/
    test_metrics.py
    test_qubo.py
```

## Installation

Python 3.11+ is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -e .
```

If editable install gives trouble, use:

```bash
pip install -r requirements.txt
export PYTHONPATH=src
```

## Main dependencies

- qiskit
- qiskit-algorithms
- qiskit-optimization
- qiskit-machine-learning
- qiskit-aer
- docplex
- numpy
- pandas

The current Qiskit machine-learning docs expose `VQC` and `QSVC`, while the optimization docs expose `QuadraticProgram` and `MinimumEigenOptimizer` for QUBO workflows. This repo uses the optimization stack because your project is a resource-allocation problem rather than plain classification. citeturn302033search1turn302033search3turn716525search0turn716525search1

## Quick start

Run the full experiment with the default config:

```bash
python scripts/run_experiment.py --config configs/default.json
```

This will:

1. generate a synthetic patient cohort
2. build a QUBO objective
3. solve it with greedy and brute-force baselines
4. solve it with QAOA on a simulator
5. write a JSON summary to `results/`

## Example research question

Can a quantum optimization method produce competitive treatment-allocation decisions when balancing patient benefit, throughput, and dependency constraints under limited capacity?

## Notes

- This repo uses a simulator. You do not need quantum hardware.
- Start with 5 to 10 patients. QAOA becomes slow as the problem grows.
- The synthetic setup is intentional. It lets you test the method before trying a real healthcare-derived scoring scheme.

## Suggested next step for the class paper

Use this repo to generate results, then write up:

- objective function design
- baseline comparison
- QAOA setup
- solution quality
- runtime and scalability limits
- ethical limitations of simplified patient-benefit scores
