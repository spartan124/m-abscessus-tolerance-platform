export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string;
  role: 'researcher' | 'admin' | 'viewer';
  is_active: boolean;
  created_at: string;
}

export interface Experiment {
  id: number;
  name: string;
  description?: string;
  experiment_type: 'imaging' | 'crispr' | 'tnseq' | 'combined';
  status: 'pending' | 'running' | 'completed' | 'failed';
  is_public: boolean;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export interface ExperimentListResponse {
  experiments: Experiment[];
  total: number;
  page: number;
  per_page: number;
  pages: number;
}

export interface Strain {
  id: number;
  name: string;
  description?: string;
}

export interface Drug {
  id: number;
  name: string;
  class?: string;
  description?: string;
}

export interface Condition {
  id: number;
  name: string;
  description?: string;
}

export interface FileUpload {
  id: number;
  experiment_id: number;
  filename: string;
  original_filename: string;
  file_type: string;
  file_size: number;
  status: string;
  created_at: string;
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  user: User;
}
