import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Register from './pages/Register';
import Login from './pages/Login';
import StudentProfile from './pages/StudentProfile';
import Dashboard from './pages/Dashboard';
import Skills from './pages/Skills';
import Careers from './pages/Careers';
import Assessments from './pages/Assessments';
import TakeAssessment from './pages/TakeAssessment';
import PracticalTasks from './pages/PracticalTasks';
import Passport from './pages/Passport';
import SkillGaps from './pages/SkillGaps';
import RecruiterDashboard from './pages/RecruiterDashboard';
import Home from './pages/Home';

export default function App(){
  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="p-4 bg-white shadow-sm">
        <Link to="/" className="font-bold mr-4">Kshetra</Link>
        <Link to="/register" className="mr-2">Register</Link>
        <Link to="/login" className="mr-2">Login</Link>
        <Link to="/profile" className="mr-2">Profile</Link>
        <Link to="/dashboard" className="mr-2">Dashboard</Link>
        <Link to="/skills" className="mr-2">Skills</Link>
        <Link to="/careers" className="mr-2">Careers</Link>
        <Link to="/assessments" className="mr-2">Assessments</Link>
        <Link to="/practical" className="mr-2">Practical</Link>
        <Link to="/passport" className="mr-2">Passport</Link>
        <Link to="/recruiter" className="mr-2">Recruiter</Link>
      </nav>
      <main className="p-6">
        <Routes>
          <Route path="/register" element={<Register />} />
          <Route path="/login" element={<Login />} />
          <Route path="/profile" element={<StudentProfile />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/skills" element={<Skills />} />
          <Route path="/careers" element={<Careers />} />
          <Route path="/assessments" element={<Assessments />} />
          <Route path="/assessments/:id" element={<TakeAssessment />} />
          <Route path="/practical" element={<PracticalTasks />} />
          <Route path="/passport" element={<Passport />} />
          <Route path="/skill-gaps" element={<SkillGaps />} />
          <Route path="/recruiter" element={<RecruiterDashboard />} />
          <Route path="/" element={<Home />} />
        </Routes>
      </main>
    </div>
  )
}
