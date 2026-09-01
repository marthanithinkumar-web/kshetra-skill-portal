import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function SkillGaps(){
  const [data, setData] = useState(null);
  const [userId, setUserId] = useState(null);

  useEffect(()=>{
    const rawUserId = localStorage.getItem('kshetra_user_id');
    if(rawUserId) setUserId(Number(rawUserId));
  },[])

  async function load(){
    if(!userId) return;
    const resp = await api.get(`/skill-gaps/${userId}`);
    setData(resp.data);
  }

  useEffect(()=>{ if(userId) load(); }, [userId]);

  if(!userId) return <div className="p-6">Set localStorage kshetra_user_id for demo</div>

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Skill Gaps & Roadmap</h2>
      {!data && <div>Loading...</div>}
      {data && (
        <div>
          <div className="bg-white p-4 rounded shadow mb-4">
            <div className="font-semibold">Career: {data.career.name}</div>
          </div>
          <div className="bg-white p-4 rounded shadow mb-4">
            <h3 className="font-bold">Skill Gaps</h3>
            <ul>
              {data.skill_gaps.map(s=>(
                <li key={s.skill_id} className="flex justify-between items-center py-2 border-b">
                  <div>
                    <div className="font-semibold">{s.skill_name}</div>
                    <div className="text-sm text-gray-600">Required: {s.required_level} — Current: {s.current_level}</div>
                  </div>
                  <div className="text-right">
                    <div className={`px-2 py-1 rounded ${s.priority==='High'?'bg-red-100 text-red-800':'bg-yellow-100 text-yellow-800'}`}>{s.priority}</div>
                  </div>
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-white p-4 rounded shadow">
            <h3 className="font-bold">Personalized Roadmap</h3>
            <ol className="mt-2">
              {data.roadmap.items.map(it=>(
                <li key={it.skill_id} className="mb-3">
                  <div className="font-semibold">{it.skill_name} — {it.priority}</div>
                  <div className="text-sm text-gray-700">From {it.current_level} → {it.target_level}</div>
                  <div className="mt-2">
                    <ul className="list-disc ml-6 text-sm">
                      {it.recommendations.map((r,idx)=>(<li key={idx}>{r}</li>))}
                    </ul>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        </div>
      )}
    </div>
  )
}
