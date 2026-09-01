import { api } from './api';

export function createProfile(payload){
  return api.post('/students/create', payload);
}

export function getProfile(userId){
  return api.get(`/students/${userId}`);
}

export function updateProfile(userId, payload){
  return api.put(`/students/${userId}`, payload);
}

export function addEducation(userId, payload){
  return api.post(`/students/${userId}/education`, payload);
}

export function addCertification(userId, payload){
  return api.post(`/students/${userId}/certifications`, payload);
}

export function addProject(userId, payload){
  return api.post(`/students/${userId}/projects`, payload);
}

export function addSkill(userId, payload){
  return api.post(`/students/${userId}/skills`, payload);
}

export function dashboard(userId){
  return api.get(`/students/${userId}/dashboard`);
}
