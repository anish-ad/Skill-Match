import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const signup = (data) => api.post("/auth/signup", data);
export const login = (data) => api.post("/auth/login", data);
export const getDashboard = () => api.get("/dashboard");

export const uploadResume = (file) => {
  const formData = new FormData();
  formData.append("file", file);
  return api.post("/resume/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
};

export const getMyResumes = () => api.get("/resume/my-resumes");

export const analyzeJob = (data) => api.post("/jobs/analyze", data);
export const getMyJobs = () => api.get("/jobs/my-jobs");

export default api;