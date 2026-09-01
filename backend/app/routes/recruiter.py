from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from typing import List

router = APIRouter(prefix='/api/recruiter', tags=['recruiter'])

LEVEL_ORDER = { 'Beginner': 0, 'Intermediate': 1, 'Advanced': 2 }

from ..dependencies import require_role

@router.post('/company')
def create_company(payload: dict, db: Session = Depends(get_db), current_user: models.User = Depends(require_role('Recruiter','Admin'))):
    c = models.Company(name=payload.get('name'), description=payload.get('description'), website=payload.get('website'))
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.post('/jobs')
def create_job(payload: dict, db: Session = Depends(get_db), current_user: models.User = Depends(require_role('Recruiter','Admin'))):
    company = db.query(models.Company).filter(models.Company.id==payload.get('company_id')).first()
    if not company:
        raise HTTPException(status_code=404, detail='Company not found')
    job = models.Job(company_id=company.id, title=payload.get('title'), description=payload.get('description'), location=payload.get('location'), mode=payload.get('mode'))
    db.add(job)
    db.commit()
    db.refresh(job)
    # attach skills if provided: list of {skill_id, required_level}
    for rs in payload.get('required_skills', []):
        skill = db.query(models.Skill).filter(models.Skill.id==rs.get('skill_id')).first()
        if skill and skill not in job.skills:
            job.skills.append(skill)
    db.add(job)
    db.commit()
    return job

@router.post('/internships')
def create_internship(payload: dict, db: Session = Depends(get_db), current_user: models.User = Depends(require_role('Recruiter','Admin'))):
    company = db.query(models.Company).filter(models.Company.id==payload.get('company_id')).first()
    if not company:
        raise HTTPException(status_code=404, detail='Company not found')
    intern = models.Internship(company_id=company.id, title=payload.get('title'), description=payload.get('description'), location=payload.get('location'), mode=payload.get('mode'))
    db.add(intern)
    db.commit()
    db.refresh(intern)
    for rs in payload.get('required_skills', []):
        skill = db.query(models.Skill).filter(models.Skill.id==rs.get('skill_id')).first()
        if skill and skill not in intern.skills:
            intern.skills.append(skill)
    db.add(intern)
    db.commit()
    return intern

@router.get('/jobs')
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()
    out = []
    for j in jobs:
        out.append({
            'id': j.id,
            'company': j.company.name if j.company else None,
            'title': j.title,
            'description': j.description,
            'location': j.location,
            'mode': j.mode,
            'skills': [ { 'id': s.id, 'name': s.name } for s in j.skills ]
        })
    return out

@router.get('/internships')
def list_internships(db: Session = Depends(get_db)):
    interns = db.query(models.Internship).all()
    out = []
    for it in interns:
        out.append({
            'id': it.id,
            'company': it.company.name if it.company else None,
            'title': it.title,
            'description': it.description,
            'location': it.location,
            'mode': it.mode,
            'skills': [ { 'id': s.id, 'name': s.name } for s in it.skills ]
        })
    return out

@router.post('/search')
def search_candidates(payload: dict, db: Session = Depends(get_db)):
    # payload: { requirements: [ { skill_name: str, min_level: 'Intermediate' } ] }
    reqs = payload.get('requirements', [])
    # Build skill->required_order map
    required = {}
    skill_objs = {}
    for r in reqs:
        name = r.get('skill_name')
        min_level = r.get('min_level', 'Beginner')
        required[name.lower()] = LEVEL_ORDER.get(min_level, 0)
    # fetch all student_skills where skill in required
    results = []
    # for performance, map skill names to ids
    skills = db.query(models.Skill).filter(models.Skill.name.in_([r.get('skill_name') for r in reqs])).all()
    skill_name_to_id = {s.name.lower(): s.id for s in skills}
    # gather candidate students who have any of these verified skills
    student_skills = db.query(models.StudentSkill).filter(models.StudentSkill.skill_id.in_(list(skill_name_to_id.values()))).all()
    # group by student
    by_student = {}
    for ss in student_skills:
        by_student.setdefault(ss.student_id, []).append(ss)
    # compute match score per student
    for student_id, sskills in by_student.items():
        match_score = 0.0
        total_weight = len(reqs) if len(reqs)>0 else 1
        matched = []
        missing = []
        partial = []
        for req in reqs:
            sname = req.get('skill_name')
            sid = skill_name_to_id.get(sname.lower())
            required_ord = LEVEL_ORDER.get(req.get('min_level','Beginner'), 0)
            ss = next((x for x in sskills if x.skill_id==sid), None)
            if not ss or not ss.verified_level:
                # missing
                missing.append(sname)
                continue
            cur_ord = LEVEL_ORDER.get(ss.verified_level, 0)
            if cur_ord >= required_ord:
                matched.append(sname)
                match_score += 1.0
            elif cur_ord < required_ord and cur_ord > 0:
                partial.append(sname)
                match_score += 0.5
        # Normalize to percentage
        score_pct = 0.0
        if total_weight > 0:
            score_pct = (match_score / total_weight) * 100.0
        student = db.query(models.Student).filter(models.Student.id==student_id).first()
        user = student.user if student else None
        results.append({
            'student_id': student_id,
            'name': user.full_name if user else None,
            'email': user.email if user else None,
            'matched': matched,
            'partial': partial,
            'missing': missing,
            'match_score': score_pct
        })
    # Sort by score desc
    results.sort(key=lambda x: x['match_score'], reverse=True)
    return results

