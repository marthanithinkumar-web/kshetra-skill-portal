import React, { useEffect, useState } from 'react';
import { createCompany, createJob, searchCandidates, listApplications, viewEvidence } from '../services/recruiter';

export default function RecruiterDashboard(){
  const [companyName, setCompanyName] = useState('');
  const [companyMsg, setCompanyMsg] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [jobMsg, setJobMsg] = useState('');
  const [requirements, setRequirements] = useState([{ skill_name: 'SQL', min_level: 'Intermediate' }, { skill_name: 'Python', min_level: 'Intermediate' }]);
  const [candidates, setCandidates] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [evidence, setEvidence] = useState(null);

  async function createCompanyHandler(e){
    e.preventDefault();
    try{
      const resp = await createCompany({ name: companyName });
      setCompanyMsg('Company created: ' + resp.data.name);
    }catch(err){ setCompanyMsg('Failed'); }
  }

  async function createJobHandler(e){
    e.preventDefault();
    try{
      const resp = await createJob({ company_id: 1, title: jobTitle, required_skills: requirements });
      setJobMsg('Job created: ' + resp.data.title);
    }catch(err){ setJobMsg('Failed'); }
  }

  async function search(){
    const resp = await searchCandidates({ requirements });
    setCandidates(resp.data);
  }

  async function loadEvidence(student_id){
    setSelectedStudent(student_id);
    const resp = await viewEvidence(student_id);
    setEvidence(resp.data);
  }

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Recruiter Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-semibold mb-2">Create Company</h3>
          <form onSubmit={createCompanyHandler}>
            <input className="border p-2 w-full mb-2" value={companyName} onChange={e=>setCompanyName(e.target.value)} placeholder="Company name" />
            <button className="bg-blue-600 text-white px-3 py-1 rounded">Create</button>
          </form>
          {companyMsg && <div className="mt-2">{companyMsg}</div>}
        </div>

        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-semibold mb-2">Create Job</h3>
          <form onSubmit={createJobHandler}>
            <input className="border p-2 w-full mb-2" value={jobTitle} onChange={e=>setJobTitle(e.target.value)} placeholder="Job title" />
            <button className="bg-green-600 text-white px-3 py-1 rounded">Create Job</button>
          </form>
          {jobMsg && <div className="mt-2">{jobMsg}</div>}
        </div>
      </div>

      <div className="bg-white p-4 rounded shadow mt-4">
        <h3 className="font-semibold mb-2">Candidate Search</h3>
        <div className="mb-2">Search requirements (demo):</div>
        <div className="mb-2">
          {requirements.map((r,i)=>(<div key={i} className="text-sm">{r.skill_name} — {r.min_level}</div>))}
        </div>
        <button className="bg-indigo-600 text-white px-3 py-1 rounded" onClick={search}>Search</button>

        <div className="mt-4">
          <h4 className="font-semibold">Results</h4>
          {candidates.map(c=>(
            <div key={c.student_id} className="flex justify-between items-center py-2 border-b">
              <div>
                <div className="font-semibold">{c.name}</div>
                <div className="text-sm text-gray-600">Score: {Math.round(c.match_score)}%</div>
              </div>
              <div>
                <button className="bg-blue-600 text-white px-3 py-1 rounded mr-2" onClick={()=>loadEvidence(c.student_id)}>View Evidence</button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {evidence && (
        <div className="bg-white p-4 rounded shadow mt-4">
          <h3 className="font-semibold">Evidence for student {selectedStudent}</h3>
          <pre className="text-sm">{JSON.stringify(evidence, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}
