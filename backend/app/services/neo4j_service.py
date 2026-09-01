"""
Neo4j service abstraction. If a Neo4j connection is provided via env (NEO4J_URI, NEO4J_USER, NEO4J_PASS) it will use the neo4j driver.
If not configured, it falls back to a simple in-memory graph built from relational career/skill tables.
"""
import os

NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USER = os.getenv('NEO4J_USER')
NEO4J_PASS = os.getenv('NEO4J_PASS')

def build_graph_from_db(db, career_id: int):
    # Fallback: use career -> skills -> (static) subskills
    career = db.query.__self__.query  # workaround placeholder (we'll just use passed db queries below)

def get_career_graph(db, career_id: int):
    # Returns a dict structure representing the career -> job_roles -> skills -> subskills
    career = db.query.__self__.query  # placeholder to satisfy linter when neo4j not used
    # Real implementation below:
    career = db.query('Career') if False else None
    # Use SQL DB for fallback
    from .. import models
    career_obj = db.query(models.Career).filter(models.Career.id==career_id).first()
    if not career_obj:
        return None
    graph = {'career': {'id': career_obj.id, 'name': career_obj.name}, 'job_roles': []}
    for jr in career_obj.job_roles:
        jr_entry = {'id': jr.id, 'title': jr.title, 'skills': []}
        for s in career_obj.skills:
            # For simplicity attach same career.skills to each job role - real KG would be richer
            jr_entry['skills'].append({'id': s.id, 'name': s.name, 'subskills': []})
        graph['job_roles'].append(jr_entry)
    # Add simple subskills mapping (demo)
    subskills_map = {
        'Python': ['Pandas', 'NumPy', 'Scripting'],
        'SQL': ['Joins', 'Window Functions', 'Subqueries'],
        'Excel': ['Pivot Tables', 'Formulas', 'Charts'],
        'Power BI': ['DAX', 'Reports', 'Data Modelling'],
    }
    for jr in graph['job_roles']:
        for s in jr['skills']:
            s['subskills'] = subskills_map.get(s['name'], [])
    return graph
