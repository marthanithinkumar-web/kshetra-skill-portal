# Kshetra — SIH26044

AI-Based Student Skill Verification & Career Readiness (MVP Phase 1)

This repository contains the Phase 1 scaffolding for the Kshetra platform (Smart India Hackathon 2026).

Phase 1 implemented here:
- Project structure (monorepo: frontend, backend, database)
- FastAPI backend scaffold
- Oracle-compatible SQLAlchemy DB setup (configurable via env)
- Authentication (registration/login) with password hashing and JWT
- Role-based access control basic model (users + roles)
- Minimal React frontend scaffold with Register/Login pages

Phase 2 implemented here:
- Student profile CRUD (students, education, certifications, projects)
- Skills CRUD and listing
- Careers and job roles, career <-> skill association
- Student dashboard endpoint aggregating profile, skills, projects, certifications
- Frontend pages: Profile, Dashboard, Skills, Careers
- Seed script: backend/database/seed_phase2.py to create demo data (Arun Kumar, skills, Data Analyst career)

Phase 3 implemented here:
- Skill assessments, practical tasks, evidence collection
- Verification engine (rule-based weighted scoring) and skill passport
- Seed script: backend/database/seed_phase3.py

Phase 4 implemented here:
- Skill gap engine and knowledge-graph fallback for career -> job role -> skill -> subskill
- Personalized roadmap generation

Important architecture decision (applies to the whole project)
- The platform uses a hybrid practical AI/ML approach for the SIH MVP:
  1. RULE-BASED / WEIGHTED SCORING (primary, explainable)
     - Core skill verification, evidence aggregation, skill-gap calculation, career readiness
  2. SMALL ML COMPONENTS (optional, targeted)
     - Skill classification, ranking, lightweight prediction/analytics
  3. NLP / LLM ONLY WHERE IT ADDS REAL VALUE
     - Resume skill extraction, job-description extraction, AI interview evaluation, personalized explanations

Notes about verification and ML policy:
- Do NOT train or build a large ML model from scratch for the MVP.
- Keep AI provider modular and abstracted behind a service layer.
- The verified skill score is produced by a deterministic, explainable, weighted scoring engine.
- If an evidence source is unavailable, the engine explicitly excludes that source rather than fabricating values.
- Weights are configurable from the backend (see /api/verifications/weights) and stored in VerificationWeights table.
- Any ML/NLP usage must be clearly separated from the deterministic verification engine and explicitly documented.

Next steps:
- Run backend and frontend following the instructions below.

Environment (examples):
- Python 3.10+
- Node 18+
- Oracle DB (or use a compatible connection string for testing)

Files created in Phase 1 & 2:
- /backend/app/main.py
- /backend/app/core/config.py
- /backend/app/database.py
- /backend/app/models.py
- /backend/app/schemas.py
- /backend/app/schemas_profiles.py
- /backend/app/services/auth.py
- /backend/app/routes/auth.py
- /backend/app/routes/students.py
- /backend/app/routes/skills.py
- /backend/app/routes/careers.py
- /backend/requirements.txt
- /backend/database/seed_roles.py
- /backend/database/seed_phase2.py
- /frontend/package.json
- /frontend/public/index.html
- /frontend/src/index.js
- /frontend/src/index.css
- /frontend/src/App.jsx
- /frontend/src/pages/Register.jsx
- /frontend/src/pages/Login.jsx
- /frontend/src/pages/StudentProfile.jsx
- /frontend/src/pages/Dashboard.jsx
- /frontend/src/pages/Skills.jsx
- /frontend/src/pages/Careers.jsx
- /frontend/src/services/api.js
- /frontend/src/services/students.js
- .env.example

Run backend (development):
1. Create a virtualenv and activate it
   - python -m venv .venv
   - source .venv/bin/activate  (macOS / Linux) or .venv\\Scripts\\activate (Windows)
2. pip install -r backend/requirements.txt
   - Note: cx_Oracle may require Oracle Instant Client. For quick local dev use SQLite:
     - set DATABASE_URL=sqlite:///./dev.db in .env
3. Copy .env.example -> .env and set SECRET_KEY to a secure random string
4. Start the API:
   - uvicorn backend.app.main:app --reload --port 8000
5. Seed demo data (after starting or with PYTHONPATH):
   - python -m backend.database.seed_phase2
     or
   - python backend/database/seed_phase2.py

Run frontend (development):
1. cd frontend
2. npm install
3. npm start

Notes:
- The frontend expects the backend API at http://localhost:8000/api by default; set REACT_APP_API_URL to change.
- For demo flows, register a user as Student (role_id = 1), then run the seed script to create Arun example, or set localStorage keys 'kshetra_user_id' and 'kshetra_token' for the demo user.

Maintainer: TEAM KSHETRA
