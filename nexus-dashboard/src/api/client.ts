import axios from 'axios';

// MISSION-CRITICAL: Automated Cloud Handshake
// This will automatically point to your cloud URL once you set it in your Vercel/Netlify Environment Variables.
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8888';

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// TACTICAL SECURITY HANDSHAKE: Attach JWT to every mission signal
axiosInstance.interceptors.request.use((config) => {
  const token = localStorage.getItem('nexus_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const api = {
  submitEmergency: (content: string, userId: string, metadata: any = {}) => 
    axiosInstance.post('/incident', { content, user_id: userId, metadata }),
  
  getProfile: (userId: string) => 
    axiosInstance.get(`/profile/${userId}`),
    
  setProfile: (userId: string, profile: any) => 
    axiosInstance.post(`/profile/${userId}`, profile),
    
  getHistory: (userId: string) => 
    axiosInstance.get(`/history/${userId}`),

  checkHealth: () => 
    axiosInstance.get('/health'),
};
