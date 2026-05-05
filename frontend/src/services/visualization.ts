import api from './api';

export interface SurvivalCurveData {
  time: number;
  survival: number;
  [key: string]: number;
}

export interface HeatmapData {
  rows: string[];
  columns: string[];
  values: number[][];
}

export interface TimeKillData {
  time: number;
  cfu: number;
  condition?: string;
  [key: string]: number | string | undefined;
}

export interface ScatterData {
  x: number;
  y: number;
  label?: string;
  [key: string]: number | string | undefined;
}

export interface ImageMeta {
  id: number;
  filename: string;
  url: string;
  description?: string;
}

export interface NetworkData {
  nodes: { id: string; label: string; [key: string]: unknown }[];
  edges: { source: string; target: string; weight?: number }[];
}

export async function getSurvivalCurve(id: number): Promise<SurvivalCurveData[]> {
  const { data } = await api.get<SurvivalCurveData[]>(`/visualization/survival-curve/${id}`);
  return data;
}

export async function getHeatmap(id: number): Promise<HeatmapData> {
  const { data } = await api.get<HeatmapData>(`/visualization/heatmap/${id}`);
  return data;
}

export async function getTimeKill(id: number): Promise<TimeKillData[]> {
  const { data } = await api.get<TimeKillData[]>(`/visualization/time-kill/${id}`);
  return data;
}

export async function getScatter(id: number): Promise<ScatterData[]> {
  const { data } = await api.get<ScatterData[]>(`/visualization/scatter/${id}`);
  return data;
}

interface ImagesResponse {
  images: ImageMeta[];
  total: number;
}

export async function getImages(id: number): Promise<ImageMeta[]> {
  const { data } = await api.get<ImagesResponse>(`/visualization/images/${id}`);
  return data.images;
}

export async function getNetwork(id: number): Promise<NetworkData> {
  const { data } = await api.get<NetworkData>(`/visualization/network/${id}`);
  return data;
}
