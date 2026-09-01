import React, { useEffect, useState } from 'react';
import { api, isDemoMode } from '../services/api';

const demoSkills = [
  { name: 'Data Structures', score: 92, level: 'Advanced' },
  { name: 'Python', score: 87, level: 'Strong' },
  { name: 'SQL', score: 79, level: 'Proficient' },
  { name: 'System Design', score: 68, level: 'Developing' },
];

const opportunities = [
  { title: 'Product Analyst Intern', company: 'Nexora Labs', type: 'Remote' },
  { title: 'Data Operations Trainee', company: 'Northstar AI', type: 'Hybrid' },
  { title: 'Frontend Engineer Intern', company: 'Helio Studio', type: 'On-site' },
  { title: 'Business Intelligence Intern', company: 'ValueGrid', type: 'Remote' },
];

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    load();
  }, []);

  async function load() {
    try {
      setLoading(true);

      if (isDemoMode()) {
        setData({
          profile: { user: { full_name: 'Aarav Sharma' }, target_career_id: 3 },
          skills: demoSkills,
          roadmap: { items: [{ skill_name: 'Advanced SQL', current_level: 'Intermediate', target_level: 'Advanced', priority: 'High' }, { skill_name: 'System Design', current_level: 'Beginner', target_level: 'Intermediate', priority: 'Medium' }] },
          opportunities: { jobs: opportunities },
          assessments: [{ assessment_id: 'SQL Sprint', score: 88 }, { assessment_id: 'DSA Diagnostic', score: 92 }],
        });
        return;
      }

      const resp = await api.get('/students/me');
      const skillsResp = await api.get('/students/me/skills');
      const roadmapResp = await api.get('/students/me/roadmap');
      const oppResp = await api.get('/students/me/opportunities');
      const assessmentsResp = await api.get('/students/me/assessments');

      setData({
        profile: resp.data,
        skills: skillsResp.data?.length ? skillsResp.data : demoSkills,
        roadmap: roadmapResp.data,
        opportunities: oppResp.data?.jobs?.length ? oppResp.data : { jobs: opportunities },
        assessments: assessmentsResp.data?.length ? assessmentsResp.data : [{ assessment_id: 'SQL Sprint', score: 88 }, { assessment_id: 'DSA Diagnostic', score: 92 }],
      });
    } catch (err) {
      console.error('Error loading dashboard', err);
      setData({
        profile: { user: { full_name: 'Aarav Sharma' }, target_career_id: 3 },
        skills: demoSkills,
        roadmap: { items: [{ skill_name: 'Advanced SQL', current_level: 'Intermediate', target_level: 'Advanced', priority: 'High' }, { skill_name: 'System Design', current_level: 'Beginner', target_level: 'Intermediate', priority: 'Medium' }] },
        opportunities: { jobs: opportunities },
        assessments: [{ assessment_id: 'SQL Sprint', score: 88 }, { assessment_id: 'DSA Diagnostic', score: 92 }],
      });
    } finally {
      setLoading(false);
    }
  }

  if (loading) return <div className="page-shell dashboard-loading">Loading dashboard...</div>;

  const student = data?.profile || { user: { full_name: 'Student' } };
  const name = student.user?.full_name || 'Student';
  const overallScore = Math.round((data.skills.reduce((acc, s) => acc + (s.score || 0), 0) / (data.skills.length || 1)) || 0);

  return (
    <div className="page-shell dashboard-page">
      <header className="dashboard-topbar">
        <div>
          <span className="eyebrow dark">Welcome back</span>
          <h1>{name}</h1>
          <p>Target career: {student.target_career_id ? `Career ID ${student.target_career_id}` : 'Career not set'}</p>
        </div>
        <div className="summary-cards">
          <div className="pill-card">
            <span>Career readiness</span>
            <strong>{overallScore}%</strong>
          </div>
          <div className="pill-card">
            <span>Verified skills</span>
            <strong>{data.skills.filter((s) => s.score >= 70).length}</strong>
          </div>
        </div>
      </header>

      <div className="dashboard-grid">
        <section className="panel panel-wide">
          <div className="panel-header">
            <h3>Skill Passport</h3>
            <span className="tag success">Live</span>
          </div>
          <div className="skill-list">
            {data.skills.map((s) => (
              <div key={s.name} className="skill-row">
                <div className="skill-meta">
                  <strong>{s.name}</strong>
                  <span>{s.level}</span>
                </div>
                <div className="progress-wrap">
                  <div className="progress-bar">
                    <span style={{ width: `${s.score}%` }} />
                  </div>
                </div>
                <div className="skill-score">{s.score}%</div>
              </div>
            ))}
          </div>
        </section>

        <aside className="panel">
          <div className="panel-header">
            <h3>Roadmap</h3>
            <span className="tag neutral">Plan</span>
          </div>
          <div className="roadmap-list">
            {(data.roadmap?.items || []).map((item, idx) => (
              <div key={idx} className="roadmap-item">
                <strong>{item.skill_name}</strong>
                <small>
                  {item.current_level} → {item.target_level}
                </small>
                <span>{item.priority} priority</span>
              </div>
            ))}
          </div>
        </aside>
      </div>

      <div className="dashboard-grid lower-grid">
        <section className="panel">
          <div className="panel-header">
            <h3>Open opportunities</h3>
            <span className="tag neutral">4 Matches</span>
          </div>
          <div className="opportunity-list">
            {data.opportunities.jobs.map((job, idx) => (
              <div key={idx} className="opportunity-item">
                <div>
                  <strong>{job.title}</strong>
                  <small>{job.company}</small>
                </div>
                <span>{job.type}</span>
              </div>
            ))}
          </div>
        </section>

        <section className="panel">
          <div className="panel-header">
            <h3>Recent assessments</h3>
            <span className="tag info">Updated</span>
          </div>
          <div className="assessment-list">
            {(data.assessments || []).map((assessment, idx) => (
              <div key={idx} className="assessment-item">
                <div>
                  <strong>{assessment.assessment_id}</strong>
                  <small>Performance review</small>
                </div>
                <span>{assessment.score || '—'}%</span>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
