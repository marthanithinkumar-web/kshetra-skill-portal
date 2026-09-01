from sqlalchemy.orm import Session
from .. import models
from datetime import datetime

# Map numeric score to level
def score_to_level(score: float) -> str:
    if score >= 80:
        return 'Advanced'
    if score >= 50:
        return 'Intermediate'
    return 'Beginner'

# Default weights if none configured in DB
DEFAULT_WEIGHTS = {
    'coding_assessment': 0.25,
    'practical_task': 0.25,
    'project_evidence': 0.20,
    'technical_explanation': 0.15,
    'github_evidence': 0.15,
}

# Ensure verification engine follows the hybrid architecture decision:
# - Rule-based weighted scoring is the primary method
# - Missing evidence types are treated explicitly (excluded from weighted average)
# - Weights are configurable via API (VerificationWeights table)
# - No ML model training happens here; small ML components may be added separately and invoked by services when needed

def get_weights(db: Session) -> dict:
    w = db.query(models.VerificationWeights).order_by(models.VerificationWeights.id.desc()).first()
    if not w:
        return DEFAULT_WEIGHTS
    return {
        'coding_assessment': w.coding_assessment,
        'practical_task': w.practical_task,
        'project_evidence': w.project_evidence,
        'technical_explanation': w.technical_explanation,
        'github_evidence': w.github_evidence,
    }

def aggregate_evidence(db: Session, student_id: int, skill_id: int) -> dict:
    # Collect evidence by type and compute average score per type
    rows = db.query(models.Evidence).filter(models.Evidence.student_id==student_id, models.Evidence.skill_id==skill_id).all()
    by_type = {}
    for r in rows:
        by_type.setdefault(r.evidence_type, []).append(r.score or 0.0)
    aggregates = {}
    for k, v in by_type.items():
        if len(v) == 0:
            aggregates[k] = None
        else:
            # assume scores are 0-100; compute average
            aggregates[k] = sum(v)/len(v)
    return aggregates

def compute_verification(db: Session, student_id: int, skill_id: int) -> dict:
    weights = get_weights(db)
    aggregates = aggregate_evidence(db, student_id, skill_id)
    # For any missing evidence type, treat score as None and reduce total weight for confidence
    total_weight = 0.0
    weighted_sum = 0.0
    evidence_count = 0
    for etype, w in weights.items():
        score = aggregates.get(etype)
        if score is None:
            continue
        # clamp/normalize
        s = max(0.0, min(100.0, float(score)))
        weighted_sum += s * w
        total_weight += w
        evidence_count += len([x for x in db.query(models.Evidence).filter(models.Evidence.student_id==student_id, models.Evidence.skill_id==skill_id, models.Evidence.evidence_type==etype).all()])
    # If no evidence, return minimal
    if total_weight == 0:
        final_score = 0.0
        confidence = 0.0
    else:
        # Normalize weighted sum to 0-100 by dividing by total weight
        final_score = weighted_sum / total_weight
        # Confidence: proportion of weights present * (0.5 + 0.5 * evidence_count_factor)
        weight_coverage = total_weight / sum(weights.values())
        evidence_count_factor = min(1.0, evidence_count / 5.0)  # saturates at 5 evidences
        confidence = weight_coverage * (0.5 + 0.5 * evidence_count_factor) * 100.0
    # Map to level
    level = score_to_level(final_score)

    # Update or create StudentSkill entry
    student_skill = db.query(models.StudentSkill).filter(models.StudentSkill.student_id==student_id, models.StudentSkill.skill_id==skill_id).first()
    if not student_skill:
        student_skill = models.StudentSkill(student_id=student_id, skill_id=skill_id)
        db.add(student_skill)
    student_skill.score = float(final_score)
    student_skill.verified_level = level
    student_skill.confidence = float(confidence)
    student_skill.evidence_count = evidence_count
    student_skill.last_verified_at = datetime.utcnow()
    db.add(student_skill)
    db.commit()
    db.refresh(student_skill)

    # Record history
    hist = models.SkillVerificationHistory(student_skill_id=student_skill.id, score=final_score, verified_level=level, confidence=confidence, evidence_count=evidence_count)
    db.add(hist)
    db.commit()

    return {
        'student_skill_id': student_skill.id,
        'score': final_score,
        'verified_level': level,
        'confidence': confidence,
        'evidence_count': evidence_count,
        'verified_at': student_skill.last_verified_at,
        'per_type_aggregates': aggregates,
        'weights_used': weights,
    }
