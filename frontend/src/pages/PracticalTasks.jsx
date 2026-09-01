import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import { createPractical, submitPractical } from '../services/assessments';

export default function PracticalTasks(){
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [skillId, setSkillId] = useState(null);
  const [repoUrl, setRepoUrl] = useState('');
  const [message, setMessage] = useState('');
  const userId = Number(localStorage.getItem('kshetra_user_id')) || null;

  useEffect(()=>{ load(); }, []);
  async function load(){
    const resp = await api.get('/assessments');
    setTasks(resp.data);
  }

  async function create(e){
    e.preventDefault();
    await createPractical({ title, description, skill_id: Number(skillId) });
    setMessage('Task created');
    load();
  }

  async function submit(e, taskId){
    e.preventDefault();
    if(!userId){ alert('Set user id'); return; }
    const payload = { task_id: taskId, student_id: userId, submission_text: description, repo_url: repoUrl };
    const resp = await submitPractical(payload);
    setMessage('Submitted. Score: ' + resp.data.score);
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded shadow">
      <h2 className="font-bold mb-4">Practical Tasks</h2>
      <form onSubmit={create} className="mb-4">
        <input className="border p-2 w-full mb-2" placeholder="Title" value={title} onChange={e=>setTitle(e.target.value)} />
        <textarea className="border p-2 w-full mb-2" placeholder="Description" value={description} onChange={e=>setDescription(e.target.value)} />
        <input className="border p-2 w-full mb-2" placeholder="Skill Id" value={skillId||''} onChange={e=>setSkillId(e.target.value)} />
        <button className="bg-blue-600 text-white px-4 py-2 rounded">Create Task</button>
      </form>

      <div>
        <h3 className="font-semibold">Available Tasks</h3>
        <ul>
          {tasks.map(t=>(
            <li key={t.id} className="mb-2">
              <div className="flex justify-between">
                <div>
                  <div className="font-semibold">{t.title}</div>
                  <div className="text-sm text-gray-600">{t.description}</div>
                </div>
                <div>
                  <form onSubmit={(e)=>submit(e,t.id)}>
                    <input className="border p-2 mr-2" placeholder="Repo URL" value={repoUrl} onChange={e=>setRepoUrl(e.target.value)} />
                    <button className="bg-green-600 text-white px-3 py-1 rounded">Submit</button>
                  </form>
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
      {message && <p className="mt-2">{message}</p>}
    </div>
  )
}
