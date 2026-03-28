import React from 'react';
import { Config } from '../types/api';
import { Settings, Zap, Users, Activity } from 'lucide-react';

interface ConfigurationPanelProps {
  config: Partial<Config>;
  onConfigChange: (config: Partial<Config>) => void;
  disabled?: boolean;
}

export const ConfigurationPanel: React.FC<ConfigurationPanelProps> = ({
  config,
  onConfigChange,
  disabled = false,
}) => {
  const handleInputChange = (field: keyof Config, value: string | number) => {
    onConfigChange({
      ...config,
      [field]: field === 'num_patients' || field === 'capacity' || field === 'seed' || 
                field === 'qaoa_reps' || field === 'optimizer_maxiter' 
        ? parseInt(value.toString()) || 0
        : parseFloat(value.toString()) || 0,
    });
  };

  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-6">
        <Settings className="w-5 h-5 text-quantum-600" />
        <h2 className="text-xl font-bold text-gray-800">Configuration</h2>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Basic Configuration */}
        <div className="space-y-4">
          <h3 className="font-semibold text-gray-700 flex items-center gap-2">
            <Users className="w-4 h-4" />
            Basic Settings
          </h3>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Number of Patients
            </label>
            <input
              type="number"
              min="1"
              max="20"
              value={config.num_patients || 6}
              onChange={(e) => handleInputChange('num_patients', e.target.value)}
              disabled={disabled}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-quantum-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Treatment Capacity
            </label>
            <input
              type="number"
              min="1"
              max="10"
              value={config.capacity || 3}
              onChange={(e) => handleInputChange('capacity', e.target.value)}
              disabled={disabled}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-quantum-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Random Seed
            </label>
            <input
              type="number"
              value={config.seed || 42}
              onChange={(e) => handleInputChange('seed', e.target.value)}
              disabled={disabled}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-quantum-500"
            />
          </div>
        </div>

        {/* Optimization Parameters */}
        <div className="space-y-4">
          <h3 className="font-semibold text-gray-700 flex items-center gap-2">
            <Activity className="w-4 h-4" />
            Optimization Parameters
          </h3>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Throughput Weight
            </label>
            <input
              type="number"
              step="0.1"
              value={config.throughput_weight || 1.5}
              onChange={(e) => handleInputChange('throughput_weight', e.target.value)}
              disabled={disabled}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-quantum-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Capacity Penalty
            </label>
            <input
              type="number"
              step="0.1"
              value={config.capacity_penalty || 12.0}
              onChange={(e) => handleInputChange('capacity_penalty', e.target.value)}
              disabled={disabled}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-quantum-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Dependency Penalty
            </label>
            <input
              type="number"
              step="0.1"
              value={config.dependency_penalty || 8.0}
              onChange={(e) => handleInputChange('dependency_penalty', e.target.value)}
              disabled={disabled}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-quantum-500"
            />
          </div>
        </div>

        {/* Quantum Parameters */}
        <div className="space-y-4">
          <h3 className="font-semibold text-gray-700 flex items-center gap-2">
            <Zap className="w-4 h-4" />
            Quantum Parameters
          </h3>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              QAOA Repetitions
            </label>
            <input
              type="number"
              min="1"
              max="5"
              value={config.qaoa_reps || 1}
              onChange={(e) => handleInputChange('qaoa_reps', e.target.value)}
              disabled={disabled}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-quantum-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Optimizer Max Iterations
            </label>
            <input
              type="number"
              min="10"
              max="200"
              value={config.optimizer_maxiter || 60}
              onChange={(e) => handleInputChange('optimizer_maxiter', e.target.value)}
              disabled={disabled}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-quantum-500"
            />
          </div>
        </div>
      </div>
    </div>
  );
};
