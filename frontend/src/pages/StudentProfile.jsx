import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function StudentProfile(){
  const [profile, setProfile] = useState(null);
  const [userId, setUserId] = useState(null);
  const [bio, setBio] = useState('');
  const [location, setLocation] = useState('');
  const [message, setMessage] = useState('');

  useEffect(()=>{
    // try to read user id from localStorage demo token mapping
    const token = localStorage.getItem('kshetra_token');
    const rawUserId = localStorage.getItem('kshetra_user_id');
    if(rawUserId) setUserId(Number(rawUserId));
  },[])

  async function loadProfile(){
    if(!userId) return;
    try{
      const resp = await api.get(`/students/${userId}`);
      setProfile(resp.data);
      setBio(resp.data.bio || '');
      setLocation(resp.data.location || '');
    }catch(err){
      setMessage('Profile not found');
    }
  }

  useEffect(()=>{ loadProfile() }, [userId]);

  async function createProfile(e){
    e.preventDefault();
    try{
      const payload = { user_id: userId, bio, location };
      const resp = await api.post('/students/create', payload);
      setProfile(resp.data);
      setMessage('Profile created');
    }catch(err){ setMessage(err?.response?.data?.detail || 'Failed'); }
  }

  async function updateProfile(e){
    e.preventDefault();
    try{
      const payload = { bio, location };
      const resp = await api.put(`/students/${userId}`, payload);
      setProfile(resp.data);
      setMessage('Profile updated');
    }catch(err){ setMessage(err?.response?.data?.detail || 'Failed'); }
  }

  return (
    <div className="max-w-3xl mx-auto bg-white p-6 rounded shadow">
      <h2 className="text-xl font-bold mb-4">Student Profile</h2>
      {!userId && <p className="mb-2">No user id found in demo storage. After registering, store your user id in localStorage under key 'kshetra_user_id'.</p>}
      {profile ? (
        <div>
          <p><strong>Name:</strong> {profile.user.full_name || '—'}</p>
          <p><strong>Email:</strong> {profile.user.email}</p>
        </div>
      ) : null}

      <form onSubmit={profile ? updateProfile : createProfile} className="mt-4">
        <label className="block">Bio</label>
        <textarea className="w-full border p-2 mb-2" value={bio} onChange={e=>setBio(e.target.value)} />
        <label className="block">Location</label>
        <input className="w-full border p-2 mb-4" value={location} onChange={e=>setLocation(e.target.value)} />
        <div>
          <button className="bg-blue-600 text-white px-4 py-2 rounded mr-2" type="submit">{profile ? 'Update Profile' : 'Create Profile'}</button>
          <button type="button" className="bg-gray-200 px-4 py-2 rounded" onClick={loadProfile}>Reload</button>
        </div>
      </form>

      {message && <p className="mt-4">{message}</p>}
    </div>
  )
}
