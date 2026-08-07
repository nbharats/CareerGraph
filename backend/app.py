from flask import Flask
from database import get_driver
from flask_cors import CORS

app=Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

@app.route("/")
def home():
    return {
        "message": "CareerGraph API Running"
    }

@app.route("/seed")
def seed():

    driver = get_driver()

    with driver.session() as session:
        # Delete old graph
        session.run("""
            MATCH (n)
            DETACH DELETE n
        """)

        # Create new graph
        session.run("""

        CREATE

        // Students
        (bharat:Student {name:'Bharat'}),
        (rahul:Student {name:'Rahul'}),
        (priya:Student {name:'Priya'}),

        // Skills
        (python:Skill {name:'Python'}),
        (flask:Skill {name:'Flask'}),
        (react:Skill {name:'React'}),
        (neo4j:Skill {name:'Neo4j'}),
        (java:Skill {name:'Java'}),
        (sql:Skill {name:'SQL'}),
        (html:Skill {name:'HTML'}),
        (css:Skill {name:'CSS'}),

        // Companies
        (google:Company {name:'Google'}),
        (microsoft:Company {name:'Microsoft'}),
        (amazon:Company {name:'Amazon'}),
        (meta:Company {name:'Meta'}),
        (netflix:Company {name:'Netflix'}),

        // Jobs
        (backend:Job {title:'Backend Developer'}),
        (frontend:Job {title:'Frontend Developer'}),
        (fullstack:Job {title:'Full Stack Developer'}),
        (ai:Job {title:'AI Engineer'}),
        (data:Job {title:'Data Engineer'}),

        // College
        (rcee:College {name:'RCEE'}),

        // Bharat
        (bharat)-[:HAS_SKILL]->(python),
        (bharat)-[:HAS_SKILL]->(flask),
        (bharat)-[:LEARNING]->(react),
        (bharat)-[:ALUMNI_OF]->(rcee),

        // Rahul
        (rahul)-[:HAS_SKILL]->(java),
        (rahul)-[:HAS_SKILL]->(sql),
        (rahul)-[:ALUMNI_OF]->(rcee),

        // Priya
        (priya)-[:HAS_SKILL]->(react),
        (priya)-[:HAS_SKILL]->(html),
        (priya)-[:HAS_SKILL]->(css),
        (priya)-[:ALUMNI_OF]->(rcee),

        // Backend Job
        (backend)-[:REQUIRES]->(python),
        (backend)-[:REQUIRES]->(flask),
        (backend)-[:POSTED_BY]->(google),

        // Frontend Job
        (frontend)-[:REQUIRES]->(react),
        (frontend)-[:REQUIRES]->(html),
        (frontend)-[:REQUIRES]->(css),
        (frontend)-[:POSTED_BY]->(microsoft),

        // Full Stack Job
        (fullstack)-[:REQUIRES]->(python),
        (fullstack)-[:REQUIRES]->(react),
        (fullstack)-[:REQUIRES]->(sql),
        (fullstack)-[:POSTED_BY]->(amazon),

        // AI Job
        (ai)-[:REQUIRES]->(python),
        (ai)-[:REQUIRES]->(neo4j),
        (ai)-[:POSTED_BY]->(meta),

        // Data Job
        (data)-[:REQUIRES]->(python),
        (data)-[:REQUIRES]->(sql),
        (data)-[:POSTED_BY]->(netflix)
        """)
    return {
        "status":"success",
        "message":"Database Seeded Successfully"
    }

@app.route("/students")
def students():

    driver=get_driver()

    with driver.session() as session:

        result=session.run("""

        MATCH (s:Student)

        RETURN s.name AS student

        """)

        students=[]

        for record in result:
            students.append(record["student"])

        return students

@app.route("/jobs")
def jobs():

    driver=get_driver()

    with driver.session() as session:

        result=session.run("""

        MATCH (j:Job)

        RETURN j.title AS job

        """)

        jobs=[]

        for record in result:
            jobs.append(record["job"])

        return jobs

@app.route("/graph")
def graph():

    driver = get_driver()

    with driver.session() as session:

        result = session.run("""
        MATCH (n)
        RETURN labels(n) AS label, count(n) AS total
        """)

        data = []

        for record in result:
            data.append({
                "label": record["label"],
                "count": record["total"]
            })

        return data

@app.route("/recommend/<name>")
def recommend(name):

    driver = get_driver()

    with driver.session() as session:

        result = session.run("""
        MATCH (s:Student {name:$name})

        MATCH (j:Job)-[:POSTED_BY]->(c:Company)

        OPTIONAL MATCH (s)-[:HAS_SKILL]->(mySkill:Skill)
        OPTIONAL MATCH (j)-[:REQUIRES]->(jobSkill:Skill)

        WITH s,j,c,
             collect(DISTINCT mySkill.name) AS studentSkills,
             collect(DISTINCT jobSkill.name) AS requiredSkills

        RETURN
            j.title AS job,
            c.name AS company,
            [x IN requiredSkills WHERE x IN studentSkills] AS matchedSkills,
            [x IN requiredSkills WHERE NOT x IN studentSkills] AS missingSkills
        """, name=name)

        recommendations = []

        for record in result:

            matched = record["matchedSkills"]
            missing = record["missingSkills"]

            total_required = len(matched) + len(missing)

            if total_required == 0:
                score = 0
            else:
                score = round((len(matched) / total_required) * 100)

            recommendations.append({

                "job": record["job"],
                "company": record["company"],

                "matchScore": score,

                "matchedSkills": matched,
                "missingSkills": missing

            })

        recommendations.sort(
                key=lambda job: job["matchScore"],
                reverse=True
            )

        return recommendations

@app.route("/skills")
def skills():

    driver = get_driver()

    with driver.session() as session:

        result = session.run("""
            MATCH (s:Skill)
            RETURN s.name AS skill
            ORDER BY skill
        """)

        data = []

        for record in result:
            data.append(record["skill"])

        return data

@app.route("/companies")
def companies():

    driver = get_driver()

    with driver.session() as session:

        result = session.run("""
            MATCH (c:Company)
            RETURN c.name AS company
            ORDER BY company
        """)

        data = []

        for record in result:
            data.append(record["company"])

        return data

@app.route("/student/<name>")
def student(name):

    driver = get_driver()

    with driver.session() as session:

        result = session.run("""

        MATCH (s:Student {name:$name})

        OPTIONAL MATCH (s)-[:HAS_SKILL]->(skill:Skill)
        OPTIONAL MATCH (s)-[:LEARNING]->(learning:Skill)

        RETURN
            s.name AS name,
            collect(DISTINCT skill.name) AS skills,
            collect(DISTINCT learning.name) AS learning

        """, name=name)

        record = result.single()

        return {
            "name": record["name"],
            "skills": record["skills"],
            "learning": record["learning"]
        }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)