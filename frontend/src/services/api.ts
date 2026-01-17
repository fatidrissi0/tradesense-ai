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
  register: (data: any) => api.post('/auth/register', data),
  login: (data: any) => api.post('/auth/login', data),
  getCurrentUser: () => api.get('/auth/me'),
};

export const paymentAPI = {
  getPlans: () => api.get('/payment/plans'),
  checkout: (data: any) => api.post('/payment/checkout', data),
  getHistory: () => api.get('/payment/history'),
};

export const tradingAPI = {
  getActiveChallenge: () => api.get('/challenges/active'),
  executeTrade: (data: any) => api.post('/trades/execute', data),
  getTradeHistory: () => api.get('/trades/history'),
};

export const marketAPI = {
  getLivePrice: (symbol: string) => api.get(`/market/live/${symbol}`),
  getChartData: (symbol: string) => api.get(`/market/chart/${symbol}`),
  getMoroccoStock: (ticker: string) => api.get(`/market/morocco/${ticker}`),
  getSignal: (symbol: string) => api.get(`/signals/${symbol}`),
  getMoroccoSignal: (ticker: string) => api.get(`/signals/morocco/${ticker}`),
};

export const leaderboardAPI = {
  getMonthly: () => api.get('/leaderboard/monthly'),
};

// Export the axios instance as well for flexibility
export { api };
export default api;
