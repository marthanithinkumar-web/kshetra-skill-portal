from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from .. import schemas
from ..schemas_profiles import (
    StudentProfile, StudentEducationCreate, CertificationCreate,
    ProjectCreate, StudentSkillCreate
)

from ..dependencies import get_current_user

router = APIRouter(prefix="/api/students", tags=["students"])

# --- New secure endpoints using JWT-based current user ---
@router.get('/me', response_model=StudentProfile)
def get_my_profile(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        # Create an empty student profile record on first access
        student = models.Student(user_id=current_user.id)
        db.add(student)
        db.commit()
        db.refresh(student)
    return student

@router.put('/me', response_model=StudentProfile)
def update_my_profile(payload: dict, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail='Student profile not found')
    if 'bio' in payload:
        student.bio = payload['bio']
    if 'location' in payload:
        student.location = payload['location']
    if 'target_career_id' in payload:
        student.target_career_id = payload['target_career_id']
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.post('/me/education', response_model=StudentEducationCreate)
def add_my_education(payload: StudentEducationCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail='Student profile not found')
    edu = models.StudentEducation(student_id=student.id, **payload.dict())
    db.add(edu)
    db.commit()
    db.refresh(edu)
    return edu

@router.post('/me/certifications', response_model=CertificationCreate)
def add_my_certification(payload: CertificationCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail='Student profile not found')
    cdata = payload.dict()
    if cdata.get('url') is not None:
        cdata['url'] = str(cdata['url'])
    cert = models.Certification(student_id=student.id, **cdata)
    db.add(cert)
    db.commit()
    db.refresh(cert)
    return cert

@router.post('/me/projects', response_model=ProjectCreate)
def add_my_project(payload: ProjectCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail='Student profile not found')
    pdata = payload.dict()
    if pdata.get('repo_url') is not None:
        pdata['repo_url'] = str(pdata['repo_url'])
    if pdata.get('demo_url') is not None:
        pdata['demo_url'] = str(pdata['demo_url'])
    proj = models.Project(student_id=student.id, **pdata)
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj

@router.post('/me/skills', response_model=StudentSkillCreate)
def add_my_skill(payload: StudentSkillCreate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail='Student profile not found')
    skill = db.query(models.Skill).filter(models.Skill.id == payload.skill_id).first()
    if not skill:
        raise HTTPException(status_code=400, detail='Invalid skill_id')
    ss = models.StudentSkill(student_id=student.id, skill_id=payload.skill_id, claimed_level=payload.claimed_level)
    db.add(ss)
    db.commit()
    db.refresh(ss)
    return ss

# Student creation (admin or programmatic use)
@router.post("/create", response_model=StudentProfile)
def create_student_profile(payload: dict, db: Session = Depends(get_db)):
    # payload expected to contain user_id and optional fields
    user_id = payload.get('user_id')
    if not user_id:
        raise HTTPException(status_code=400, detail="user_id is required")
    existing = db.query(models.Student).filter(models.Student.user_id == user_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")
    student = models.Student(user_id=user_id, bio=payload.get('bio'), location=payload.get('location'))
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

@router.get('/{user_id}', response_model=StudentProfile)
def get_student_profile(user_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.user_id == user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail='Student profile not found')
    return student

@router.put('/{user_id}', response_model=StudentProfile)
def update_student_profile(user_id: int, payload: dict, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.user_id == user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail='Student profile not found')
    if 'bio' in payload:
        student.bio = payload['bio']
    if 'location' in payload:
        student.location = payload['location']
    if 'target_career_id' in payload:
        student.target_career_id = payload['target_career_id']
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


# Certifications
@router.post('/{user_id}/certifications', response_model=CertificationCreate)
def add_certification(user_id: int, payload: CertificationCreate, db: Session = Depends(get_db)):
    try:
        student = db.query(models.Student).filter(models.Student.user_id == user_id).first()
        if not student:
            raise HTTPException(status_code=404, detail='Student profile not found')
        cdata = payload.dict()
        # convert HttpUrl to str for DB
        if cdata.get('url') is not None:
            cdata['url'] = str(cdata['url'])
        cert = models.Certification(student_id=student.id, **cdata)
        db.add(cert)
        db.commit()
        db.refresh(cert)
        return cert
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error creating certification: {str(e)}')

# Projects
@router.post('/{user_id}/projects', response_model=ProjectCreate)
def add_project(user_id: int, payload: ProjectCreate, db: Session = Depends(get_db)):
    try:
        student = db.query(models.Student).filter(models.Student.user_id == user_id).first()
        if not student:
            raise HTTPException(status_code=404, detail='Student profile not found')
        pdata = payload.dict()
        if pdata.get('repo_url') is not None:
            pdata['repo_url'] = str(pdata['repo_url'])
        if pdata.get('demo_url') is not None:
            pdata['demo_url'] = str(pdata['demo_url'])
        proj = models.Project(student_id=student.id, **pdata)
        db.add(proj)
        db.commit()
        db.refresh(proj)
        return proj
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error creating project: {str(e)}')

# Skills
@router.post('/{user_id}/skills', response_model=StudentSkillCreate)
def add_skill(user_id: int, payload: StudentSkillCreate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.user_id == user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail='Student profile not found')
    # Ensure skill exists
    skill = db.query(models.Skill).filter(models.Skill.id == payload.skill_id).first()
    if not skill:
        raise HTTPException(status_code=400, detail='Invalid skill_id')
    ss = models.StudentSkill(student_id=student.id, skill_id=payload.skill_id, claimed_level=payload.claimed_level)
    db.add(ss)
    db.commit()
    db.refresh(ss)
    return ss

# Student dashboard aggregation
@router.get('/{user_id}/dashboard')
def student_dashboard(user_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.user_id == user_id).first()
    if not student:
        raise HTTPException(status_code=404, detail='Student profile not found')
    # Simple aggregation: profile, skills, projects, certifications
    profile = student
    skills = [ {
        'skill': s.skill.name,
        'claimed_level': s.claimed_level,
        'verified_level': s.verified_level,
        'score': s.score,
        'confidence': s.confidence
    } for s in student.skills]
    projects = [ { 'title': p.title, 'repo_url': p.repo_url } for p in student.projects]
    certifications = [ { 'name': c.name, 'issuer': c.issuer } for c in student.certifications]
    return {
        'profile': profile,
        'skills': skills,
        'projects': projects,
        'certifications': certifications
    }

# --- secure 'me' getters for data driven flows ---
@router.get('/me/skills')
def get_my_skills(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        return []
    rows = db.query(models.StudentSkill).filter(models.StudentSkill.student_id==student.id).all()
    out = []
    for r in rows:
        out.append({
            'skill_id': r.skill_id,
            'skill_name': r.skill.name,
            'claimed_level': r.claimed_level,
            'verified_level': r.verified_level,
            'score': r.score,
            'confidence': r.confidence,
            'evidence_count': r.evidence_count,
            'last_verified_at': r.last_verified_at
        })
    return out

@router.get('/me/assessments')
def get_my_assessments(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        return []
    attempts = db.query(models.AssessmentAttempt).filter(models.AssessmentAttempt.student_id==student.id).order_by(models.AssessmentAttempt.started_at.desc()).all()
    out = []
    for a in attempts:
        out.append({'attempt_id': a.id, 'assessment_id': a.assessment_id, 'score': a.score, 'started_at': a.started_at, 'submitted_at': a.submitted_at})
    return out

@router.get('/me/roadmap')
def get_my_roadmap(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.user_id == current_user.id).first()
    if not student:
        return None
    roadmap = db.query(models.Roadmap).filter(models.Roadmap.student_id==student.id).order_by(models.Roadmap.created_at.desc()).first()
    if not roadmap:
        return None
    items = []
    for it in roadmap.items:
        items.append({'skill_id': it.skill_id, 'skill_name': it.skill.name, 'current_level': it.current_level, 'target_level': it.target_level, 'priority': it.priority, 'recommendations': it.recommendations, 'sequence': it.sequence})
    return {'id': roadmap.id, 'title': roadmap.title, 'items': items}

@router.get('/me/opportunities')
def get_my_opportunities(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Return jobs and internships for students to browse (no fake data)
    jobs = db.query(models.Job).order_by(models.Job.created_at.desc()).limit(20).all()
    interns = db.query(models.Internship).order_by(models.Internship.created_at.desc()).limit(20).all()
    out = {
        'jobs': [ { 'id': j.id, 'title': j.title, 'company': j.company.name if j.company else None, 'location': j.location, 'mode': j.mode, 'skills': [s.name for s in j.skills] } for j in jobs ],
        'internships': [ { 'id': it.id, 'title': it.title, 'company': it.company.name if it.company else None, 'location': it.location, 'mode': it.mode, 'skills': [s.name for s in it.skills] } for it in interns ]
    }
    return out
