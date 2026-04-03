export interface Record {
  id: string;
  name: string;
  description: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface RecordListResponse {
  items: Record[];
  total: number;
}

export interface RecordItemResponse {
  item: Record;
}

export interface RecordCreate {
  name: string;
  description?: string | null;
  status?: string;
}

export interface RecordUpdate {
  name?: string;
  description?: string | null;
  status?: string;
}

export interface AppInfo {
  name: string;
  env: string;
  version: string;
}

export interface HealthStatus {
  status: string;
}

function getApiBaseUrl(): string {
  if (typeof window === "undefined") {
    return process.env.BACKEND_URL || "http://localhost:8000";
  }
  return "";
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const baseUrl = getApiBaseUrl();
  const res = await fetch(`${baseUrl}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...options?.headers,
    },
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ error: { message: res.statusText } }));
    throw new Error(error.error?.message || error.detail || res.statusText);
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

export const api = {
  health: () => request<HealthStatus>("/health"),
  appInfo: () => request<AppInfo>("/api/v1/app"),
  records: {
    list: (skip = 0, limit = 50) =>
      request<RecordListResponse>(`/api/v1/records?skip=${skip}&limit=${limit}`),
    get: (id: string) => request<RecordItemResponse>(`/api/v1/records/${id}`),
    create: (data: RecordCreate) =>
      request<RecordItemResponse>("/api/v1/records", {
        method: "POST",
        body: JSON.stringify(data),
      }),
    update: (id: string, data: RecordUpdate) =>
      request<RecordItemResponse>(`/api/v1/records/${id}`, {
        method: "PATCH",
        body: JSON.stringify(data),
      }),
    delete: (id: string) =>
      request<void>(`/api/v1/records/${id}`, { method: "DELETE" }),
  },
};
