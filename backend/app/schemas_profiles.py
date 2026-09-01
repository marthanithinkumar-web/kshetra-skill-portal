from pydantic import BaseModel, ConfigDict, HttpUrl
from typing import Optional, List
from datetime import datetime

class StudentEducationBase(BaseModel):
    institution: str
    degree: Optional[str]
    field_of_study: Optional[str]
    start_year: Optional[int]
    end_year: Optional[int]

class StudentEducationCreate(StudentEducationBase):
    pass

class StudentEducation(StudentEducationBase):
    id: int
    student_id: int
    model_config = ConfigDict(from_attributes=True)

class CertificationBase(BaseModel):
    name: str
    issuer: Optional[str]
    issue_date: Optional[datetime]
    url: Optional[HttpUrl]

class CertificationCreate(CertificationBase):
    pass

class Certification(CertificationBase):
    id: int
    student_id: int
    model_config = ConfigDict(from_attributes=True)

class ProjectBase(BaseModel):
    title: str
    description: Optional[str]
    repo_url: Optional[HttpUrl]
    demo_url: Optional[HttpUrl]

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    student_id: int
    created_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)

class SkillBase(BaseModel):
    name: str
    category: Optional[str]
    description: Optional[str]

class SkillCreate(SkillBase):
    pass

class Skill(SkillBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class StudentSkillBase(BaseModel):
    skill_id: int
    claimed_level: Optional[str]

class StudentSkillCreate(StudentSkillBase):
    pass

class StudentSkill(StudentSkillBase):
    id: int
    verified_level: Optional[str]
    score: Optional[float]
    confidence: Optional[float]
    evidence_count: Optional[int]
    last_verified_at: Optional[datetime]
    skill: Skill
    model_config = ConfigDict(from_attributes=True)

class CareerBase(BaseModel):
    name: str
    description: Optional[str]

class CareerCreate(CareerBase):
    pass

class Career(CareerBase):
    id: int
    skills: List[Skill] = []
    model_config = ConfigDict(from_attributes=True)

class JobRoleBase(BaseModel):
    career_id: int
    title: str
    description: Optional[str]

class JobRole(JobRoleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class StudentProfile(BaseModel):
    id: int
    user_id: int
    bio: Optional[str]
    location: Optional[str]
    target_career_id: Optional[int]
    educations: List[StudentEducation] = []
    certifications: List[Certification] = []
    projects: List[Project] = []
    skills: List[StudentSkill] = []

    model_config = ConfigDict(from_attributes=True)
