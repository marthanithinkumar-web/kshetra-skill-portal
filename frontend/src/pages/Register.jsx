import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { register } from '../services/api';

export default function Register() {
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [roleId, setRoleId] = useState(1);
  const [message, setMessage] = useState('');

  async function handleSubmit(e) {
    e.preventDefault();

    if (!fullName.trim() || !email.trim()) {
      setMessage('Please enter your full name and email address.');
      return;
    }

    if (password.length < 6) {
      setMessage('Password must be at least 6 characters long.');
      return;
    }

    if (password !== confirmPassword) {
      setMessage('Passwords do not match.');
      return;
    }

    try {
      const payload = { email: email.trim(), full_name: fullName.trim(), password, role_id: roleId };
      await register(payload);
      setMessage('Registration successful. You can now login to your portal.');
      setTimeout(() => {
        window.location.hash = '#/login';
      }, 800);
    } catch (err) {
      setMessage(err?.response?.data?.detail || 'Registration failed');
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-shell register-shell">
        <aside className="auth-cta register-cta">
          <div className="auth-brand">
            <span className="brand-icon">K</span>
            <span>Kshetra</span>
          </div>

          <div className="auth-copy">
            <span className="eyebrow dark">Join the platform</span>
            <h1>Create a verified student profile.</h1>
            <p>
              Set up your identity, connect your academic profile, and start building a skill passport trusted by recruiters and mentors.
            </p>
          </div>

          <div className="auth-meta-list">
            <div>
              <strong>AI skill mapping</strong>
              <span>Convert academic and project work into measurable strengths</span>
            </div>
            <div>
              <strong>Opportunity matching</strong>
              <span>Discover internships and roles aligned to your profile</span>
            </div>
            <div>
              <strong>Career readiness</strong>
              <span>Track the exact roadmap needed to move forward</span>
            </div>
          </div>
        </aside>

        <section className="auth-panel register-panel">
          <div className="auth-header">
            <span className="eyebrow dark">Create account</span>
            <h2>Register</h2>
          </div>

          <form className="auth-form" onSubmit={handleSubmit}>
            <div className="field-grid">
              <label>
                <span>Full name</span>
                <input
                  type="text"
                  value={fullName}
                  placeholder="Your full name"
                  onChange={(e) => setFullName(e.target.value)}
                  required
                />
              </label>

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
            </div>

            <div className="field-grid">
              <label>
                <span>Password</span>
                <input
                  type="password"
                  value={password}
                  placeholder="Create a password"
                  onChange={(e) => setPassword(e.target.value)}
                  required
                />
              </label>

              <label>
                <span>Confirm password</span>
                <input
                  type="password"
                  value={confirmPassword}
                  placeholder="Repeat your password"
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  required
                />
              </label>
            </div>

            <label>
              <span>Select role</span>
              <select
                className="auth-select"
                value={roleId}
                onChange={(e) => setRoleId(Number(e.target.value))}
              >
                <option value={1}>Student</option>
                <option value={2}>College / TPO</option>
                <option value={3}>Recruiter</option>
                <option value={4}>Platform Admin</option>
              </select>
            </label>

            <div className="form-row register-row">
              <label className="checkbox-row">
                <input type="checkbox" defaultChecked />
                <span>I agree to the platform terms</span>
              </label>
              <Link to="/login">Already signed in?</Link>
            </div>

            <button type="submit" className="primary-button auth-button">Create account</button>
          </form>

          <div className="auth-divider"><span>or</span></div>
          <div className="account-switch">
            <span>Already have an account?</span>
            <Link to="/login">Go to login</Link>
          </div>

          {message && <p className="form-message">{message}</p>}
        </section>
      </div>
    </div>
  );
}
