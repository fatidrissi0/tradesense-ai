import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401) {
      localStorage.removeItem('access_token');
      // Optional: Redirect to login or handle session expiry
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (data: any) => api.post('/api/auth/register', data),
  login: (data: any) => api.post('/api/auth/login', data),
  getCurrentUser: () => api.get('/api/auth/me'),
};

export const paymentAPI = {
  getPlans: () => api.get('/api/payment/plans'),
  checkout: (data: any) => api.post('/api/payment/checkout', data),
  getHistory: () => api.get('/api/payment/history'),
};

export const tradingAPI = {
  getActiveChallenge: () => api.get('/api/challenges/active'),
  executeTrade: (data: any) => api.post('/api/trades/execute', data),
  getTradeHistory: () => api.get('/api/trades/history'),
};

export const marketAPI = {
  getLivePrice: (symbol: string) => api.get(`/api/market/live/${symbol}`),
  getChartData: (symbol: string) => api.get(`/api/market/chart/${symbol}`),
  getMoroccoStock: (ticker: string) => api.get(`/api/market/morocco/${ticker}`),
  getSignal: (symbol: string) => api.get(`/api/signals/${symbol}`),
  getMoroccoSignal: (ticker: string) => api.get(`/api/signals/morocco/${ticker}`),
};

export const leaderboardAPI = {
  getMonthly: () => api.get('/api/leaderboard/monthly'),
};

// Export the axios instance as well for flexibility
export { api };
export default api;
