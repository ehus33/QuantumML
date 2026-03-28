# Project spec

## Title
Quantum-Inspired Optimization for Healthcare Resource Allocation

## Research question
Can QAOA-style quantum optimization produce competitive treatment-allocation decisions when balancing patient health benefit and the number of patients treated under limited capacity and dependency constraints?

## Core idea
Each patient has:

- an expected health benefit score
- a resource cost
- an optional prerequisite dependency

A binary variable decides whether the patient is treated. The optimizer aims to maximize:

- total expected health benefit
- total patients treated

while penalizing:

- exceeding system capacity
- violating dependencies

## Methods

- synthetic patient cohort generation
- QUBO formulation in Docplex
- conversion to `QuadraticProgram`
- greedy baseline
- brute-force exact baseline
- QAOA with `MinimumEigenOptimizer`

Qiskit Optimization documents `QuadraticProgram` and `MinimumEigenOptimizer` as the standard workflow for turning binary optimization into an Ising Hamiltonian solved by a minimum eigensolver. citeturn716525search0turn716525search1turn716525search3

## Output

- solution bitstring
- treated patient count
- total expected benefit
- capacity usage
- dependency violations
- objective score
- runtime

## Why it is high-risk

Current quantum optimization methods are resource-limited and may fail to beat classical methods on even modest problem sizes. That makes the method ambitious but still reportable if it underperforms.
