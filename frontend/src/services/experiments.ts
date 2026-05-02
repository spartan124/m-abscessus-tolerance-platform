import api from './api';
import { Experiment, ExperimentListResponse, Strain, Drug, Condition } from '../types';

export interface ExperimentParams {
  page?: number;
  per_page?: number;
  search?: string;
  experiment_type?: string;
  status?: string;
}

export interface ExperimentData {
  name: string;
  description?: string;
  experiment_type: 'imaging' | 'crispr' | 'tnseq' | 'combined';
  is_public?: boolean;
}

export async function listExperiments(params?: ExperimentParams): Promise<ExperimentListResponse> {
  const { data } = await api.get<ExperimentListResponse>('/experiments/', { params });
  return data;
}

export async function createExperiment(data: ExperimentData): Promise<Experiment> {
  const { data: response } = await api.post<Experiment>('/experiments/', data);
  return response;
}

export async function getExperiment(id: number): Promise<Experiment> {
  const { data } = await api.get<Experiment>(`/experiments/${id}`);
  return data;
}

export async function updateExperiment(id: number, data: Partial<ExperimentData>): Promise<Experiment> {
  const { data: response } = await api.put<Experiment>(`/experiments/${id}`, data);
  return response;
}

export async function deleteExperiment(id: number): Promise<void> {
  await api.delete(`/experiments/${id}`);
}

export async function listStrains(): Promise<Strain[]> {
  const { data } = await api.get<Strain[]>('/experiments/strains');
  return data;
}

export async function listDrugs(): Promise<Drug[]> {
  const { data } = await api.get<Drug[]>('/experiments/drugs');
  return data;
}

export async function listConditions(): Promise<Condition[]> {
  const { data } = await api.get<Condition[]>('/experiments/conditions');
  return data;
}
