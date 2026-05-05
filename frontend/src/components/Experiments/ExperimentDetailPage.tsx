import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import Layout from '../Common/Layout';
import LoadingSpinner from '../Common/LoadingSpinner';
import ErrorMessage from '../Common/ErrorMessage';
import ExperimentForm from './ExperimentForm';
import { getExperiment, updateExperiment, deleteExperiment, ExperimentData } from '../../services/experiments';
import { Experiment } from '../../types';

export default function ExperimentDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const experimentId = Number(id);

  const [experiment, setExperiment] = useState<Experiment | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editing, setEditing] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState(false);

  useEffect(() => {
    if (!experimentId) return;
    setLoading(true);
    getExperiment(experimentId)
      .then(setExperiment)
      .catch((err) =>
        setError(err?.response?.data?.detail || 'Failed to load experiment.')
      )
      .finally(() => setLoading(false));
  }, [experimentId]);

  async function handleUpdate(data: ExperimentData) {
    const updated = await updateExperiment(experimentId, data);
    setExperiment(updated);
    setEditing(false);
  }

  async function handleDelete() {
    await deleteExperiment(experimentId);
    navigate('/experiments');
  }

  if (loading) return <Layout><LoadingSpinner /></Layout>;
  if (error) return <Layout><ErrorMessage message={error} /></Layout>;
  if (!experiment) return null;

  return (
    <Layout>
      <div className="mb-6 flex items-center gap-3">
        <Link to="/experiments" className="text-blue-700 hover:underline text-sm">
          ← Experiments
        </Link>
        <span className="text-gray-400">/</span>
        <h1 className="text-xl font-bold text-gray-900">{experiment.name}</h1>
      </div>

      {editing ? (
        <div className="card max-w-lg">
          <h2 className="text-lg font-semibold mb-4">Edit Experiment</h2>
          <ExperimentForm
            initial={experiment}
            onSubmit={handleUpdate}
            onCancel={() => setEditing(false)}
            submitLabel="Update"
          />
        </div>
      ) : (
        <>
          <div className="card mb-6 max-w-2xl">
            <dl className="grid grid-cols-2 gap-x-6 gap-y-4 text-sm">
              <Detail label="ID" value={String(experiment.id)} />
              <Detail label="Type" value={experiment.experiment_type} />
              <Detail label="Status" value={experiment.status} />
              <Detail label="Public" value={experiment.is_public ? 'Yes' : 'No'} />
              <Detail
                label="Created"
                value={new Date(experiment.created_at).toLocaleString()}
              />
              <Detail
                label="Updated"
                value={new Date(experiment.updated_at).toLocaleString()}
              />
              {experiment.description && (
                <div className="col-span-2">
                  <dt className="text-gray-500 font-medium">Description</dt>
                  <dd className="mt-1 text-gray-900">{experiment.description}</dd>
                </div>
              )}
            </dl>
          </div>

          {/* Action buttons */}
          <div className="flex flex-wrap gap-3 mb-8">
            <button className="btn-secondary" onClick={() => setEditing(true)}>
              ✏️ Edit
            </button>
            <Link
              to={`/visualization/${experiment.id}`}
              className="btn-primary"
            >
              📊 View Visualizations
            </Link>
            <Link to={`/upload?experiment_id=${experiment.id}`} className="btn-secondary">
              📂 Upload Files
            </Link>
            <button
              className="btn-danger"
              onClick={() => setDeleteConfirm(true)}
            >
              🗑️ Delete
            </button>
          </div>
        </>
      )}

      {/* Delete confirmation modal */}
      {deleteConfirm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40">
          <div className="bg-white rounded-lg shadow-xl w-full max-w-sm mx-4 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">Delete Experiment</h3>
            <p className="text-sm text-gray-600 mb-6">
              Are you sure you want to delete <strong>{experiment.name}</strong>? This action
              cannot be undone.
            </p>
            <div className="flex justify-end gap-3">
              <button className="btn-secondary" onClick={() => setDeleteConfirm(false)}>
                Cancel
              </button>
              <button className="btn-danger" onClick={handleDelete}>
                Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </Layout>
  );
}

function Detail({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <dt className="text-gray-500 font-medium">{label}</dt>
      <dd className="mt-0.5 text-gray-900 capitalize">{value}</dd>
    </div>
  );
}
