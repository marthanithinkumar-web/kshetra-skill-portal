from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..services import verification_engine
from .. import models
from ..dependencies import get_current_user

router = APIRouter(prefix='/api/verifications', tags=['verifications'])

@router.post('/run')
def run_verification(req: dict, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    student_id = req.get('student_id')
    skill_id = req.get('skill_id')
    if not student_id or not skill_id:
        raise HTTPException(status_code=400, detail='student_id and skill_id required')
    # Only the student themselves or admin/recruiter/college can trigger verification
    role = current_user.role.name if current_user.role else None
    if role == 'Student':
        if not current_user.student or current_user.student.id != student_id:
            raise HTTPException(status_code=403, detail='Cannot verify other student')
    # Allow Admin, Recruiter and College to run for now
    return verification_engine.compute_verification(db, student_id, skill_id)

from ..dependencies import require_role

@router.get('/weights')
def get_weights(db: Session = Depends(get_db)):
    """Return the current verification weights. If none configured, returns defaults."""
    w = db.query(models.VerificationWeights).order_by(models.VerificationWeights.id.desc()).first()
    if not w:
        return verification_engine.DEFAULT_WEIGHTS
    return {
        'coding_assessment': w.coding_assessment,
        'practical_task': w.practical_task,
        'project_evidence': w.project_evidence,
        'technical_explanation': w.technical_explanation,
        'github_evidence': w.github_evidence,
        'updated_at': w.updated_at,
    }

@router.post('/weights')
def set_weights(payload: dict, db: Session = Depends(get_db), current_user: models.User = Depends(require_role('Admin'))):
    """Create or update verification weights. Accepts keys matching the default weights.
    Example payload: {"coding_assessment": 0.25, "practical_task": 0.25, "project_evidence": 0.2, "technical_explanation": 0.15, "github_evidence": 0.15}
    """
    # Validate payload keys and values
    keys = ['coding_assessment','practical_task','project_evidence','technical_explanation','github_evidence']
    values = {}
    total = 0.0
    for k in keys:
        v = payload.get(k)
        if v is None:
            raise HTTPException(status_code=400, detail=f'Missing weight: {k}')
        try:
            fv = float(v)
        except Exception:
            raise HTTPException(status_code=400, detail=f'Invalid value for {k}')
        if fv < 0 or fv > 1:
            raise HTTPException(status_code=400, detail=f'Weight for {k} must be between 0 and 1')
        values[k] = fv
        total += fv
    if abs(total - 1.0) > 0.0001:
        raise HTTPException(status_code=400, detail='Weights must sum to 1.0')
    w = models.VerificationWeights(coding_assessment=values['coding_assessment'], practical_task=values['practical_task'], project_evidence=values['project_evidence'], technical_explanation=values['technical_explanation'], github_evidence=values['github_evidence'])
    db.add(w)
    db.commit()
    db.refresh(w)
    return {'detail': 'weights updated', 'weights_id': w.id}

@router.get('/passport/{student_id}')
def skill_passport(student_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    student = db.query(models.Student).filter(models.Student.id==student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    # Authorization: Students can view own passport; Recruiter/Admin/College can view others
    role = current_user.role.name if current_user.role else None
    if role == 'Student' and current_user.student and current_user.student.id != student_id:
        raise HTTPException(status_code=403, detail='Forbidden')
    # Build passport: list verified skills for student
    records = db.query(models.StudentSkill).filter(models.StudentSkill.student_id==student_id).all()
    skills = []
    for r in records:
        skills.append({
            'skill_id': r.skill_id,
            'skill_name': r.skill.name,
            'score': r.score,
            'verified_level': r.verified_level,
            'confidence': r.confidence,
            'evidence_count': r.evidence_count,
            'last_verified_at': r.last_verified_at,
        })
    # career readiness as average of scores
    if len(records) == 0:
        readiness = 0
    else:
        readiness = sum([(r.score or 0.0) for r in records])/len(records)
    return {
        'student': {'id': student.id, 'name': student.user.full_name},
        'target_career': student.target_career.name if student.target_career else None,
        'skills': skills,
        'career_readiness': readiness
    }

@router.get('/history/{student_skill_id}')
def verification_history(student_skill_id: int, db: Session = Depends(get_db)):
    rows = db.query(models.SkillVerificationHistory).filter(models.SkillVerificationHistory.student_skill_id==student_skill_id).order_by(models.SkillVerificationHistory.created_at.desc()).all()
    return rows
