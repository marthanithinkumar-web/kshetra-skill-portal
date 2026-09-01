import React, { useState } from 'react';
import { register } from '../services/api';

export default function Register(){
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [password, setPassword] = useState('');
  const [roleId, setRoleId] = useState(1);
  const [message, setMessage] = useState('');

  async function handleSubmit(e){
    e.preventDefault();
    try{
      const payload = { email, full_name: fullName, password, role_id: roleId };
      const resp = await register(payload);
      setMessage('Registration successful. You can login now.');
    }catch(err){
      setMessage(err?.response?.data?.detail || 'Registration failed');
    }
  }

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded shadow">
      <h2 className="text-xl font-bold mb-4">Student Register (Demo)</h2>
      <form onSubmit={handleSubmit}>
        <label className="block">Email</label>
        <input className="w-full border p-2 mb-2" value={email} onChange={e=>setEmail(e.target.value)} />
        <label className="block">Full name</label>
        <input className="w-full border p-2 mb-2" value={fullName} onChange={e=>setFullName(e.target.value)} />
        <label className="block">Password</label>
        <input type="password" className="w-full border p-2 mb-2" value={password} onChange={e=>setPassword(e.target.value)} />
        <label className="block">Role</label>
        <select className="w-full border p-2 mb-4" value={roleId} onChange={e=>setRoleId(Number(e.target.value))}>
          <option value={1}>Student</option>
          <option value={2}>College/TPO</option>
          <option value={3}>Recruiter</option>
          <option value={4}>Platform Admin</option>
        </select>
        <button className="bg-blue-600 text-white px-4 py-2 rounded">Register</button>
      </form>
      {message && <p className="mt-4">{message}</p>}
    </div>
  )
}
