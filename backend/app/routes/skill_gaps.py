from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from typing import List
from . import verifications
from ..services import neo4j_service

router = APIRouter(prefix='/api/skill-gaps', tags=['skill-gaps'])

LEVEL_ORDER = { 'Beginner': 0, 'Intermediate': 1, 'Advanced': 2 }

@router.get('/{student_id}')
def compute_skill_gaps(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.id==student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail='Student not found')
    if not student.target_career_id:
        raise HTTPException(status_code=400, detail='Student has not selected a target career')
    career = db.query(models.Career).filter(models.Career.id==student.target_career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail='Career not found')
    # Ensure student skills are up-to-date: use student_skill table
    student_skills = { ss.skill_id: ss for ss in student.skills }
    # Career required skills from association table; required_level stored in career_skill_table (may be null)
    reqs = []
    conn = db.connection() if hasattr(db, 'connection') else None
    # Use career.skills list and try to read required_level from association via SQLAlchemy relationship property
    for s in career.skills:
        # SQLAlchemy doesn't expose required_level directly from secondary on objects without explicit association object.
        # For demo, assume required_level is 'Intermediate' for all required skills
        required_level = 'Intermediate'
        ss = student_skills.get(s.id)
        current_level = ss.verified_level if ss and ss.verified_level else None
        current_score = ss.score if ss else None
        # Compute gap severity
        gap = None
        priority = 'Low'
        if current_level is None:
            gap = 'Missing'
            priority = 'High'
        else:
            req_ord = LEVEL_ORDER.get(required_level, 1)
            cur_ord = LEVEL_ORDER.get(current_level, 0)
            diff = req_ord - cur_ord
            if diff <= 0:
                gap = 'Matched'
                priority = 'Low'
            elif diff == 1:
                gap = 'Partially Matched'
                priority = 'Medium'
            else:
                gap = 'Missing'
                priority = 'High'
        reqs.append({
            'skill_id': s.id,
            'skill_name': s.name,
            'required_level': required_level,
            'current_level': current_level or 'None',
            'current_score': current_score,
            'gap': gap,
            'priority': priority
        })
    # Generate personalized roadmap
    roadmap_items = []
    seq = 1
    for r in sorted(reqs, key=lambda x: ('High'==x['priority'], 'Medium'==x['priority']), reverse=True):
        if r['gap'] == 'Matched':
            continue
        # Recommendations: use neo4j graph to propose subskills and sequence
        graph = neo4j_service.get_career_graph(db, career.id)
        recs = []
        # find subskills for this skill in graph
        if graph:
            for jr in graph.get('job_roles', []):
                for sk in jr.get('skills', []):
                    if sk['id'] == r['skill_id']:
                        recs = sk.get('subskills', [])
        if not recs:
            recs = [f'Practice core topics of {r["skill_name"]}', f'Take hands-on project on {r["skill_name"]}']
        roadmap_items.append({
            'skill_id': r['skill_id'],
            'skill_name': r['skill_name'],
            'current_level': r['current_level'],
            'target_level': r['required_level'],
            'priority': r['priority'],
            'recommendations': recs,
            'sequence': seq
        })
        seq += 1
    # Persist roadmap
    roadmap = models.Roadmap(student_id=student.id, title=f'Roadmap for {career.name}', description=f'Personalized roadmap to reach required skills for {career.name}')
    db.add(roadmap)
    db.commit()
    db.refresh(roadmap)
    for item in roadmap_items:
        ri = models.RoadmapItem(roadmap_id=roadmap.id, skill_id=item['skill_id'], current_level=item['current_level'], target_level=item['target_level'], priority=item['priority'], recommendations='; '.join(item['recommendations']), sequence=item['sequence'])
        db.add(ri)
    db.commit()
    # Return structured response
    return {
        'student_id': student.id,
        'career': {'id': career.id, 'name': career.name},
        'skill_gaps': reqs,
        'roadmap': {
            'id': roadmap.id,
            'title': roadmap.title,
            'items': [ { 'skill_id': i.skill_id, 'skill_name': i.skill.name, 'current_level': i.current_level, 'target_level': i.target_level, 'priority': i.priority, 'recommendations': i.recommendations.split('; '), 'sequence': i.sequence } for i in roadmap.items ]
        }
    }
