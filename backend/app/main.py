from fastapi import FastAPI
from .routes import auth
from .database import engine
from . import models

from .routes import students, skills, careers, assessments, verifications, skill_gaps

app = FastAPI(title="Kshetra - Phase 4 API")

app.include_router(auth.router)
app.include_router(students.router)
app.include_router(skills.router)
app.include_router(careers.router)
app.include_router(assessments.router)
app.include_router(verifications.router)
app.include_router(skill_gaps.router)
from .routes import recruiter
app.include_router(recruiter.router)

@app.on_event("startup")
def startup_event():
    # Create tables (development convenience)
    from .database import Base
    Base.metadata.create_all(bind=engine)

@app.get("/api/health")
def health():
    return {"status": "ok"}
