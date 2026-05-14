import axios from "axios";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
});

export const scanBookshelf = (formData) =>
  api.post("/api/scan/", formData, { headers: { "Content-Type": "multipart/form-data" } });

export const getDemoScan = () => api.post("/api/scan/demo");

export const getRecommendations = (titles, mood = null) =>
  api.post("/api/recommend/", { titles, mood });

export const getMoodRecommendations = (mood) =>
  api.post("/api/recommend/mood", { mood });

export const getTrending = () => api.get("/api/recommend/trending");

export const searchBooks = (q, top_k = 10) =>
  api.get("/api/search/", { params: { q, top_k } });

export const getAnalytics = (userId) =>
  api.get(`/api/analytics/${userId}`);

export default api;
