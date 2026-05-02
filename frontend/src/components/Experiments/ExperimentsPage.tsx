import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Layout from '../Common/Layout';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorMessage from '../Common/ErrorMessage';
import ExperimentForm from './ExperimentForm';
import { useExperiments } from '../../hooks/useExperiments';
import { createExperiment, ExperimentData } from '../../services/experiments';
import { Experiment } from '../../types';

const STATUS_BADGE: Record<Experiment['status'], string> = {
  pending: 'badge-yellow',
  running: 'badge-blue',
  completed: 'badge-green',
  failed: 'badge-red',
};

const TYPE_BADGE: Record<Experiment['experiment_type'], string> = {
  imaging: 'badge-blue',
  crispr: 'badge-purple',
  tnseq: 'badge-green',
  combined: 'badge-gray',
};

export default function ExperimentsPage() {
  const [showModal, setShowModal] = useState(false);
  const [search, setSearch] = useState('');
  const [typeFilter, setTypeFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  const { experiments, total, page, pages, setPage, loading, error, refetch } =
    useExperiments({
      search: search || undefined,
      experiment_type: typeFilter || undefined,
      status: statusFilter || undefined,
    });

  async function handleCreate(data: ExperimentData) {
    await createExperiment(data);
    setShowModal(false);
    refetch();
  }

  return (
    <Layout>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Experiments</h1>
        <button className="btn-primary" onClick={() => setShowModal(true)}>
          + New Experiment
        </button>
      </div>

      {/* Filters */}
      <div className="card mb-6 flex flex-wrap gap-3">
        <input
          type="text"
          placeholder="Search experiments…"
          className="input-field flex-1 min-w-[180px]"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select
          className="input-field w-44"
          value={typeFilter}
          onChange={(e) => setTypeFilter(e.target.value)}
        >
          <option value="">All types</option>
          <option value="imaging">Imaging</option>
          <option value="crispr">CRISPR</option>
          <option value="tnseq">Tn-seq</option>
          <option value="combined">Combined</option>
        </select>
        <select
          className="input-field w-44"
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
        >
          <option value="">All statuses</option>
          <option value="pending">Pending</option>
          <option value="running">Running</option>
          <option value="completed">Completed</option>
          <option value="failed">Failed</option>
        </select>
      </div>

      {error && <ErrorMessage message={error} />}
      {loading ? (
        <LoadingSpinner />
      ) : (
        <>
          <div className="card overflow-x-auto p-0">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  {['Name', 'Type', 'Status', 'Public', 'Created', ''].map((h) => (
                    <th
                      key={h}
                      className="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wide"
                    >
                      {h}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-100 bg-white">
                {experiments.length === 0 ? (
                  <tr>
                    <td colSpan={6} className="px-4 py-8 text-center text-gray-400">
                      No experiments found.
                    </td>
                  </tr>
                ) : (
                  experiments.map((exp) => (
                    <tr key={exp.id} className="hover:bg-gray-50 transition-colors">
                      <td className="px-4 py-3 text-sm font-medium text-gray-900">
                        {exp.name}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <span className={TYPE_BADGE[exp.experiment_type] ?? 'badge-gray'}>
                          {exp.experiment_type}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <span className={STATUS_BADGE[exp.status] ?? 'badge-gray'}>
                          {exp.status}
                        </span>
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {exp.is_public ? 'Yes' : 'No'}
                      </td>
                      <td className="px-4 py-3 text-sm text-gray-500">
                        {new Date(exp.created_at).toLocaleDateString()}
                      </td>
                      <td className="px-4 py-3 text-sm">
                        <Link
                          to={`/experiments/${exp.id}`}
                          className="text-blue-700 hover:underline font-medium"
                        >
                          View →
                        </Link>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {pages > 1 && (
            <div className="flex items-center justify-between mt-4">
              <p className="text-sm text-gray-500">
                Showing {experiments.length} of {total} experiments
              </p>
              <div className="flex gap-2">
                <button
                  className="btn-secondary"
                  disabled={page <= 1}
                  onClick={() => setPage(page - 1)}
                >
                  ← Prev
                </button>
                <span className="px-3 py-2 text-sm text-gray-700">
                  Page {page} of {pages}
                </span>
                <button
                  className="btn-secondary"
                  disabled={page >= pages}
                  onClick={() => setPage(page + 1)}
                >
                  Next →
                </button>
              </div>
            </div>
          )}
        </>
      )}

      {/* Create modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-lg mx-4 p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">New Experiment</h2>
            <ExperimentForm
              onSubmit={handleCreate}
              onCancel={() => setShowModal(false)}
              submitLabel="Create"
            />
          </div>
        </div>
      )}
    </Layout>
  );
}
