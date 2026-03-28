from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any, Dict

from flask import Flask, request, jsonify
from flask_cors import CORS

REPO_ROOT = Path(__file__).resolve().parents[0]
SRC_PATH = REPO_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from quantum_healthcare_optimizer.config import ExperimentConfig
from quantum_healthcare_optimizer.experiment import run_experiment
from quantum_healthcare_optimizer.data import generate_patient_cohort
from quantum_healthcare_optimizer.baselines import greedy_baseline, brute_force_baseline
from quantum_healthcare_optimizer.quantum_solver import qaoa_solve
from quantum_healthcare_optimizer.metrics import patients_to_table

app = Flask(__name__)
CORS(app)


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "healthy", "service": "quantum-healthcare-optimizer"})


@app.route("/config", methods=["GET"])
def get_default_config():
    """Get default configuration."""
    config = ExperimentConfig()
    return jsonify({
        "seed": config.seed,
        "num_patients": config.num_patients,
        "capacity": config.capacity,
        "throughput_weight": config.throughput_weight,
        "capacity_penalty": config.capacity_penalty,
        "dependency_penalty": config.dependency_penalty,
        "fairness_penalty": config.fairness_penalty,
        "qaoa_reps": config.qaoa_reps,
        "optimizer_maxiter": config.optimizer_maxiter
    })


@app.route("/generate-patients", methods=["POST"])
def generate_patients():
    """Generate synthetic patient data."""
    try:
        data = request.get_json()
        num_patients = data.get("num_patients", 6)
        seed = data.get("seed", 42)
        
        patients = generate_patient_cohort(num_patients, seed)
        return jsonify({
            "patients": patients_to_table(patients),
            "num_patients": len(patients)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/solve", methods=["POST"])
def solve_optimization():
    """Solve healthcare optimization problem with specified method."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ["patients", "method"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        patients = data["patients"]
        method = data["method"]
        
        # Get configuration parameters with defaults
        capacity = data.get("capacity", 3)
        throughput_weight = data.get("throughput_weight", 1.5)
        capacity_penalty = data.get("capacity_penalty", 12.0)
        dependency_penalty = data.get("dependency_penalty", 8.0)
        fairness_penalty = data.get("fairness_penalty", 0.0)
        qaoa_reps = data.get("qaoa_reps", 1)
        optimizer_maxiter = data.get("optimizer_maxiter", 60)
        seed = data.get("seed", 42)
        
        # Solve with specified method
        if method == "greedy":
            result = greedy_baseline(
                patients, capacity, throughput_weight,
                capacity_penalty, dependency_penalty, fairness_penalty
            )
        elif method == "brute_force":
            result = brute_force_baseline(
                patients, capacity, throughput_weight,
                capacity_penalty, dependency_penalty, fairness_penalty
            )
        elif method == "qaoa":
            result = qaoa_solve(
                patients, capacity, throughput_weight,
                capacity_penalty, dependency_penalty, fairness_penalty,
                reps=qaoa_reps, maxiter=optimizer_maxiter, seed=seed
            )
        else:
            return jsonify({"error": f"Unknown method: {method}"}), 400
        
        return jsonify({
            "method": method,
            "result": result.__dict__,
            "config": {
                "capacity": capacity,
                "throughput_weight": throughput_weight,
                "capacity_penalty": capacity_penalty,
                "dependency_penalty": dependency_penalty,
                "fairness_penalty": fairness_penalty,
                "qaoa_reps": qaoa_reps,
                "optimizer_maxiter": optimizer_maxiter,
                "seed": seed
            }
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/experiment", methods=["POST"])
def run_full_experiment():
    """Run full experiment with all solvers."""
    try:
        data = request.get_json()
        
        # Create config from request or use defaults
        config = ExperimentConfig(
            seed=data.get("seed", 42),
            num_patients=data.get("num_patients", 6),
            capacity=data.get("capacity", 3),
            throughput_weight=data.get("throughput_weight", 1.5),
            capacity_penalty=data.get("capacity_penalty", 12.0),
            dependency_penalty=data.get("dependency_penalty", 8.0),
            fairness_penalty=data.get("fairness_penalty", 0.0),
            qaoa_reps=data.get("qaoa_reps", 1),
            optimizer_maxiter=data.get("optimizer_maxiter", 60)
        )
        
        # Run experiment
        payload = run_experiment(config)
        return jsonify(payload)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/compare", methods=["POST"])
def compare_methods():
    """Compare all methods on given patient data."""
    try:
        data = request.get_json()
        
        if "patients" not in data:
            return jsonify({"error": "Missing patients data"}), 400
        
        patients = data["patients"]
        
        # Get configuration parameters
        capacity = data.get("capacity", 3)
        throughput_weight = data.get("throughput_weight", 1.5)
        capacity_penalty = data.get("capacity_penalty", 12.0)
        dependency_penalty = data.get("dependency_penalty", 8.0)
        fairness_penalty = data.get("fairness_penalty", 0.0)
        qaoa_reps = data.get("qaoa_reps", 1)
        optimizer_maxiter = data.get("optimizer_maxiter", 60)
        seed = data.get("seed", 42)
        
        # Run all methods
        greedy = greedy_baseline(
            patients, capacity, throughput_weight,
            capacity_penalty, dependency_penalty, fairness_penalty
        )
        brute = brute_force_baseline(
            patients, capacity, throughput_weight,
            capacity_penalty, dependency_penalty, fairness_penalty
        )
        qaoa = qaoa_solve(
            patients, capacity, throughput_weight,
            capacity_penalty, dependency_penalty, fairness_penalty,
            reps=qaoa_reps, maxiter=optimizer_maxiter, seed=seed
        )
        
        results = [greedy, brute, qaoa]
        
        return jsonify({
            "patients": patients,
            "config": {
                "capacity": capacity,
                "throughput_weight": throughput_weight,
                "capacity_penalty": capacity_penalty,
                "dependency_penalty": dependency_penalty,
                "fairness_penalty": fairness_penalty,
                "qaoa_reps": qaoa_reps,
                "optimizer_maxiter": optimizer_maxiter,
                "seed": seed
            },
            "results": [result.__dict__ for result in results]
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
