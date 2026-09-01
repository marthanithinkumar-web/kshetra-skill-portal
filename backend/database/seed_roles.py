"""Simple script to insert default roles for Phase 1 demo."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
from backend.app.models import Role
from backend.app.core.config import settings
from backend.app.database import Base

engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine)

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    roles = [
        {"name": "student", "description": "Student / Learner"},
        {"name": "college", "description": "College / TPO"},
        {"name": "recruiter", "description": "Industry / Recruiter"},
        {"name": "admin", "description": "Platform Admin"},
    ]
    for r in roles:
        exists = db.query(Role).filter(Role.name == r['name']).first()
        if not exists:
            db.add(Role(name=r['name'], description=r.get('description')))
    db.commit()
    print('Default roles ensured.')
