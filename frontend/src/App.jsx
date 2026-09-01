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

export default function App() {
  return (
    <div className="min-h-screen">
      <nav className="top-nav">
        <div className="page-shell nav-shell">
          <Link to="/" className="brand-mark">
            <span className="brand-icon">K</span>
            <span>Kshetra</span>
          </Link>
          <div className="nav-links">
            <Link to="/dashboard">Dashboard</Link>
            <Link to="/skills">Skills</Link>
            <Link to="/careers">Careers</Link>
            <Link to="/passport">Passport</Link>
            <Link to="/recruiter">Recruiters</Link>
          </div>
          <div className="nav-actions">
            <Link to="/login" className="nav-link-button ghost">Login</Link>
            <Link to="/register" className="nav-link-button solid">Register</Link>
          </div>
        </div>
      </nav>

      <main>
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
  );
}
