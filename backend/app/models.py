from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text, Float, Table
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

# Association tables
career_skill_table = Table(
    'career_skills',
    Base.metadata,
    Column('career_id', Integer, ForeignKey('careers.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True),
    Column('required_level', String(50), nullable=True)
)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    role = relationship("Role")
    student = relationship("Student", uselist=False, back_populates="user")

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    target_career_id = Column(Integer, ForeignKey('careers.id'), nullable=True)
    bio = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='student')
    educations = relationship('StudentEducation', back_populates='student', cascade='all, delete-orphan')
    certifications = relationship('Certification', back_populates='student', cascade='all, delete-orphan')
    projects = relationship('Project', back_populates='student', cascade='all, delete-orphan')
    skills = relationship('StudentSkill', back_populates='student', cascade='all, delete-orphan')
    target_career = relationship('Career')

class StudentEducation(Base):
    __tablename__ = 'student_education'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    institution = Column(String(255), nullable=False)
    degree = Column(String(255), nullable=True)
    field_of_study = Column(String(255), nullable=True)
    start_year = Column(Integer, nullable=True)
    end_year = Column(Integer, nullable=True)

    student = relationship('Student', back_populates='educations')

class Certification(Base):
    __tablename__ = 'certifications'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    name = Column(String(255), nullable=False)
    issuer = Column(String(255), nullable=True)
    issue_date = Column(DateTime, nullable=True)
    url = Column(String(1024), nullable=True)

    student = relationship('Student', back_populates='certifications')

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    repo_url = Column(String(1024), nullable=True)
    demo_url = Column(String(1024), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship('Student', back_populates='projects')

class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), unique=True, nullable=False)
    category = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)

    careers = relationship('Career', secondary=career_skill_table, back_populates='skills')
    student_skills = relationship('StudentSkill', back_populates='skill')

class Career(Base):
    __tablename__ = 'careers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)

    skills = relationship('Skill', secondary=career_skill_table, back_populates='careers')
    job_roles = relationship('JobRole', back_populates='career')

