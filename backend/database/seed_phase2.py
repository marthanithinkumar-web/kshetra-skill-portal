"""Seed demo data for Phase 2: students, skills, careers, projects."""
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
    # Ensure roles exist
    roles = {r.name: r for r in db.query(models.Role).all()}
    if 'student' not in roles:
        db.add(models.Role(name='student', description='Student / Learner'))
    if 'admin' not in roles:
        db.add(models.Role(name='admin', description='Platform Admin'))
    db.commit()

    # Create demo skills
    skill_names = ['Python', 'SQL', 'Excel', 'Power BI', 'Statistics', 'Pandas', 'NumPy', 'Data Visualization', 'Machine Learning', 'Git']
    existing_skills = {s.name: s for s in db.query(models.Skill).filter(models.Skill.name.in_(skill_names)).all()}
    for name in skill_names:
        if name not in existing_skills:
            db.add(models.Skill(name=name))
    db.commit()

    # Careers
    career = db.query(models.Career).filter(models.Career.name=='Data Analyst').first()
    if not career:
        career = models.Career(name='Data Analyst', description='Data Analyst role')
        db.add(career)
        db.commit()
        db.refresh(career)
    # Attach some skills
    skills = db.query(models.Skill).filter(models.Skill.name.in_(['Python','SQL','Excel','Power BI','Statistics'])).all()
    for s in skills:
        if s not in career.skills:
            career.skills.append(s)
    db.add(career)
    db.commit()

    # Create a demo user Arun
    arun = db.query(models.User).filter(models.User.email=='arun.k@example.com').first()
    if not arun:
        # use simple hashed password for demo (not secure)
        from backend.app.services.auth import get_password_hash
        student_role = db.query(models.Role).filter(models.Role.name=='student').first()
        arun = models.User(email='arun.k@example.com', full_name='Arun Kumar', hashed_password=get_password_hash('password123'), role_id=student_role.id)
        db.add(arun)
        db.commit()
        db.refresh(arun)
    # Create student profile for Arun
    student = db.query(models.Student).filter(models.Student.user_id==arun.id).first()
    if not student:
        student = models.Student(user_id=arun.id, bio='Demo student Arun Kumar', location='India', target_career_id=career.id)
        db.add(student)
        db.commit()
        db.refresh(student)
    # Add a project
    if not db.query(models.Project).filter(models.Project.student_id==student.id).first():
        db.add(models.Project(student_id=student.id, title='Sales Analysis', description='Data analysis project using Python and Pandas', repo_url='https://github.com/example/sales-analysis'))
    db.commit()
    print('Phase 2 seed complete')

if __name__ == '__main__':
    seed()
