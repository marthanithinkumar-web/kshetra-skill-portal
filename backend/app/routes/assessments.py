from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from ..schemas_assessments import (
    AssessmentCreate, Assessment, AssessmentAttemptCreate, AttemptResult, PracticalTaskCreate, PracticalTask, PracticalSubmissionCreate, PracticalSubmission
)
from typing import List
import json

router = APIRouter(prefix='/api/assessments', tags=['assessments'])

@router.post('/', response_model=Assessment)
def create_assessment(payload: AssessmentCreate, db: Session = Depends(get_db)):
    # create assessment and questions
    ass = models.Assessment(title=payload.title, description=payload.description, skill_id=payload.skill_id, duration_minutes=payload.duration_minutes)
    db.add(ass)
    db.commit()
    db.refresh(ass)
    for q in payload.questions:
        qq = models.AssessmentQuestion(assessment_id=ass.id, prompt=q.prompt, choices=q.choices, answer=q.answer, max_marks=q.max_marks)
        db.add(qq)
    db.commit()
    db.refresh(ass)
    return ass

@router.get('/', response_model=List[Assessment])
def list_assessments(db: Session = Depends(get_db)):
    return db.query(models.Assessment).all()

@router.get('/{assessment_id}', response_model=Assessment)
def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    a = db.query(models.Assessment).filter(models.Assessment.id==assessment_id).first()
    if not a:
        raise HTTPException(status_code=404, detail='Assessment not found')
    return a

@router.post('/attempt', response_model=AttemptResult)
def submit_attempt(payload: AssessmentAttemptCreate, db: Session = Depends(get_db)):
    assessment = db.query(models.Assessment).filter(models.Assessment.id==payload.assessment_id).first()
    if not assessment:
        raise HTTPException(status_code=404, detail='Assessment not found')
    student = db.query(models.Student).filter(models.Student.id==payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    attempt = models.AssessmentAttempt(assessment_id=assessment.id, student_id=student.id)
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    total_score = 0.0
    total_max = 0.0
    # Simple auto-grading for question types where answer is provided and matches
    for ans in payload.answers:
        q = db.query(models.AssessmentQuestion).filter(models.AssessmentQuestion.id==ans.get('question_id')).first()
        if not q:
            continue
        resp = ans.get('response')
        marks = 0.0
        if q.answer is not None and resp is not None:
            # basic exact match grading
            if str(resp).strip().lower() == str(q.answer).strip().lower():
                marks = q.max_marks or 1.0
        total_score += marks
        total_max += (q.max_marks or 1.0)
        aa = models.AttemptAnswer(attempt_id=attempt.id, question_id=q.id, response=json.dumps(resp), marks_obtained=marks)
        db.add(aa)
    db.commit()
    # Normalize to 0-100
    final_score = 0.0
    if total_max > 0:
        final_score = (total_score / total_max) * 100.0
    attempt.score = final_score
    attempt.submitted_at = None
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    # Create evidence record for coding_assessment
    e = models.Evidence(student_id=student.id, skill_id=assessment.skill_id, evidence_type='coding_assessment', reference_id=attempt.id, score=final_score, details=f'Auto-graded assessment {assessment.id}')
    db.add(e)
    db.commit()
    return {'attempt_id': attempt.id, 'score': final_score}

# Practical tasks
@router.post('/practical', response_model=PracticalTask)
def create_practical_task(payload: PracticalTaskCreate, db: Session = Depends(get_db)):
    task = models.PracticalTask(title=payload.title, description=payload.description, skill_id=payload.skill_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.post('/practical/submit', response_model=PracticalSubmission)
def submit_practical(payload: PracticalSubmissionCreate, db: Session = Depends(get_db)):
    try:
        task = db.query(models.PracticalTask).filter(models.PracticalTask.id==payload.task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail='Task not found')
        student = db.query(models.Student).filter(models.Student.id==payload.student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail='Student not found')
        sub = models.PracticalSubmission(task_id=task.id, student_id=student.id, submission_text=payload.submission_text, repo_url=(str(payload.repo_url) if payload.repo_url else None))
        db.add(sub)
        db.commit()
        db.refresh(sub)
        # For demo, set score to 75 by default; in production this would be reviewer graded or auto-graded
        sub.score = 75.0
        db.add(sub)
        db.commit()
        # Create evidence record
        e = models.Evidence(student_id=student.id, skill_id=task.skill_id, evidence_type='practical_task', reference_id=sub.id, score=sub.score, details='Practical submission auto-score')
        db.add(e)
        db.commit()
        return sub
    except HTTPException:
        raise
    except Exception as e:
        # Return a clear HTTP error to the client for debugging in dev
        raise HTTPException(status_code=500, detail=f'Error submitting practical: {str(e)}')