from ..dependencies import get_current_user

@router.get('/students/{student_id}/evidence')
def view_student_evidence(student_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    # Only Recruiter/Admin/College or the student themselves may view evidence
    role = current_user.role.name if current_user.role else None
    if role == 'Student':
        # if student, ensure owner
        if not current_user.student or current_user.student.id != student_id:
            raise HTTPException(status_code=403, detail='Forbidden')
    elif role not in ('Recruiter','Admin','College'):
        raise HTTPException(status_code=403, detail='Forbidden')
    # Return evidence records grouped by skill
    rows = db.query(models.Evidence).filter(models.Evidence.student_id==student_id).all()
    out = {}
    for r in rows:
        out.setdefault(r.skill_id, []).append({ 'type': r.evidence_type, 'score': r.score, 'details': r.details, 'reference_id': r.reference_id, 'created_at': r.created_at })
    return out

from ..dependencies import get_current_user

@router.post('/jobs/{job_id}/apply')
def apply_job(job_id: int, payload: dict, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    job = db.query(models.Job).filter(models.Job.id==job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail='Job not found')
    # If current user is student, they may omit student_id and apply as themselves
    student_id = payload.get('student_id')
    if current_user.role and current_user.role.name == 'Student':
        student_obj = db.query(models.Student).filter(models.Student.user_id==current_user.id).first()
        if not student_obj:
            raise HTTPException(status_code=404, detail='Student profile not found')
        student_id = student_obj.id
    if not student_id:
        raise HTTPException(status_code=400, detail='student_id required')
    app = models.Application(student_id=student_id, job_id=job_id, cover_letter=payload.get('cover_letter'))
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

@router.post('/internships/{internship_id}/apply')
def apply_internship(internship_id: int, payload: dict, db: Session = Depends(get_db)):
    intern = db.query(models.Internship).filter(models.Internship.id==internship_id).first()
    if not intern:
        raise HTTPException(status_code=404, detail='Internship not found')
    student_id = payload.get('student_id')
    if not student_id:
        raise HTTPException(status_code=400, detail='student_id required')
    app = models.Application(student_id=student_id, internship_id=internship_id, cover_letter=payload.get('cover_letter'))
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

@router.get('/jobs/{job_id}/applications')
def list_applications(job_id: int, db: Session = Depends(get_db)):
    apps = db.query(models.Application).filter(models.Application.job_id==job_id).all()
    out = []
    for a in apps:
        out.append({ 'id': a.id, 'student_id': a.student_id, 'student_name': a.student.user.full_name, 'status': a.status, 'shortlisted': a.shortlisted })
    return out

@router.post('/applications/{application_id}/shortlist')
def shortlist_application(application_id: int, payload: dict, db: Session = Depends(get_db)):
    app = db.query(models.Application).filter(models.Application.id==application_id).first()
    if not app:
        raise HTTPException(status_code=404, detail='Application not found')
    app.shortlisted = bool(payload.get('shortlisted', True))
    app.status = payload.get('status', app.status)
    db.add(app)
    db.commit()
    return { 'id': app.id, 'shortlisted': app.shortlisted, 'status': app.status }
