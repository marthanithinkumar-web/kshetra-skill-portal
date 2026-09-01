from pydantic import BaseModel, ConfigDict, Field, HttpUrl
from typing import Optional, List
from datetime import datetime

class AssessmentQuestionBase(BaseModel):
    prompt: str
    choices: Optional[str] = None
    answer: Optional[str] = None
    max_marks: Optional[float] = 1.0

class AssessmentQuestionCreate(AssessmentQuestionBase):
    pass

class AssessmentQuestion(AssessmentQuestionBase):
    id: int
    assessment_id: int
    model_config = ConfigDict(from_attributes=True)

class AssessmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    skill_id: int
    duration_minutes: Optional[int] = None

class AssessmentCreate(AssessmentBase):
    questions: List[AssessmentQuestionCreate] = []

class Assessment(AssessmentBase):
    id: int
    created_at: Optional[datetime]
    questions: List[AssessmentQuestion] = []
    model_config = ConfigDict(from_attributes=True)

class AssessmentAttemptCreate(BaseModel):
    assessment_id: int
    student_id: int
    answers: List[dict] = []  # {question_id, response}

class AttemptResult(BaseModel):
    attempt_id: int
    score: float

class PracticalTaskBase(BaseModel):
    title: str
    description: Optional[str]
    skill_id: int

class PracticalTaskCreate(PracticalTaskBase):
    pass

class PracticalTask(PracticalTaskBase):
    id: int
    created_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)

class PracticalSubmissionCreate(BaseModel):
    task_id: int
    student_id: int
    submission_text: Optional[str]
    repo_url: Optional[HttpUrl]

class PracticalSubmission(PracticalSubmissionCreate):
    id: int
    score: Optional[float]
    created_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)

class EvidenceRecord(BaseModel):
    id: int
    student_id: int
    skill_id: int
    evidence_type: str
    reference_id: Optional[int]
    score: Optional[float]
    details: Optional[str]
    created_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)

class VerificationRequest(BaseModel):
    student_id: int
    skill_id: int

class VerificationResult(BaseModel):
    student_skill_id: int
    score: float
    verified_level: str
    confidence: float
    evidence_count: int
    created_at: Optional[datetime]
