'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { getApiBaseUrl } from '@/lib/api-client';

interface User {
  id: number;
  username: string;
  role: 'user' | 'admin';
}

interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string, confirmPassword: string) => Promise<void>;
  logout: () => void;
  isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on mount
    const token = localStorage.getItem('access_token');
    if (token) {
      // Validate token and get user info
      fetch(`${getApiBaseUrl()}/api/v1/auth/users/me`, {
        headers: { 'Authorization': `Bearer ${token}` },
      })
        .then(res => {
          if (!res.ok) throw new Error('Token invalid');
          return res.json();
        })
        .then(userData => {
          setUser(userData);
          if (typeof window !== 'undefined') {
            localStorage.setItem('user_id', String(userData.id));
          }
        })
        .catch(() => {
          // Token invalid, remove it
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        })
        .finally(() => {
          setIsLoading(false);
        });
    } else {
      setIsLoading(false);
    }
  }, []);

  const extractErrorMessage = (errorData: any, fallback: string) => {
    if (!errorData) return fallback;
    if (typeof errorData.detail === 'string') return errorData.detail;
    if (Array.isArray(errorData.detail)) {
      return errorData.detail
        .map((item: any) => item?.msg || item?.detail || JSON.stringify(item))
        .join('; ');
    }
    if (typeof errorData.detail === 'object') {
      return Object.values(errorData.detail)
        .map((val) => (typeof val === 'string' ? val : JSON.stringify(val)))
        .join('; ');
    }
    if (typeof errorData === 'string') return errorData;
    return fallback;
  };

  const login = async (username: string, password: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${getApiBaseUrl()}/api/v1/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Login failed' }));
        throw new Error(extractErrorMessage(errorData, 'Login failed'));
      }
      const data = await response.json();
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
      // Get user info
      const userResponse = await fetch(`${getApiBaseUrl()}/api/v1/auth/users/me`, {
        headers: { 'Authorization': `Bearer ${data.access_token}` },
      });
      if (!userResponse.ok) throw new Error('Failed to get user info');
      const userData = await userResponse.json();
      setUser(userData);
      localStorage.setItem('user_id', String(userData.id));
    } finally {
      setIsLoading(false);
    }
  };

  const register = async (username: string, password: string, confirmPassword: string) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${getApiBaseUrl()}/api/v1/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, confirm_password: confirmPassword }),
      });
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({ detail: 'Registration failed' }));
        throw new Error(extractErrorMessage(errorData, 'Registration failed'));
      }
      const data = await response.json();
      // Auto login after register
      await login(username, password);
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_id');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}