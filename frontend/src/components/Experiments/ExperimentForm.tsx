import React, { useState, FormEvent } from 'react';
import { Experiment } from '../../types';
import { ExperimentData } from '../../services/experiments';
import ErrorMessage from '../Common/ErrorMessage';

interface ExperimentFormProps {
  initial?: Partial<Experiment>;
  onSubmit: (data: ExperimentData) => Promise<void>;
  onCancel: () => void;
  submitLabel?: string;
}

const EXPERIMENT_TYPES: { value: ExperimentData['experiment_type']; label: string }[] = [
  { value: 'imaging', label: 'Imaging' },
  { value: 'crispr', label: 'CRISPR' },
  { value: 'tnseq', label: 'Tn-seq' },
  { value: 'combined', label: 'Combined' },
];

export default function ExperimentForm({
  initial,
  onSubmit,
  onCancel,
  submitLabel = 'Save',
}: ExperimentFormProps) {
  const [name, setName] = useState(initial?.name ?? '');
  const [description, setDescription] = useState(initial?.description ?? '');
  const [experimentType, setExperimentType] = useState<ExperimentData['experiment_type']>(
    initial?.experiment_type ?? 'imaging'
  );
  const [isPublic, setIsPublic] = useState(initial?.is_public ?? false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await onSubmit({ name, description, experiment_type: experimentType, is_public: isPublic });
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Failed to save experiment.');
    } finally {
      setLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && <ErrorMessage message={error} />}

      <div>
        <label htmlFor="exp-name" className="block text-sm font-medium text-gray-700 mb-1">
          Name <span className="text-red-500">*</span>
        </label>
        <input
          id="exp-name"
          type="text"
          required
          className="input-field"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>

      <div>
        <label htmlFor="exp-desc" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="exp-desc"
          rows={3}
          className="input-field resize-none"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
        />
      </div>

      <div>
        <label htmlFor="exp-type" className="block text-sm font-medium text-gray-700 mb-1">
          Experiment Type <span className="text-red-500">*</span>
        </label>
        <select
          id="exp-type"
          className="input-field"
          value={experimentType}
          onChange={(e) =>
            setExperimentType(e.target.value as ExperimentData['experiment_type'])
          }
        >
          {EXPERIMENT_TYPES.map(({ value, label }) => (
            <option key={value} value={value}>
              {label}
            </option>
          ))}
        </select>
      </div>

      <div className="flex items-center gap-2">
        <input
          id="exp-public"
          type="checkbox"
          className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          checked={isPublic}
          onChange={(e) => setIsPublic(e.target.checked)}
        />
        <label htmlFor="exp-public" className="text-sm text-gray-700">
          Make this experiment public
        </label>
      </div>

      <div className="flex justify-end gap-3 pt-2">
        <button type="button" onClick={onCancel} className="btn-secondary">
          Cancel
        </button>
        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? 'Saving…' : submitLabel}
        </button>
      </div>
    </form>
  );
}
