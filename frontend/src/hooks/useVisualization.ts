import { useState, useEffect } from 'react';
import * as vizService from '../services/visualization';
import type {
  SurvivalCurveData,
  HeatmapData,
  TimeKillData,
  ScatterData,
  ImageMeta,
  NetworkData,
} from '../services/visualization';

interface UseVisualizationResult {
  survivalCurve: SurvivalCurveData[] | null;
  heatmap: HeatmapData | null;
  timeKill: TimeKillData[] | null;
  scatter: ScatterData[] | null;
  images: ImageMeta[] | null;
  network: NetworkData | null;
  loading: boolean;
  error: string | null;
}

export function useVisualization(experimentId: number): UseVisualizationResult {
  const [survivalCurve, setSurvivalCurve] = useState<SurvivalCurveData[] | null>(null);
  const [heatmap, setHeatmap] = useState<HeatmapData | null>(null);
  const [timeKill, setTimeKill] = useState<TimeKillData[] | null>(null);
  const [scatter, setScatter] = useState<ScatterData[] | null>(null);
  const [images, setImages] = useState<ImageMeta[] | null>(null);
  const [network, setNetwork] = useState<NetworkData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!experimentId) return;
    let cancelled = false;
    setLoading(true);
    setError(null);

    Promise.allSettled([
      vizService.getSurvivalCurve(experimentId),
      vizService.getHeatmap(experimentId),
      vizService.getTimeKill(experimentId),
      vizService.getScatter(experimentId),
      vizService.getImages(experimentId),
      vizService.getNetwork(experimentId),
    ]).then(([sc, hm, tk, sp, img, net]) => {
      if (cancelled) return;
      if (sc.status === 'fulfilled') setSurvivalCurve(sc.value);
      if (hm.status === 'fulfilled') setHeatmap(hm.value);
      if (tk.status === 'fulfilled') setTimeKill(tk.value);
      if (sp.status === 'fulfilled') setScatter(sp.value);
      if (img.status === 'fulfilled') setImages(img.value);
      if (net.status === 'fulfilled') setNetwork(net.value);

      const firstError = [sc, hm, tk, sp, img, net].find(
        (r) => r.status === 'rejected'
      ) as PromiseRejectedResult | undefined;
      if (firstError) {
        setError(firstError.reason?.response?.data?.detail || 'Some visualizations failed to load');
      }
      setLoading(false);
    });

    return () => { cancelled = true; };
  }, [experimentId]);

  return { survivalCurve, heatmap, timeKill, scatter, images, network, loading, error };
}
