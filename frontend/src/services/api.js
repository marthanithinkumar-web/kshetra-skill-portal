import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export function isDemoMode() {
  try {
    const host = window.location.hostname;
    return host !== 'localhost' && host !== '127.0.0.1';
  } catch (e) {
    return true;
  }
}

function getDemoRoleName(roleId) {
  const map = {
    1: 'student',
    2: 'college',
    3: 'recruiter',
    4: 'admin',
  };
  return map[roleId] || 'student';
}

function buildDemoProfile(form) {
  const email = (form?.email || form?.full_name || 'student@college.edu').toLowerCase();
  return {
    email,
    full_name: form?.full_name || 'Demo Student',
    id: Date.now(),
    is_active: true,
    created_at: new Date().toISOString(),
    role: { id: form?.role_id || 1, name: getDemoRoleName(form?.role_id || 1), description: 'Student / Learner' },
    target_career_id: 3,
  };
}

export const api = axios.create({
  baseURL: API_BASE,
});

api.interceptors.request.use((config) => {
  try {
    const token = localStorage.getItem('kshetra_token');
    if (token) {
      config.headers = config.headers || {};
      config.headers.Authorization = `Bearer ${token}`;
    }
  } catch (e) {
    // ignore localStorage errors in browser privacy mode
  }
  return config;
});

export async function register(user) {
  if (isDemoMode()) {
    const profile = buildDemoProfile(user);
    localStorage.setItem('kshetra_demo_user', JSON.stringify(profile));
    return Promise.resolve({ data: profile });
  }

  return api.post('/auth/register', user);
}

export async function login(form) {
  if (isDemoMode()) {
    const stored = JSON.parse(localStorage.getItem('kshetra_demo_user') || 'null');
    const email = (form.email || '').trim().toLowerCase();
    const password = form.password || '';

    if (stored && stored.email === email && password.length >= 6) {
      const token = `demo-token-${Date.now()}`;
      localStorage.setItem('kshetra_token', token);
      localStorage.setItem('kshetra_user_id', String(stored.id));
      return Promise.resolve({ data: { access_token: token, token_type: 'bearer' } });
    }

    const fallbackProfile = buildDemoProfile({ email, full_name: email.split('@')[0], role_id: 1 });
    localStorage.setItem('kshetra_demo_user', JSON.stringify(fallbackProfile));
    const token = `demo-token-${Date.now()}`;
    localStorage.setItem('kshetra_token', token);
    localStorage.setItem('kshetra_user_id', String(fallbackProfile.id));
    return Promise.resolve({ data: { access_token: token, token_type: 'bearer' } });
  }

  const params = new URLSearchParams();
  params.append('username', form.email);
  params.append('password', form.password);
  return api.post('/auth/login', params, { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } });
}
