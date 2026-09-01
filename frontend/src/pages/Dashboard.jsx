import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function Dashboard(){
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(()=>{ load(); }, []);

  async function load(){
    try{
      setLoading(true);
      const resp = await api.get(`/students/me`);
      const skillsResp = await api.get('/students/me/skills');
      const roadmapResp = await api.get('/students/me/roadmap');
      const oppResp = await api.get('/students/me/opportunities');
      const assessmentsResp = await api.get('/students/me/assessments');
      setData({ profile: resp.data, skills: skillsResp.data, roadmap: roadmapResp.data, opportunities: oppResp.data, assessments: assessmentsResp.data });
    }catch(err){
      console.error('Error loading dashboard', err);
    }finally{
      setLoading(false);
    }
  }

  if(loading) return <div className="max-w-3xl mx-auto p-6">Loading...</div>

  if(!data || !data.profile) return <div className="max-w-3xl mx-auto p-6">No profile found. Complete your profile.</div>

  const student = data.profile;
  const name = student.user.full_name || 'Student';

  return (
    <div className="max-w-6xl mx-auto p-6">
      <header className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold">Welcome back, {name}</h1>
          <p className="text-sm text-gray-600">Target career: {student.target_career_id ? `Career ID ${student.target_career_id}` : 'Not set'}</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="text-center">
            <div className="text-gray-500 text-sm">Career Readiness</div>
            <div className="text-xl font-bold">{Math.round((data.skills.reduce((acc,s)=>acc + (s.score||0),0) / (data.skills.length||1)) || 0)}%</div>
          </div>
          <div className="text-center">
            <div className="text-gray-500 text-sm">Verified Skills</div>
            <div className="text-xl font-bold">{data.skills.filter(s=>s.verified_level).length}</div>
          </div>
        </div>
      </header>

      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="col-span-2 bg-white p-4 rounded shadow">
          <h3 className="font-bold mb-2">Skills</h3>
          {data.skills.length === 0 && <div className="text-gray-600">You haven't added any skills yet</div>}
          <ul>
            {data.skills.map((s,i)=> (
              <li key={i} className="border-b py-2 flex justify-between">
                <div>
                  <div className="font-semibold">{s.skill_name}</div>
                  <div className="text-sm text-gray-500">Claimed: {s.claimed_level || '—'}</div>
                </div>
                <div className="text-right">
                  <div className="font-semibold">{s.verified_level || 'Not verified'}</div>
                  <div className="text-sm text-gray-500">Score: {s.score || '—'} | Confidence: {s.confidence || '—'}</div>
                  <div className="text-sm text-gray-400">Last: {s.last_verified_at || '—'}</div>
                </div>
              </li>
            ))}
          </ul>
        </div>

        <aside className="bg-white p-4 rounded shadow">
          <h3 className="font-bold mb-2">Roadmap</h3>
          {!data.roadmap && <div className="text-gray-600">No roadmap yet. Complete assessments to generate one.</div>}
          {data.roadmap && data.roadmap.items.map((it,i)=>(
            <div key={i} className="mb-2">
              <div className="font-semibold">{it.skill_name}</div>
              <div className="text-sm text-gray-500">{it.current_level} → {it.target_level} | Priority: {it.priority}</div>
            </div>
          ))}
        </aside>
      </div>

      <section className="bg-white p-4 rounded shadow mb-6">
        <h3 className="font-bold mb-2">Opportunities</h3>
        <div className="grid md:grid-cols-2 gap-4">
          {data.opportunities.jobs.map((j,i)=>(
            <div key={i} className="border p-3 rounded">
              <div className="font-semibold">{j.title}</div>
              <div className="text-sm text-gray-500">{j.company} · {j.location}</div>
            </div>
          ))}
        </div>
      </section>

      <section className="bg-white p-4 rounded shadow">
        <h3 className="font-bold mb-2">Recent Assessments</h3>
        {!data.assessments.length && <div className="text-gray-600">No assessments taken yet.</div>}
        {data.assessments.map((a,i)=>(
          <div key={i} className="border-b py-2">Assessment {a.assessment_id} — Score: {a.score || '—'}</div>
        ))}
      </section>
    </div>
  )
}
