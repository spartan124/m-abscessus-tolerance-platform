import api from './api';
import { FileUpload } from '../types';

export type UploadType = 'imaging' | 'crispr' | 'tnseq' | 'metadata';

export async function uploadFile(
  type: UploadType,
  experimentId: number,
  file: File
): Promise<FileUpload> {
  const formData = new FormData();
  formData.append('experiment_id', String(experimentId));
  formData.append('file', file);

  const { data } = await api.post<FileUpload>(`/upload/${type}`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
}

export async function getUploadStatus(id: number): Promise<FileUpload> {
  const { data } = await api.get<FileUpload>(`/upload/status/${id}`);
  return data;
}
