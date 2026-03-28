import React from 'react';
import { SolverResult } from '../types/api';
import { Clock, Trophy, Zap, Target } from 'lucide-react';

interface ResultsTableProps {
  results: SolverResult[];
}

export const ResultsTable: React.FC<ResultsTableProps> = ({ results }) => {
  const getMethodIcon = (method: string) => {
    switch (method) {
      case 'greedy':
        return <Zap className="w-4 h-4 text-yellow-600" />;
      case 'brute_force':
        return <Target className="w-4 h-4 text-blue-600" />;
      case 'qaoa':
        return <Trophy className="w-4 h-4 text-purple-600" />;
      default:
        return null;
    }
  };

  const getMethodName = (method: string) => {
    switch (method) {
      case 'greedy':
        return 'Greedy';
      case 'brute_force':
        return 'Brute Force';
      case 'qaoa':
        return 'QAOA (Quantum)';
      default:
        return method;
    }
  };

  return (
    <div className="card">
      <h2 className="text-xl font-bold text-gray-800 mb-6">Optimization Results</h2>
      
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Method</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Score</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Benefit</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Throughput</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Patients Treated</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">Runtime</th>
            </tr>
          </thead>
          <tbody>
            {results.map((result, index) => (
              <tr key={index} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-3 px-4">
                  <div className="flex items-center gap-2">
                    {getMethodIcon(result.name)}
                    <span className="font-medium">{getMethodName(result.name)}</span>
                  </div>
                </td>
                <td className="py-3 px-4">
                  <span className="font-semibold text-green-600">
                    {result.breakdown.score.toFixed(2)}
                  </span>
                </td>
                <td className="py-3 px-4">{result.breakdown.benefit_term.toFixed(2)}</td>
                <td className="py-3 px-4">{result.breakdown.throughput_term.toFixed(2)}</td>
                <td className="py-3 px-4">
                  {result.picked.filter(p => p === 1).length} / {result.picked.length}
                </td>
                <td className="py-3 px-4">
                  <div className="flex items-center gap-1">
                    <Clock className="w-3 h-3 text-gray-500" />
                    {result.runtime_seconds < 0.001 
                      ? '< 0.001s' 
                      : `${result.runtime_seconds.toFixed(3)}s`
                    }
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Detailed Breakdown */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
        {results.map((result, index) => (
          <div key={index} className="bg-gray-50 rounded-lg p-4">
            <div className="flex items-center gap-2 mb-3">
              {getMethodIcon(result.name)}
              <h3 className="font-semibold text-gray-800">{getMethodName(result.name)}</h3>
            </div>
            
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600">Total Score:</span>
                <span className="font-semibold">{result.breakdown.score.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Benefit Term:</span>
                <span>{result.breakdown.benefit_term.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Throughput Term:</span>
                <span>{result.breakdown.throughput_term.toFixed(2)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Capacity Overflow:</span>
                <span className={result.breakdown.capacity_overflow > 0 ? 'text-red-600' : 'text-green-600'}>
                  {result.breakdown.capacity_overflow}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Dependency Violations:</span>
                <span className={result.breakdown.dependency_violations > 0 ? 'text-red-600' : 'text-green-600'}>
                  {result.breakdown.dependency_violations}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Fairness Gap:</span>
                <span>{result.breakdown.fairness_gap.toFixed(2)}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
