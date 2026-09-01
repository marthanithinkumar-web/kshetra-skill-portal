import React, { useState } from 'react';
import { login, api } from '../services/api';

export default function Login(){
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  async function handleSubmit(e){
    e.preventDefault();
    try{
      const resp = await login({ email, password });
      const token = resp.data.access_token;
      localStorage.setItem('kshetra_token', token);
      // Optional: fetch profile to cache user id or other info
      try{
        const me = await api.get('/students/me');
        localStorage.setItem('kshetra_user_id', me.data.user_id);
      }catch(e){}
      setMessage('Login successful');
      window.location.href = '/dashboard';
    }catch(err){
      setMessage(err?.response?.data?.detail || 'Login failed');
    }
  }

  return (
    <div className="max-w-md mx-auto bg-white p-6 rounded shadow">
      <h2 className="text-xl font-bold mb-4">Login (Demo)</h2>
      <form onSubmit={handleSubmit}>
        <label className="block">Email</label>
        <input className="w-full border p-2 mb-2" value={email} onChange={e=>setEmail(e.target.value)} />
        <label className="block">Password</label>
        <input type="password" className="w-full border p-2 mb-2" value={password} onChange={e=>setPassword(e.target.value)} />
        <button className="bg-green-600 text-white px-4 py-2 rounded">Login</button>
      </form>
      {message && <p className="mt-4">{message}</p>}
    </div>
  )
}
