from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schemas_profiles import SkillCreate, Skill

router = APIRouter(prefix='/api/skills', tags=['skills'])

@router.post('/', response_model=Skill)
def create_skill(payload: SkillCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Skill).filter(models.Skill.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=400, detail='Skill already exists')
    s = models.Skill(name=payload.name, category=payload.category, description=payload.description)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s

@router.get('/', response_model=list[Skill])
def list_skills(db: Session = Depends(get_db)):
    skills = db.query(models.Skill).order_by(models.Skill.name).all()
    return skills

@router.get('/{skill_id}', response_model=Skill)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    s = db.query(models.Skill).filter(models.Skill.id == skill_id).first()
    if not s:
        raise HTTPException(status_code=404, detail='Skill not found')
    return s
