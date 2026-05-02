import api from './api';
import { AuthTokens, User } from '../types';

export interface RegisterData {
  email: string;
  username: string;
  full_name: string;
  password: string;
}

export async function login(email: string, password: string): Promise<AuthTokens> {
  const { data } = await api.post<AuthTokens>('/auth/login', { email, password });
  return data;
}

export async function register(data: RegisterData): Promise<AuthTokens> {
  const { data: response } = await api.post<AuthTokens>('/auth/register', data);
  return response;
}

export async function refreshToken(token: string): Promise<AuthTokens> {
  const { data } = await api.post<AuthTokens>('/auth/refresh', { refresh_token: token });
  return data;
}

export async function getMe(): Promise<User> {
  const { data } = await api.get<User>('/auth/me');
  return data;
}

export function logout(): void {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
}
