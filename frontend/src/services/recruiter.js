import { api } from './api';

export function createCompany(payload){
  return api.post('/recruiter/company', payload);
}

export function createJob(payload){
  return api.post('/recruiter/jobs', payload);
}

export function createInternship(payload){
  return api.post('/recruiter/internships', payload);
}

export function searchCandidates(payload){
  return api.post('/recruiter/search', payload);
}

export function viewEvidence(studentId){
  return api.get(`/recruiter/students/${studentId}/evidence`);
}

export function listApplications(jobId){
  return api.get(`/recruiter/jobs/${jobId}/applications`);
}

export function shortlistApplication(applicationId, payload){
  return api.post(`/recruiter/applications/${applicationId}/shortlist`, payload);
}