class JobRole(Base):
    __tablename__ = 'job_roles'
    id = Column(Integer, primary_key=True, index=True)
    career_id = Column(Integer, ForeignKey('careers.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    career = relationship('Career', back_populates='job_roles')

class StudentSkill(Base):
    __tablename__ = 'student_skills'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    claimed_level = Column(String(50), nullable=True)
    verified_level = Column(String(50), nullable=True)
    score = Column(Float, nullable=True)
    confidence = Column(Float, nullable=True)
    evidence_count = Column(Integer, default=0)
    last_verified_at = Column(DateTime, nullable=True)

    student = relationship('Student', back_populates='skills')
    skill = relationship('Skill', back_populates='student_skills')

# Assessment and Evidence Models
class Assessment(Base):
    __tablename__ = 'assessments'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    duration_minutes = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    questions = relationship('AssessmentQuestion', back_populates='assessment', cascade='all, delete-orphan')
    skill = relationship('Skill')

class AssessmentQuestion(Base):
    __tablename__ = 'assessment_questions'
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey('assessments.id'), nullable=False)
    prompt = Column(Text, nullable=False)
    choices = Column(Text, nullable=True)  # JSON-encoded choices for MCQ
    answer = Column(Text, nullable=True)   # expected answer or key
    max_marks = Column(Float, default=1.0)

    assessment = relationship('Assessment', back_populates='questions')

class AssessmentAttempt(Base):
    __tablename__ = 'assessment_attempts'
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey('assessments.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    submitted_at = Column(DateTime, nullable=True)
    score = Column(Float, nullable=True)

    answers = relationship('AttemptAnswer', back_populates='attempt', cascade='all, delete-orphan')
    assessment = relationship('Assessment')
    student = relationship('Student')

class AttemptAnswer(Base):
    __tablename__ = 'attempt_answers'
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey('assessment_attempts.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('assessment_questions.id'), nullable=False)
    response = Column(Text, nullable=True)
    marks_obtained = Column(Float, nullable=True)

    attempt = relationship('AssessmentAttempt', back_populates='answers')
    question = relationship('AssessmentQuestion')

class PracticalTask(Base):
    __tablename__ = 'practical_tasks'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    skill = relationship('Skill')
    submissions = relationship('PracticalSubmission', back_populates='task', cascade='all, delete-orphan')

class PracticalSubmission(Base):
    __tablename__ = 'practical_submissions'
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('practical_tasks.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    submission_text = Column(Text, nullable=True)
    repo_url = Column(String(1024), nullable=True)
    score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship('PracticalTask', back_populates='submissions')
    student = relationship('Student')

class Evidence(Base):
    __tablename__ = 'evidence'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    evidence_type = Column(String(50), nullable=False)  # e.g., coding_assessment, practical_task, project, interview, github
    reference_id = Column(Integer, nullable=True)  # FK to relevant entity (attempt id, submission id, project id)
    score = Column(Float, nullable=True)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship('Student')
    skill = relationship('Skill')

class SkillVerificationHistory(Base):
    __tablename__ = 'skill_verification_history'
    id = Column(Integer, primary_key=True, index=True)
    student_skill_id = Column(Integer, ForeignKey('student_skills.id'), nullable=False)
    score = Column(Float, nullable=False)
    verified_level = Column(String(50), nullable=True)
    confidence = Column(Float, nullable=True)
    evidence_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    student_skill = relationship('StudentSkill')

class VerificationWeights(Base):
    __tablename__ = 'verification_weights'
    id = Column(Integer, primary_key=True, index=True)
    coding_assessment = Column(Float, default=0.25)
    practical_task = Column(Float, default=0.25)
    project_evidence = Column(Float, default=0.20)
    technical_explanation = Column(Float, default=0.15)
    github_evidence = Column(Float, default=0.15)
    updated_at = Column(DateTime, default=datetime.utcnow)

# Roadmaps
class Roadmap(Base):
    __tablename__ = 'roadmaps'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship('RoadmapItem', back_populates='roadmap', cascade='all, delete-orphan')
    student = relationship('Student')

class RoadmapItem(Base):
    __tablename__ = 'roadmap_items'
    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey('roadmaps.id'), nullable=False)
    skill_id = Column(Integer, ForeignKey('skills.id'), nullable=False)
    current_level = Column(String(50), nullable=True)
    target_level = Column(String(50), nullable=True)
    priority = Column(String(20), nullable=True)
    recommendations = Column(Text, nullable=True)
    sequence = Column(Integer, nullable=True)

    roadmap = relationship('Roadmap', back_populates='items')
    skill = relationship('Skill')

# Recruiter / Jobs
job_skill_table = Table(
    'job_skills',
    Base.metadata,
    Column('job_id', Integer, ForeignKey('jobs.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True),
    Column('required_level', String(50), nullable=True)
)

# Separate association table for internships to avoid SQLAlchemy join ambiguity
internship_skill_table = Table(
    'internship_skills',
    Base.metadata,
    Column('internship_id', Integer, ForeignKey('internships.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True),
    Column('required_level', String(50), nullable=True)
)

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    website = Column(String(1024), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    jobs = relationship('Job', back_populates='company')
    internships = relationship('Internship', back_populates='company')

class Job(Base):
    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    mode = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship('Company', back_populates='jobs')
    skills = relationship('Skill', secondary=job_skill_table)
    applications = relationship('Application', back_populates='job')

class Internship(Base):
    __tablename__ = 'internships'
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(String(255), nullable=True)
    mode = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    company = relationship('Company', back_populates='internships')
    skills = relationship('Skill', secondary=internship_skill_table)
    applications = relationship('Application', back_populates='internship')

class Application(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('jobs.id'), nullable=True)
    internship_id = Column(Integer, ForeignKey('internships.id'), nullable=True)
    cover_letter = Column(Text, nullable=True)
    status = Column(String(50), default='applied')
    shortlisted = Column(Boolean, default=False)
    applied_at = Column(DateTime, default=datetime.utcnow)

    student = relationship('Student')
    job = relationship('Job', back_populates='applications')
    internship = relationship('Internship', back_populates='applications')

class RevokedToken(Base):
    __tablename__ = 'revoked_tokens'
    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
