import React, { useEffect, useState } from 'react';
import { listAssessments } from '../services/assessments';
import { Link } from 'react-router-dom';

export default function Assessments(){
  const [assessments, setAssessments] = useState([]);

  useEffect(()=>{ load(); }, []);

  async function load(){
    const resp = await listAssessments();
    setAssessments(resp.data);
  }

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded shadow">
      <h2 className="font-bold mb-4">Assessments</h2>
      <ul>
        {assessments.map(a=>(
          <li key={a.id} className="mb-2">
            <div className="flex justify-between items-center">
              <div>
                <div className="font-semibold">{a.title}</div>
                <div className="text-sm text-gray-600">{a.description}</div>
              </div>
              <div>
                <Link to={`/assessments/${a.id}`} className="text-blue-600">Take</Link>
              </div>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
