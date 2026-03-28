import axios from 'axios';
import { Patient, Config, SolverResult, ExperimentResult } from '../types/api';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiClient = {
  // Health check
  health: () => api.get('/health'),
  
  // Configuration
  getConfig: () => api.get<Config>('/config'),
  
  // Patient generation
  generatePatients: (numPatients: number, seed: number) => 
    api.post<{ patients: Patient[]; num_patients: number }>('/generate-patients', {
      num_patients: numPatients,
      seed,
    }),
  
  // Solve with specific method
  solve: (data: {
    patients: Patient[];
    method: 'greedy' | 'brute_force' | 'qaoa';
    config: Partial<Config>;
  }) => api.post<{ method: string; result: SolverResult; config: Partial<Config> }>('/solve', {
    patients: data.patients,
    method: data.method,
    ...data.config,
  }),
  
  // Run full experiment
  runExperiment: (config: Partial<Config>) => 
    api.post<ExperimentResult>('/experiment', config),
  
  // Compare all methods
  compare: (data: {
    patients: Patient[];
    config: Partial<Config>;
  }) => api.post<{
    patients: Patient[];
    config: Partial<Config>;
    results: SolverResult[];
  }>('/compare', {
    patients: data.patients,
    ...data.config,
  }),
};
