import React from 'react';
import { Link } from 'react-router-dom';

const metrics = [
  { label: 'Verified skill passports', value: '24K+' },
  { label: 'Campus partner colleges', value: '180+' },
  { label: 'Career match accuracy', value: '92%' },
  { label: 'Avg. hiring response', value: '3.7x' },
];

const workflowSteps = [
  { title: 'Profile', text: 'Create a student profile with academic background, project history, and coding signals.' },
  { title: 'Assess', text: 'Run structured evaluations and task-based evidence collection across critical skills.' },
  { title: 'Verify', text: 'Apply weighted verification rules for consistent, transparent readiness scoring.' },
  { title: 'Match', text: 'Surface internship and placement opportunities suited to the verified skill passport.' },
];

const featureCards = [
  'Skill Passport Engine',
  'Mentor & TPO Dashboard',
  'Verified Internship Matching',
  'Career Readiness Signals',
  'AI Skill Gap Insights',
  'Recruiter Shortlisting',
];

export default function Home() {
  return (
    <div className="page-shell">
      <section className="hero-section">
        <div className="hero-grid">
          <div className="hero-copy">
            <span className="eyebrow">Smart India Hackathon 2026</span>
            <h1>Kshetra turns talent into evidence-backed career readiness.</h1>
            <p>
              Build student profiles with verified coding, project, and skill evidence — then match them to
              internships, jobs, and growth pathways with clarity.
            </p>
            <div className="hero-actions">
              <Link to="/register" className="primary-button">Get started</Link>
              <Link to="/dashboard" className="secondary-button">View dashboard</Link>
            </div>
            <div className="trust-row">
              {metrics.map((metric) => (
                <div key={metric.label} className="trust-pill">
                  <strong>{metric.value}</strong>
                  <span>{metric.label}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="hero-visual">
            <div className="glass-card primary-panel">
              <div className="profile-topline">
                <span className="status-dot" />
                <span>Career readiness</span>
              </div>
              <div className="score-block">
                <strong>89%</strong>
                <span>Verified Skill Passport</span>
              </div>
              <div className="mini-chart">
                <span style={{ height: '42%' }} />
                <span style={{ height: '58%' }} />
                <span style={{ height: '76%' }} />
                <span style={{ height: '88%' }} />
                <span style={{ height: '92%' }} />
                <span style={{ height: '100%' }} />
              </div>
              <div className="skill-tags">
                <span>DSA</span>
                <span>System Design</span>
                <span>Problem Solving</span>
              </div>
            </div>
            <div className="glass-card floating-panel">
              <div className="panel-row">
                <span className="label">Current focus</span>
                <span className="tag success">On track</span>
              </div>
              <strong>Data Analyst path</strong>
              <small>Priority skills: SQL, Dashboarding, Python</small>
            </div>
          </div>
        </div>
      </section>

      <section className="feature-section">
        <div className="section-heading">
          <span className="eyebrow dark">How Kshetra works</span>
          <h2>From learning signals to verified opportunity matching.</h2>
        </div>
        <div className="steps-grid">
          {workflowSteps.map((step, index) => (
            <div key={step.title} className="info-card">
              <span className="step-number">0{index + 1}</span>
              <h3>{step.title}</h3>
              <p>{step.text}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="feature-section alt-section">
        <div className="section-heading narrow">
          <span className="eyebrow dark">Why teams use it</span>
          <h2>Built for students, college teams, and hiring stakeholders.</h2>
        </div>
        <div className="feature-grid">
          {featureCards.map((feature) => (
            <div key={feature} className="feature-card">
              <div className="feature-icon">✦</div>
              <span>{feature}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="cta-strip">
        <div>
          <span className="eyebrow dark">Transform the talent pipeline</span>
          <h3>Give every student a verified, evidence-backed skill identity.</h3>
        </div>
        <Link to="/register" className="primary-button">Launch portal</Link>
      </section>
    </div>
  );
}
