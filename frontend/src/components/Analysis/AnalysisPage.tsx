import React, { useEffect, useState } from 'react';
import Layout from '../Common/Layout';
import LoadingSpinner from '../Common/LoadingSpinner';
import { listExperiments } from '../../services/experiments';
import { Experiment } from '../../types';

export default function AnalysisPage() {
  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [selected, setSelected] = useState<string>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listExperiments({ per_page: 100 })
      .then((res) => setExperiments(res.experiments))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Layout>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Analysis</h1>

      <div className="max-w-xl">
        <div className="card mb-6">
          <label htmlFor="analysis-exp" className="block text-sm font-medium text-gray-700 mb-2">
            Select Experiment
          </label>
          {loading ? (
            <LoadingSpinner />
          ) : (
            <select
              id="analysis-exp"
              className="input-field"
              value={selected}
              onChange={(e) => setSelected(e.target.value)}
            >
              <option value="">— Choose experiment —</option>
              {experiments.map((exp) => (
                <option key={exp.id} value={exp.id}>
                  {exp.name} ({exp.experiment_type})
                </option>
              ))}
            </select>
          )}
        </div>

        <div className="card flex flex-col items-center py-12 text-center">
          <span className="text-5xl mb-4">🔬</span>
          <h2 className="text-lg font-semibold text-gray-700 mb-2">
            Analysis Features Coming Soon
          </h2>
          <p className="text-sm text-gray-500 max-w-sm">
            Advanced statistical analysis, differential expression, and tolerance scoring will be
            available here. Stay tuned for updates.
          </p>
          {selected && (
            <p className="mt-4 text-xs text-blue-700 font-medium">
              Selected experiment ID: {selected}
            </p>
          )}
        </div>
      </div>
    </Layout>
  );
}
