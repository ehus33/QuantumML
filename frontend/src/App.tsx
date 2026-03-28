import React, { useState, useEffect } from 'react';
import { ConfigurationPanel } from './components/ConfigurationPanel';
import { ResultsTable } from './components/ResultsTable';
import { apiClient } from './api/client';
import { Config, ExperimentResult, SolverResult } from './types/api';
import { Play, Zap, Activity, Users, Cpu } from 'lucide-react';

function App() {
  const [config, setConfig] = useState<Partial<Config>>({
    seed: 42,
    num_patients: 6,
    capacity: 3,
    throughput_weight: 1.5,
    capacity_penalty: 12.0,
    dependency_penalty: 8.0,
    fairness_penalty: 0.0,
    qaoa_reps: 1,
    optimizer_maxiter: 60,
  });

  const [results, setResults] = useState<SolverResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const runExperiment = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.runExperiment(config);
      setResults(response.data.results);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to run experiment');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
      {/* Header */}
      <header className="quantum-gradient text-white shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Cpu className="w-8 h-8" />
              <div>
                <h1 className="text-2xl font-bold">Quantum Healthcare Optimizer</h1>
                <p className="text-blue-100 text-sm">AI-powered treatment allocation using quantum computing</p>
              </div>
            </div>
            <div className="flex items-center gap-2 text-sm">
              <Zap className="w-4 h-4" />
              <span>QAOA Powered</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Configuration Panel */}
          <div className="lg:col-span-1">
            <ConfigurationPanel
              config={config}
              onConfigChange={setConfig}
              disabled={loading}
            />
            
            {/* Run Button */}
            <button
              onClick={runExperiment}
              disabled={loading}
              className="w-full mt-6 btn-primary flex items-center justify-center gap-2 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Activity className="w-4 h-4 animate-spin" />
                  Running Experiment...
                </>
              ) : (
                <>
                  <Play className="w-4 h-4" />
                  Run Quantum Experiment
                </>
              )}
            </button>

            {/* Error Display */}
            {error && (
              <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
                <p className="text-red-800 text-sm">{error}</p>
              </div>
            )}
          </div>

          {/* Results Panel */}
          <div className="lg:col-span-2">
            {results.length > 0 ? (
              <ResultsTable results={results} />
            ) : (
              <div className="card text-center py-12">
                <Users className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                <h3 className="text-lg font-semibold text-gray-700 mb-2">
                  No Results Yet
                </h3>
                <p className="text-gray-500 mb-6">
                  Configure your experiment parameters and click "Run Quantum Experiment" to see optimization results.
                </p>
                <div className="text-left max-w-md mx-auto bg-gray-50 rounded-lg p-4">
                  <h4 className="font-semibold text-gray-700 mb-2">What this does:</h4>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Generates synthetic patient data</li>
                    <li>• Optimizes treatment allocation using quantum computing</li>
                    <li>• Compares quantum (QAOA) with classical methods</li>
                    <li>• Balances patient benefit, throughput, and constraints</li>
                  </ul>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white py-6 mt-12">
        <div className="container mx-auto px-4 text-center">
          <p className="text-sm text-gray-400">
            Quantum Healthcare Optimizer • High-risk AI in Healthcare Project
          </p>
          <p className="text-xs text-gray-500 mt-2">
            Uses Qiskit for quantum simulation • No quantum hardware required
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
