import React, { useEffect, useState } from 'react';
import { getAssessment, submitAttempt } from '../services/assessments';
import { useParams } from 'react-router-dom';

export default function TakeAssessment(){
  const { id } = useParams();
  const [assessment, setAssessment] = useState(null);
  const [answers, setAnswers] = useState({});
  const userId = Number(localStorage.getItem('kshetra_user_id')) || null;
  useEffect(()=>{ if(id) load(); }, [id]);

  async function load(){
    const resp = await getAssessment(id);
    setAssessment(resp.data);
  }

  function setAnswer(qid, val){
    setAnswers(prev=>({ ...prev, [qid]: val }))
  }

  async function submit(e){
    e.preventDefault();
    if(!userId){ alert('Set kshetra_user_id in localStorage'); return; }
    const payload = { assessment_id: Number(id), student_id: userId, answers: Object.keys(answers).map(k=>({ question_id: Number(k), response: answers[k] })) }
    const resp = await submitAttempt(payload);
    alert('Score: ' + resp.data.score);
  }

  if(!assessment) return <div className="p-6">Loading...</div>
  return (
    <div className="max-w-3xl mx-auto p-6 bg-white rounded shadow">
      <h2 className="font-bold mb-4">{assessment.title}</h2>
      <form onSubmit={submit}>
        {assessment.questions.map(q=>(
          <div key={q.id} className="mb-4">
            <div className="font-semibold">{q.prompt}</div>
            {q.choices ? (
              JSON.parse(q.choices).map((c,idx)=> (
                <label key={idx} className="block"><input type="radio" name={q.id} onChange={()=>setAnswer(q.id, c)} /> {c}</label>
              ))
            ) : (
              <input className="w-full border p-2" onChange={e=>setAnswer(q.id, e.target.value)} />
            )}
          </div>
        ))}
        <button className="bg-green-600 text-white px-4 py-2 rounded">Submit</button>
      </form>
    </div>
  )
}
