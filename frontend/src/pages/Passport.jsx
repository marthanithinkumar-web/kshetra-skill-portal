import React, { useEffect, useState } from 'react';
import { getPassport, runVerification } from '../services/verifications';

export default function Passport(){
  const [passport, setPassport] = useState(null);
  const [userId, setUserId] = useState(null);
  const [message, setMessage] = useState('');

  useEffect(()=>{
    const rawUserId = localStorage.getItem('kshetra_user_id');
    if(rawUserId) setUserId(Number(rawUserId));
  },[])

  useEffect(()=>{ if(userId) load(); }, [userId]);

  async function load(){
    const resp = await getPassport(userId);
    setPassport(resp.data);
  }

  async function verifySkill(skillId){
    const resp = await runVerification({ student_id: userId, skill_id: skillId });
    setMessage('Verified: ' + resp.data.verified_level + ' Score: ' + Math.round(resp.data.score));
    load();
  }

  if(!userId) return <div className="p-6">Set localStorage kshetra_user_id for demo</div>

  return (
    <div className="max-w-5xl mx-auto p-6">
      <h2 className="text-2xl font-bold mb-4">Skill Passport</h2>
      {!passport && <div>Loading...</div>}
      {passport && (
        <div>
          <div className="bg-white p-4 rounded shadow mb-4">
            <div className="text-lg font-semibold">{passport.student.name}</div>
            <div className="text-sm text-gray-600">Target: {passport.target_career || '—'}</div>
            <div className="mt-2">Career Readiness: <strong>{Math.round(passport.career_readiness)}%</strong></div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {passport.skills.map(s=>(
              <div key={s.skill_id} className="bg-white p-4 rounded shadow">
                <div className="flex justify-between items-center">
                  <div>
                    <div className="font-semibold text-lg">{s.skill_name}</div>
                    <div className="text-sm text-gray-600">{s.verified_level || 'Unverified'}</div>
                  </div>
                  <div className="text-right">
                    <div className="text-2xl font-bold">{s.score ? Math.round(s.score) : '—'}</div>
                    <div className="text-xs text-gray-500">Confidence {s.confidence ? Math.round(s.confidence) : '—'}%</div>
                  </div>
                </div>
                <div className="mt-3">
                  <button className="bg-blue-600 text-white px-3 py-1 rounded" onClick={()=>verifySkill(s.skill_id)}>Re-run Verification</button>
                </div>
              </div>
            ))}
          </div>

          {message && <p className="mt-4">{message}</p>}
        </div>
      )}
    </div>
  )
}
