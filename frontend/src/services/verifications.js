import { api } from './api';

export function runVerification(payload){
  return api.post('/verifications/run', payload);
}

export function getPassport(studentId){
  return api.get(`/verifications/passport/${studentId}`);
}

export function getHistory(studentSkillId){
  return api.get(`/verifications/history/${studentSkillId}`);
}
