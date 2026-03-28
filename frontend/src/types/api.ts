export interface Patient {
  patient_id: number;
  benefit: number;
  resource_cost: number;
  group: number;
  depends_on: number | null;
}

export interface Config {
  seed: number;
  num_patients: number;
  capacity: number;
  throughput_weight: number;
  capacity_penalty: number;
  dependency_penalty: number;
  fairness_penalty: number;
  qaoa_reps: number;
  optimizer_maxiter: number;
}

export interface SolverResult {
  name: string;
  picked: number[];
  runtime_seconds: number;
  breakdown: {
    benefit_term: number;
    throughput_term: number;
    capacity_overflow: number;
    dependency_violations: number;
    fairness_gap: number;
    score: number;
  };
}

export interface ExperimentResult {
  config: Config;
  patients: Patient[];
  results: SolverResult[];
}
