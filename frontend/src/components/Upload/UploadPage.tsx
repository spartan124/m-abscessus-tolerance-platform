import React, { useEffect, useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useSearchParams } from 'react-router-dom';
import Layout from '../Common/Layout';
import ErrorMessage from '../Common/ErrorMessage';
import LoadingSpinner from '../Common/LoadingSpinner';
import { listExperiments } from '../../services/experiments';
import { uploadFile, UploadType } from '../../services/upload';
import { Experiment, FileUpload } from '../../types';

const UPLOAD_TYPES: { value: UploadType; label: string; description: string }[] = [
  { value: 'imaging', label: 'Imaging', description: 'Microscopy / fluorescence images' },
  { value: 'crispr', label: 'CRISPR', description: 'CRISPR screen results' },
  { value: 'tnseq', label: 'Tn-seq', description: 'Transposon sequencing data' },
  { value: 'metadata', label: 'Metadata', description: 'Experimental metadata files' },
];

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 ** 2) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 ** 2).toFixed(1)} MB`;
}

export default function UploadPage() {
  const [searchParams] = useSearchParams();
  const preselectedId = searchParams.get('experiment_id');

  const [experiments, setExperiments] = useState<Experiment[]>([]);
  const [expLoading, setExpLoading] = useState(true);
  const [experimentId, setExperimentId] = useState<string>(preselectedId ?? '');
  const [uploadType, setUploadType] = useState<UploadType>('imaging');
  const [file, setFile] = useState<File | null>(null);

  const [uploading, setUploading] = useState(false);
  const [result, setResult] = useState<FileUpload | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listExperiments({ per_page: 100 })
      .then((res) => setExperiments(res.experiments))
      .finally(() => setExpLoading(false));
  }, []);

  const onDrop = useCallback((accepted: File[]) => {
    if (accepted.length > 0) {
      setFile(accepted[0]);
      setResult(null);
      setError(null);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    multiple: false,
  });

  async function handleUpload() {
    if (!file || !experimentId) return;
    setUploading(true);
    setError(null);
    setResult(null);
    try {
      const res = await uploadFile(uploadType, Number(experimentId), file);
      setResult(res);
      setFile(null);
    } catch (err: any) {
      setError(err?.response?.data?.detail || 'Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  }

  return (
    <Layout>
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Upload Data</h1>

      <div className="max-w-2xl space-y-6">
        {/* Experiment selector */}
        <div className="card">
          <h2 className="text-base font-semibold text-gray-800 mb-3">1. Select Experiment</h2>
          {expLoading ? (
            <LoadingSpinner />
          ) : (
            <select
              className="input-field"
              value={experimentId}
              onChange={(e) => setExperimentId(e.target.value)}
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

        {/* Upload type */}
        <div className="card">
          <h2 className="text-base font-semibold text-gray-800 mb-3">2. Select Upload Type</h2>
          <div className="grid grid-cols-2 gap-3">
            {UPLOAD_TYPES.map(({ value, label, description }) => (
              <button
                key={value}
                type="button"
                onClick={() => setUploadType(value)}
                className={`text-left p-3 rounded-lg border-2 transition-colors ${
                  uploadType === value
                    ? 'border-blue-600 bg-blue-50'
                    : 'border-gray-200 hover:border-blue-300'
                }`}
              >
                <p className="text-sm font-semibold text-gray-800">{label}</p>
                <p className="text-xs text-gray-500 mt-0.5">{description}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Dropzone */}
        <div className="card">
          <h2 className="text-base font-semibold text-gray-800 mb-3">3. Drop or Select File</h2>
          <div
            {...getRootProps()}
            className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
              isDragActive
                ? 'border-blue-500 bg-blue-50'
                : 'border-gray-300 hover:border-blue-400 hover:bg-gray-50'
            }`}
          >
            <input {...getInputProps()} />
            <p className="text-3xl mb-2">📁</p>
            {isDragActive ? (
              <p className="text-blue-600 font-medium">Drop the file here…</p>
            ) : file ? (
              <div>
                <p className="font-medium text-gray-800">{file.name}</p>
                <p className="text-sm text-gray-500">{formatBytes(file.size)}</p>
              </div>
            ) : (
              <p className="text-gray-500">
                Drag &amp; drop a file here, or click to select
              </p>
            )}
          </div>
        </div>

        {error && <ErrorMessage message={error} />}

        {result && (
          <div className="rounded-md bg-green-50 border border-green-200 p-4 text-sm text-green-800">
            ✅ <strong>{result.original_filename}</strong> uploaded successfully (ID: {result.id}).
          </div>
        )}

        <button
          className="btn-primary w-full"
          disabled={!file || !experimentId || uploading}
          onClick={handleUpload}
        >
          {uploading ? 'Uploading…' : 'Upload File'}
        </button>
      </div>
    </Layout>
  );
}
