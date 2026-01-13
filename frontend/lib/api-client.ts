import axios from 'axios';

const resolveApiBaseUrl = () => {
  const envUrl = process.env.NEXT_PUBLIC_API_URL;

  // Browser runtime: favor the current host unless env points to an external host
  if (typeof window !== 'undefined') {
    if (envUrl && !envUrl.includes('core-api-service')) return envUrl;

    const { protocol, hostname } = window.location;
    return `${protocol}//${hostname}:8080`;
  }

  // SSR inside Docker uses service DNS or env override
  return envUrl || 'http://core-api-service:8080';
};

export const getApiBaseUrl = resolveApiBaseUrl;

const apiClient = axios.create({
  baseURL: "http://api.vdailytintuc.store",
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for API calls
apiClient.interceptors.request.use(
  (config) => {
    // Add auth token if available (guard for SSR)
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor for API calls
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401 errors (token expired)
    if (error.response?.status === 401 && typeof window !== 'undefined') {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      window.location.href = '/auth';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
