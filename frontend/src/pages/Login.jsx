import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { login, api } from '../services/api';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const resp = await login({ email: email.trim(), password });
      const token = resp.data.access_token;
      localStorage.setItem('kshetra_token', token);

      try {
        const me = await api.get('/students/me');
        localStorage.setItem('kshetra_user_id', me.data.user_id);
      } catch (e) {}

      setMessage('Login successful');
      setTimeout(() => {
        window.location.hash = '#/dashboard';
      }, 500);
    } catch (err) {
      setMessage(err?.response?.data?.detail || 'Login failed');
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-shell">
        <aside className="auth-cta">
          <div className="auth-brand">
            <span className="brand-icon">K</span>
            <span>Kshetra</span>
          </div>

          <div className="auth-copy">
            <span className="eyebrow dark">Student career platform</span>
            <h1>Secure access to your verified skill passport.</h1>
            <p>
              Review your progress, track internship readiness, and monitor the learning roadmap built around your true strengths.
            </p>
          </div>

          <div className="auth-meta-list">
            <div>
              <strong>Verified profile</strong>
              <span>Skills linked to evidence and assessments</span>
            </div>
            <div>
              <strong>Placement readiness</strong>
              <span>Career match insights for internships and jobs</span>
            </div>
            <div>
              <strong>Learning roadmap</strong>
              <span>Actionable next steps for each skill gap</span>
            </div>
          </div>

          <div className="auth-stat-card">
            <small>Placement readiness</small>
            <strong>81%</strong>
            <span>Updated this week</span>
          </div>
        </aside>

        <section className="auth-panel">
          <div className="auth-header">
            <span className="eyebrow dark">Portal access</span>
            <h2>Login</h2>
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            <label>
              <span>Email address</span>
              <input
                type="email"
                value={email}
                placeholder="name@college.edu"
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </label>

            <label>
              <span>Password</span>
              <input
                type="password"
                value={password}
                placeholder="Enter your password"
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </label>

            <div className="form-row">
              <label className="checkbox-row">
                <input type="checkbox" defaultChecked />
                <span>Remember me</span>
              </label>
              <Link to="/register">Create account</Link>
            </div>

            <button type="submit" className="primary-button auth-button">Login to portal</button>
          </form>

          <div className="auth-divider"><span>or</span></div>
          <div className="account-switch">
            <span>New to Kshetra?</span>
            <Link to="/register">Create a new account</Link>
          </div>

          {message && <p className="form-message">{message}</p>}
        </section>
      </div>
    </div>
  );
}
