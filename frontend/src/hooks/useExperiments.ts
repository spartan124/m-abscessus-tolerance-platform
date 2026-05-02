import { useState, useEffect, useCallback } from 'react';
import { Experiment, ExperimentListResponse } from '../types';
import { listExperiments, ExperimentParams } from '../services/experiments';

interface UseExperimentsResult {
  experiments: Experiment[];
  total: number;
  page: number;
  pages: number;
  setPage: (page: number) => void;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useExperiments(
  initialParams?: Omit<ExperimentParams, 'page'>
): UseExperimentsResult {
  const [page, setPage] = useState(1);
  const [data, setData] = useState<ExperimentListResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tick, setTick] = useState(0);

  const refetch = useCallback(() => setTick((t) => t + 1), []);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);

    listExperiments({ ...initialParams, page })
      .then((res) => {
        if (!cancelled) setData(res);
      })
      .catch((err) => {
        if (!cancelled)
          setError(err?.response?.data?.detail || 'Failed to load experiments');
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [page, tick]);

  return {
    experiments: data?.experiments ?? [],
    total: data?.total ?? 0,
    page: data?.page ?? page,
    pages: data?.pages ?? 1,
    setPage,
    loading,
    error,
    refetch,
  };
}
