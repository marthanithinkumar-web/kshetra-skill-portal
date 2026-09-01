import { api } from './api';

export function listAssessments(){
  return api.get('/assessments');
}

export function getAssessment(id){
  return api.get(`/assessments/${id}`);
}

export function submitAttempt(payload){
  return api.post('/assessments/attempt', payload);
}

export function createPractical(payload){
  return api.post('/assessments/practical', payload);
}

export function submitPractical(payload){
  return api.post('/assessments/practical/submit', payload);
}
