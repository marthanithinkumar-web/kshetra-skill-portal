import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function Skills(){
  const [skills, setSkills] = useState([]);
  const [name, setName] = useState('');
  const [message, setMessage] = useState('');

  useEffect(()=>{ load(); }, []);

  async function load(){
    const resp = await api.get('/skills');
    setSkills(resp.data);
  }

  async function create(e){
    e.preventDefault();
    try{
      await api.post('/skills', { name });
      setMessage('Skill created');
      setName('');
      load();
    }catch(err){ setMessage(err?.response?.data?.detail || 'Failed'); }
  }

  return (
    <div className="max-w-3xl mx-auto p-6 bg-white rounded shadow">
      <h2 className="font-bold mb-4">Skills</h2>
      <form onSubmit={create} className="mb-4">
        <input className="border p-2 mr-2" value={name} onChange={e=>setName(e.target.value)} placeholder="Skill name" />
        <button className="bg-blue-600 text-white px-3 py-1 rounded">Create</button>
      </form>
      <ul>
        {skills.map(s=>(<li key={s.id}>{s.name}</li>))}
      </ul>
      {message && <p className="mt-2">{message}</p>}
    </div>
  )
}
