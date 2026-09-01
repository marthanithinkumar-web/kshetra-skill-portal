import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_BASE,
});

// Attach token from localStorage to every request
api.interceptors.request.use((config) => {
  try{
    const token = localStorage.getItem('kshetra_token');
    if(token){
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }
  }catch(e){ }
  return config;
});

export async function register(user) {
  return api.post('/auth/register', user);
}

export async function login(form) {
  // OAuth2PasswordRequestForm expects form-encoded data: username & password
  const params = new URLSearchParams();
  params.append('username', form.email);
  params.append('password', form.password);
  return api.post('/auth/login', params, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } });
}
