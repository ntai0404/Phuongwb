import apiClient from './api-client';
import { getRecommendBaseUrl } from './env';

export interface RSSSource {
  id: number;
  name: string;
  url: string;
  category?: string;
  is_active: boolean;
  created_at: string;
}

export interface RSSSourceBasic {
  id: number;
  name: string;
  category?: string;
}

export interface Article {
  id: number;
  title: string;
  link: string;
  published?: string;
  summary?: string;
  image_url?: string;
  category?: string;
  source_id?: number;
  source?: RSSSourceBasic;
  content?: string;
  fetched_at?: string;
  is_saved?: boolean;
}

export interface RSSSourceCreate {
  name: string;
  url: string;
  category?: string;
}

export interface RSSSourceUpdate {
  name?: string;
  url?: string;
  category?: string;
  is_active?: boolean;
}

export const articlesApi = {
  getUserId(): number {
    if (typeof window !== 'undefined') {
      const stored = localStorage.getItem('user_id');
      if (stored) {
        const parsed = Number(stored);
        if (!Number.isNaN(parsed)) return parsed;
      }
    }
    return 1;
  },

  getAll: async (page = 1, limit = 10): Promise<Article[]> => {
    const response = await apiClient.get<Article[]>('/api/v1/articles', {
      params: { page, limit },
    });
    return response.data;
  },

  getById: async (id: number): Promise<Article> => {
    const response = await apiClient.get<Article>(`/api/v1/articles/${id}`);
    return response.data;
  },

  create: async (article: Partial<Article>): Promise<Article> => {
    const response = await apiClient.post<Article>('/api/v1/articles', article);
    return response.data;
  },

  update: async (id: number, article: Partial<Article>): Promise<Article> => {
    const response = await apiClient.put<Article>(`/api/v1/articles/${id}`, article);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/v1/articles/${id}`);
  },

  getRecommendations: async (id: number, topK = 10): Promise<number[]> => {
    const recommendBaseUrl = getRecommendBaseUrl();
    const response = await fetch(`${recommendBaseUrl}/api/v1/recommend/${id}?top_k=${topK}`);
    if (!response.ok) {
      throw new Error('Failed to fetch recommendations');
    }

    const data = await response.json();
    if (Array.isArray(data)) return data.map((x) => Number(x)).filter((x) => !Number.isNaN(x));
    if (Array.isArray((data as any).similar_articles)) {
      return (data as any).similar_articles.map((x: any) => Number(x)).filter((x: number) => !Number.isNaN(x));
    }
    if (Array.isArray((data as any).recommendations)) {
      return (data as any).recommendations
        .map((item: any) => Number(item?.id))
        .filter((x: number) => !Number.isNaN(x));
    }
    return [];
  },

  getByIds: async (ids: number[]): Promise<Article[]> => {
    if (ids.length === 0) return [];
    // Formats: /api/v1/articles?ids=1&ids=2&ids=3
    const params = new URLSearchParams();
    ids.forEach(id => params.append('ids', id.toString()));
    const response = await apiClient.get<Article[]>('/api/v1/articles', {
      params
    });
    return response.data;
  },

  saveArticle: async (id: number): Promise<void> => {
    await apiClient.post(`/api/v1/articles/save/${id}`, {}, { params: { user_id: articlesApi.getUserId() } });
  },

  unsaveArticle: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/v1/articles/save/${id}`, { params: { user_id: articlesApi.getUserId() } });
  },

  checkSaved: async (id: number): Promise<boolean> => {
    const response = await apiClient.get(`/api/v1/articles/saved/${id}`, { params: { user_id: articlesApi.getUserId() } });
    return response.data.is_saved;
  },

  markAsRead: async (id: number): Promise<void> => {
    await apiClient.post(`/api/v1/articles/read/${id}`, {}, { params: { user_id: articlesApi.getUserId() } });
  },

  getSavedArticles: async (): Promise<Article[]> => {
    const response = await apiClient.get('/api/v1/articles/saved', { params: { user_id: articlesApi.getUserId() } });
    return response.data.map((item: any) => item.article);
  },

  getReadingHistory: async (): Promise<Article[]> => {
    const response = await apiClient.get('/api/v1/articles/history', { params: { user_id: articlesApi.getUserId() } });
    return response.data.map((item: any) => item.article);
  },
};

export const rssSourcesApi = {
  getAll: async (): Promise<RSSSource[]> => {
    const response = await apiClient.get<RSSSource[]>('/api/v1/sources');
    return response.data;
  },

  create: async (source: RSSSourceCreate): Promise<RSSSource> => {
    const response = await apiClient.post<RSSSource>('/api/v1/sources', source);
    return response.data;
  },

  update: async (id: number, source: RSSSourceUpdate): Promise<RSSSource> => {
    const response = await apiClient.put<RSSSource>(`/api/v1/sources/${id}`, source);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/v1/sources/${id}`);
  },
};
