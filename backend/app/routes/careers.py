from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schemas_profiles import CareerCreate, Career, JobRoleBase, JobRole

router = APIRouter(prefix='/api/careers', tags=['careers'])

@router.post('/', response_model=Career)
def create_career(payload: CareerCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Career).filter(models.Career.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail='Career already exists')
    c = models.Career(name=payload.name, description=payload.description)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.get('/', response_model=list[Career])
def list_careers(db: Session = Depends(get_db)):
    return db.query(models.Career).all()

@router.post('/{career_id}/jobroles', response_model=JobRole)
def create_job_role(career_id: int, payload: JobRoleBase, db: Session = Depends(get_db)):
    career = db.query(models.Career).filter(models.Career.id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail='Career not found')
    jr = models.JobRole(career_id=career_id, title=payload.title, description=payload.description)
    db.add(jr)
    db.commit()
    db.refresh(jr)
    return jr

@router.get('/{career_id}/skills')
def career_skills(career_id: int, db: Session = Depends(get_db)):
    career = db.query(models.Career).filter(models.Career.id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail='Career not found')
    # include skill names and required_level from association
    rows = []
    for skill in career.skills:
        rows.append({'id': skill.id, 'name': skill.name, 'category': skill.category, 'description': skill.description})
    return rows

@router.post('/{career_id}/skills/{skill_id}')
def attach_skill_to_career(career_id: int, skill_id: int, db: Session = Depends(get_db)):
    career = db.query(models.Career).filter(models.Career.id == career_id).first()
    skill = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not career or not skill:
        raise HTTPException(status_code=404, detail='Career or skill not found')
    career.skills.append(skill)
    db.add(career)
    db.commit()
    return {'detail': 'attached'}
