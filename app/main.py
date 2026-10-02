from fastapi import FastAPI, Query
from app.database import get_connection
from app.career_assistant import generate_career_advice


app = FastAPI(
    title="AI Job Market Intelligence API",
    description="API for analyzing job market data, skills, and career opportunities",
    version="1.0.0"
)


# ==================================================
# HOME
# ==================================================

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "AI Job Market Intelligence API is running!"
    }


# ==================================================
# TEST DATABASE CONNECTION
# ==================================================

@app.get("/test-db")
def test_database():

    connection = get_connection()

    if connection is None:
        return {
            "status": "error",
            "message": "Could not connect to MySQL database"
        }

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs")

    result = cursor.fetchone()

    cursor.close()
    connection.close()

    return {
        "status": "success",
        "message": "MySQL database connected successfully",
        "total_jobs": result[0]
    }


# ==================================================
# JOB SEARCH API
# ==================================================

@app.get("/jobs")
def get_jobs(
    limit: int = Query(20, ge=1, le=100),
    title: str = None,
    location: str = None,
    remote: bool = None
):

    connection = get_connection()

    if connection is None:
        return {
            "status": "error",
            "message": "Could not connect to MySQL database"
        }

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            job_id,
            company_name,
            title,
            location,
            experience_level,
            work_type,
            remote_allowed,
            min_salary,
            max_salary,
            currency
        FROM jobs
        WHERE 1=1
    """

    params = []

    # Job title filter
    if title:
        query += " AND title LIKE %s"
        params.append(f"%{title}%")

    # Location filter
    if location:
        query += " AND location LIKE %s"
        params.append(f"%{location}%")

    # Remote filter
    if remote is not None:
        query += " AND remote_allowed = %s"
        params.append(remote)

    query += " LIMIT %s"
    params.append(limit)

    cursor.execute(query, tuple(params))

    jobs = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "status": "success",
        "count": len(jobs),
        "jobs": jobs
    }


# ==================================================
# OVERALL SKILL DEMAND API
# ==================================================

@app.get("/skills")
def get_skills():

    connection = get_connection()

    if connection is None:
        return {
            "status": "error",
            "message": "Could not connect to MySQL database"
        }

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            skill,
            job_count,
            percentage
        FROM skill_demand
        ORDER BY job_count DESC
        LIMIT 20
    """

    cursor.execute(query)

    skills = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "status": "success",
        "count": len(skills),
        "skills": skills
    }


# ==================================================
# ROLE-WISE SKILL DEMAND API
# ==================================================

@app.get("/role-skills")
def get_role_skills(role: str = None):

    connection = get_connection()

    if connection is None:
        return {
            "status": "error",
            "message": "Could not connect to MySQL database"
        }

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            role,
            skill,
            job_count,
            percentage
        FROM role_skill_demand
    """

    params = []

    if role:
        query += " WHERE role LIKE %s"
        params.append(f"%{role}%")

    query += " ORDER BY role, job_count DESC"

    cursor.execute(query, tuple(params))

    results = cursor.fetchall()

    cursor.close()
    connection.close()

    return {
        "status": "success",
        "count": len(results),
        "role_skills": results
    }


# ==================================================
# SKILL GAP ANALYSIS API
# ==================================================

@app.get("/skill-gap")
def skill_gap(
    role: str,
    skills: str
):

    connection = get_connection()

    if connection is None:
        return {
            "status": "error",
            "message": "Could not connect to MySQL database"
        }

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            skill,
            job_count,
            percentage
        FROM role_skill_demand
        WHERE role LIKE %s
        ORDER BY job_count DESC
    """

    cursor.execute(query, (f"%{role}%",))

    required_skills = cursor.fetchall()

    if not required_skills:
        cursor.close()
        connection.close()

        return {
            "status": "error",
            "message": f"No skill data found for role: {role}"
        }

    cursor.close()
    connection.close()

    # Convert user's skills into a list
    user_skills = [
        skill.strip().lower()
        for skill in skills.split(",")
        if skill.strip()
    ]

    matched_skills = []
    missing_skills = []

    # Compare skills
    for item in required_skills:

        required_skill = item["skill"].lower()

        if required_skill in user_skills:
            matched_skills.append(item)
        else:
            missing_skills.append(item)

    # Calculate match percentage
    total_required = len(required_skills)

    match_percentage = round(
        (len(matched_skills) / total_required) * 100,
        2
    )

    return {
        "status": "success",
        "role": role,
        "total_required_skills": total_required,
        "skill_match_percentage": match_percentage,
        "your_skills": user_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }


# ==================================================
# CAREER ASSISTANT API
# ==================================================

@app.get("/career-advice")
def career_advice(
    role: str,
    skills: str
):

    connection = get_connection()

    if connection is None:
        return {
            "status": "error",
            "message": "Could not connect to MySQL database"
        }

    cursor = connection.cursor(dictionary=True)

    query = """
        SELECT
            skill,
            job_count,
            percentage
        FROM role_skill_demand
        WHERE role LIKE %s
        ORDER BY job_count DESC
    """

    cursor.execute(query, (f"%{role}%",))

    required_skills = cursor.fetchall()

    # Validate role
    if not required_skills:

        cursor.close()
        connection.close()

        return {
            "status": "error",
            "message": f"No skill data found for role: {role}"
        }

    cursor.close()
    connection.close()

    # Convert user's skills into a list
    user_skills = [
        skill.strip().lower()
        for skill in skills.split(",")
        if skill.strip()
    ]

    matched_skills = []
    missing_skills = []

    # Compare user's skills with market requirements
    for item in required_skills:

        required_skill = item["skill"].lower()

        if required_skill in user_skills:
            matched_skills.append(item)
        else:
            missing_skills.append(item)

    # Calculate skill match percentage
    total_required = len(required_skills)

    match_percentage = round(
        (len(matched_skills) / total_required) * 100,
        2
    )

    # Generate career advice
    advice = generate_career_advice(
        role,
        matched_skills,
        missing_skills
    )

    return {
        "status": "success",
        "role": role,
        "total_required_skills": total_required,
        "skill_match_percentage": match_percentage,
        "your_skills": user_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "career_advice": advice
    }