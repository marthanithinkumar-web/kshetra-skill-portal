import React from 'react';
import { Link } from 'react-router-dom';

const metrics = [
  { label: 'Verified skill passports', value: '24K+' },
  { label: 'College partners', value: '180+' },
  { label: 'Skill match accuracy', value: '92%' },
  { label: 'Hiring response lift', value: '3.7x' },
];

const featureCards = [
  { title: 'Skill Passport', text: 'Convert academic achievement, projects, GitHub activity, and coding progress into an evidence-backed skill profile.' },
  { title: 'Career Intelligence', text: 'Spot role-fit gaps early and prioritize the most relevant internship or placements for each student profile.' },
  { title: 'Mentor Insights', text: 'Help colleges and faculty guide interventions using data, readiness signals, and skill-level trends.' },
  { title: 'Recruiter Access', text: 'Give industry teams a clean shortlist based on verified readiness instead of static resumes alone.' },
];

const workflowSteps = [
  { title: 'Create profile', text: 'Students capture academic history, interests, projects, and coding evidence in one place.' },
  { title: 'Verify skills', text: 'AI matches public evidence and assessment signals to create a transparent skill passport.' },
  { title: 'Gap analysis', text: 'The platform surfaces the missing capabilities and the next skill milestones to target.' },
  { title: 'Internship match', text: 'Students get relevant internship, hiring, and learning opportunities mapped to their readiness.' },
];

const categories = ['Profile', 'Skill Check', 'Internships', 'Placements', 'Roadmaps', 'Recruiter view'];

export default function Home() {
  return (
    <div className="page-shell home-page">
      <section className="hero-section">
        <div className="hero-grid">
          <div className="hero-copy">
            <span className="eyebrow">AI skill verification platform</span>
            <h1>Turn learning into a verified future.</h1>
            <p>
              Kshetra gives students, mentors, and recruiters a single source of truth for skill evidence, career readiness, and internship opportunities.
            </p>

            <div className="hero-actions">
              <Link to="/register" className="primary-button">Start demo</Link>
              <Link to="/dashboard" className="secondary-button">Open dashboard</Link>
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

              <div className="mini-chart" aria-label="Readiness chart">
                <span style={{ height: '46%' }} />
                <span style={{ height: '60%' }} />
                <span style={{ height: '72%' }} />
                <span style={{ height: '84%' }} />
                <span style={{ height: '92%' }} />
                <span style={{ height: '100%' }} />
              </div>

              <div className="skill-tags">
                <span>DSA</span>
                <span>SQL</span>
                <span>Problem Solving</span>
              </div>
            </div>

            <div className="glass-card floating-panel">
              <div className="panel-row">
                <span>Current track</span>
                <span className="tag success">On track</span>
              </div>
              <strong>Product analytics roadmap</strong>
              <small>Priority skills: SQL, BI, Python, communication</small>
            </div>
          </div>
        </div>
      </section>

      <section className="feature-section">
        <div className="section-heading">
          <span className="eyebrow dark">What Kshetra offers</span>
          <h2>Built for modern student success journeys.</h2>
        </div>

        <div className="feature-grid">
          {featureCards.map((feature) => (
            <div key={feature.title} className="feature-card">
              <div className="feature-icon">✦</div>
              <div>
                <h3>{feature.title}</h3>
                <p>{feature.text}</p>
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="feature-section alt-section">
        <div className="section-heading narrow">
          <span className="eyebrow dark">How the prototype works</span>
          <h2>A practical workflow from profile to placement signal.</h2>
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

      <section className="portal-preview-section">
        <div className="portal-preview-card">
          <div className="portal-panel-head">
            <div>
              <span className="eyebrow dark">Portal overview</span>
              <h3>One interface for students, colleges, and recruiters.</h3>
            </div>
            <Link to="/login" className="primary-button small">Open portal</Link>
          </div>

          <div className="portal-grid">
            <div className="portal-column">
              <div className="mini-stat">
                <span>Active profiles</span>
                <strong>15,420</strong>
              </div>
              <div className="mini-stat">
                <span>Internship matches</span>
                <strong>3,840</strong>
              </div>
            </div>

            <div className="portal-list-box">
              {categories.map((category) => (
                <div key={category} className="list-pill">
                  {category}
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="demo-flow-section">
        <div className="demo-flow-header">
          <span className="eyebrow dark">Demo flow</span>
          <h3>Judge-friendly prototype journey</h3>
        </div>

        <div className="demo-flow-grid">
          <div className="demo-flow-step">
            <span>01</span>
            <strong>Register</strong>
            <p>Create an account and enter the student profile details.</p>
          </div>
          <div className="demo-flow-step">
            <span>02</span>
            <strong>Login</strong>
            <p>Sign in to access the student portal and dashboard.</p>
          </div>
          <div className="demo-flow-step">
            <span>03</span>
            <strong>Dashboard</strong>
            <p>View readiness, roadmaps, skills, and opportunity matches.</p>
          </div>
          <div className="demo-flow-step">
            <span>04</span>
            <strong>Passport</strong>
            <p>See the verified skill passport and progression narrative.</p>
          </div>
        </div>
      </section>

      <section className="cta-strip">
        <div>
          <span className="eyebrow dark">Create better outcomes</span>
          <h3>Give students a trustworthy profile and show readiness in real time.</h3>
        </div>
        <Link to="/login" className="primary-button">Launch portal</Link>
      </section>
    </div>
  );
}
