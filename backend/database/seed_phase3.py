"""Seed demo data for Phase 3: assessments, questions, practical tasks, and initial evidence."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
from backend.app.core.config import settings
from backend.app.database import Base
from backend.app import models

engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine)

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    # Find Arun
    arun = db.query(models.User).filter(models.User.email=='arun.k@example.com').first()
    if not arun:
        print('Arun not found, run seed_phase2 first')
        return
    student = db.query(models.Student).filter(models.Student.user_id==arun.id).first()
    if not student:
        print('Arun student profile missing')
        return
    # Find Python skill
    python_skill = db.query(models.Skill).filter(models.Skill.name=='Python').first()
    if not python_skill:
        print('Python skill missing')
        return
    # Create an assessment
    if not db.query(models.Assessment).filter(models.Assessment.title=='Python MCQ Assessment').first():
        a = models.Assessment(title='Python MCQ Assessment', description='MCQ assessment for Python basics', skill_id=python_skill.id, duration_minutes=30)
        db.add(a)
        db.commit()
        db.refresh(a)
        q1 = models.AssessmentQuestion(assessment_id=a.id, prompt='What is the output of print(1+2)?', choices='["1","2","3","12"]', answer='3', max_marks=1.0)
        q2 = models.AssessmentQuestion(assessment_id=a.id, prompt='Which keyword is used to create a function in Python?', choices='["func","def","function","lambda"]', answer='def', max_marks=1.0)
        db.add(q1); db.add(q2)
        db.commit()
        print('Created Python assessment')
    # Create a practical task
    if not db.query(models.PracticalTask).filter(models.PracticalTask.title=='Python Practical Task').first():
        t = models.PracticalTask(title='Python Practical Task', description='Create a small script to parse CSV.', skill_id=python_skill.id)
        db.add(t)
        db.commit()
        print('Created practical task')
    # Create a project evidence (Project already added in phase2)
    proj = db.query(models.Project).filter(models.Project.student_id==student.id).first()
    if proj:
        # create evidence for project
        exists = db.query(models.Evidence).filter(models.Evidence.student_id==student.id, models.Evidence.skill_id==python_skill.id, models.Evidence.evidence_type=='project').first()
        if not exists:
            e = models.Evidence(student_id=student.id, skill_id=python_skill.id, evidence_type='project_evidence', reference_id=proj.id, score=90.0, details='Project repo analysis score')
            db.add(e)
            db.commit()
            print('Added project evidence for Arun')
    print('Phase 3 seed complete')

if __name__ == '__main__':
    seed()
