import React, { createContext, useState, useEffect, useContext, ReactNode } from 'react';
import { authAPI } from '../services/api';
import { User } from '../types';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (username: string, email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkUser = async () => {
      const token = localStorage.getItem('access_token');
      if (token) {
        try {
          const response = await authAPI.getCurrentUser();
          setUser(response.data.user);
        } catch (error) {
          console.error('Failed to fetch user', error);
          localStorage.removeItem('access_token');
        }
      }
      setLoading(false);
    };

    checkUser();
  }, []);

  const login = async (email: string, password: string) => {
    const response = await authAPI.login({ email, password });
    const { access_token, user: loggedUser } = response.data;
    localStorage.setItem('access_token', access_token);
    setUser(loggedUser);
  };

  const register = async (username: string, email: string, password: string) => {
    const response = await authAPI.register({ username, email, password });
    const { access_token, user: newUser } = response.data;
    localStorage.setItem('access_token', access_token);
    setUser(newUser);
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  const isAuthenticated = !!user;

  return (
    <AuthContext.Provider value={{ user, loading, isAuthenticated, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
