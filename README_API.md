# Quantum Healthcare Optimizer API

A Flask REST API wrapper for the quantum healthcare optimization system.

## Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Start the API server
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
- **GET** `/health`
- Returns: `{"status": "healthy", "service": "quantum-healthcare-optimizer"}`

### Configuration
- **GET** `/config`
- Returns default configuration parameters

### Generate Patients
- **POST** `/generate-patients`
- Body: `{"num_patients": 6, "seed": 42}`
- Returns: Generated synthetic patient data

### Solve Optimization
- **POST** `/solve`
- Body: 
  ```json
  {
    "patients": [...],
    "method": "greedy|brute_force|qaoa",
    "capacity": 3,
    "throughput_weight": 1.5,
    "capacity_penalty": 12.0,
    "dependency_penalty": 8.0,
    "fairness_penalty": 0.0,
    "qaoa_reps": 1,
    "optimizer_maxiter": 60,
    "seed": 42
  }
  ```
- Returns: Optimization result for specified method

### Full Experiment
- **POST** `/experiment`
- Body: Configuration parameters (all optional)
- Returns: Complete experiment results with all solvers

### Compare Methods
- **POST** `/compare`
- Body: Patient data + configuration
- Returns: Results from all three solvers for comparison

## Example Usage

### Quick experiment with defaults:
```bash
curl -X POST http://localhost:5000/experiment
```

### Generate patients:
```bash
curl -X POST http://localhost:5000/generate-patients \
  -H "Content-Type: application/json" \
  -d '{"num_patients": 8, "seed": 123}'
```

### Solve with specific method:
```bash
curl -X POST http://localhost:5000/solve \
  -H "Content-Type: application/json" \
  -d '{
    "patients": [...],
    "method": "qaoa",
    "capacity": 4,
    "qaoa_reps": 2
  }'
```

## Response Format

All responses are JSON. Error responses include an "error" field with status codes 400/500.

## Development

Run with debug mode:
```bash
python app.py
```

The API supports CORS for cross-origin requests from web applications.
