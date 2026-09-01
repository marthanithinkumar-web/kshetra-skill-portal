import React from 'react';
import { Link } from 'react-router-dom';

export default function Home(){
  return (
    <div className="max-w-6xl mx-auto p-6">
      <header className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">AI-Based Student Skill Verification & Career Readiness</h1>
          <p className="mt-2 text-gray-600">Assess. Verify. Develop. Re-verify. Connect.</p>
          <p className="mt-4 text-gray-700">Turn student skills into evidence-backed profiles that connect learning, internships and placement opportunities.</p>
          <div className="mt-6">
            <Link to="/register" className="inline-block bg-blue-600 text-white px-4 py-2 rounded mr-3">Get Started</Link>
            <Link to="/dashboard" className="inline-block bg-gray-200 text-gray-800 px-4 py-2 rounded">Explore Opportunities</Link>
          </div>
        </div>
        <div className="w-1/3 bg-gradient-to-br from-white to-gray-50 p-4 rounded shadow">
          <ol className="text-sm space-y-2 text-gray-700">
            <li>Student Profile</li>
            <li>Skill Assessment</li>
            <li>Evidence Verification</li>
            <li>Skill Passport</li>
            <li>Skill Gap</li>
            <li>Development</li>
            <li>Re-verification</li>
            <li>Internship / Placement</li>
          </ol>
        </div>
      </header>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold mb-3">How it works</h2>
        <div className="grid grid-cols-3 gap-4">
          <div className="p-4 bg-white rounded shadow">
            <h3 className="font-bold">Claim</h3>
            <p className="text-sm text-gray-600">Students create profiles and claim skills.</p>
          </div>
          <div className="p-4 bg-white rounded shadow">
            <h3 className="font-bold">Assess</h3>
            <p className="text-sm text-gray-600">Assessments and practical tasks generate evidence.</p>
          </div>
          <div className="p-4 bg-white rounded shadow">
            <h3 className="font-bold">Verify</h3>
            <p className="text-sm text-gray-600">Weighted evidence aggregation produces verified proficiency.</p>
          </div>
        </div>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold mb-3">Core features</h2>
        <div className="grid md:grid-cols-3 gap-4">
          <div className="p-4 bg-white rounded shadow">Evidence-Based Skill Verification</div>
          <div className="p-4 bg-white rounded shadow">Skill Passport</div>
          <div className="p-4 bg-white rounded shadow">Industry Skill Mapping</div>
          <div className="p-4 bg-white rounded shadow">Skill Gap Analysis</div>
          <div className="p-4 bg-white rounded shadow">Personalized Roadmap</div>
          <div className="p-4 bg-white rounded shadow">Internship & Placement Matching</div>
        </div>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold mb-3">For Students</h2>
        <p className="text-gray-600">Build evidence-rich profiles, take assessments, and get matched to internships and jobs based on verified skills.</p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold mb-3">For Colleges / TPO</h2>
        <p className="text-gray-600">Monitor student readiness and plan training based on real gaps found in verified skills.</p>
      </section>

      <section className="mb-8">
        <h2 className="text-2xl font-semibold mb-3">For Industry / Recruiters</h2>
        <p className="text-gray-600">Search candidates by VERIFIED skills and view supporting evidence before shortlisting.</p>
      </section>

      <footer className="mt-12 border-t pt-4 text-sm text-gray-600">
        <div className="flex justify-between">
          <div>© Kshetra - Demo</div>
          <div><Link to="/careers" className="text-blue-600">Careers</Link> · <Link to="/assessments" className="text-blue-600">Assessments</Link></div>
        </div>
      </footer>
    </div>
  )
}
