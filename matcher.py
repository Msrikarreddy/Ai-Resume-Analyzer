
import re

SKILL_ALIASES = {
    "Python": ["python"],
    "SQL": ["sql", "structured query language"],
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning"],
    "NLP": ["natural language processing", "nlp"],
    "Data Analysis": ["data analysis", "data analytics"],
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "Scikit-learn": ["scikit-learn", "scikit learn", "sklearn"],
    "TensorFlow": ["tensorflow"],
    "PyTorch": ["pytorch"],
    "Power BI": ["power bi"],
    "Tableau": ["tableau"],
    "Excel": ["excel", "microsoft excel"],
    "Java": ["java"],
    "JavaScript": ["javascript"],
    "React": ["react", "react.js"],
    "HTML": ["html"],
    "CSS": ["css"],
    "FastAPI": ["fastapi"],
    "Flask": ["flask"],
    "Django": ["django"],
    "Git": ["git"],
    "Docker": ["docker"],
    "AWS": ["aws", "amazon web services"],
}


def find_skills(text):
    """Find known skills mentioned in text."""
    found = set()
    text = text.lower()

    for skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            pattern = (
                r"(?<!\w)" + re.escape(alias) + r"(?!\w)"
            )

            if re.search(pattern, text):
                found.add(skill)
                break

    return found


def compare_skills(resume_text, job_description):
    """Compare resume skills with job requirements."""

    resume_skills = find_skills(resume_text)
    job_skills = find_skills(job_description)

    matched_skills = sorted(resume_skills & job_skills)
    missing_skills = sorted(job_skills - resume_skills)

    if job_skills:
        match_percentage = round(
            len(matched_skills) / len(job_skills) * 100,
            1
        )
    else:
        match_percentage = None

    return {
        "resume_skills": sorted(resume_skills),
        "job_skills": sorted(job_skills),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": match_percentage,
    }