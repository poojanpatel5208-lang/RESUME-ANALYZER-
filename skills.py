# ============================================================
# skills.py
# ------------------------------------------------------------
# This file stores:
#   1. All technical skills we can detect in a resume
#   2. Required skills for each internship role
#   3. A function to match resume skills to role skills
# ============================================================

# ---------------------------------------------------------------
# SKILLS DATABASE
# A list of all technical skills the system can detect.
# We search for these keywords inside the resume text.
# ---------------------------------------------------------------
ALL_SKILLS = [
    # Programming Languages
    "Python", "Java", "C++", "C", "R", "JavaScript", "TypeScript",
    "Kotlin", "Swift", "Go", "Rust", "PHP", "Ruby", "Scala",

    # Web Development
    "HTML", "CSS", "React", "Node.js", "Django", "Flask", "FastAPI",
    "Bootstrap", "jQuery", "REST API",

    # Data & AI/ML
    "Machine Learning", "Deep Learning", "Natural Language Processing",
    "Computer Vision", "Data Science", "Data Analysis",
    "TensorFlow", "PyTorch", "Keras", "Scikit-Learn",
    "Pandas", "NumPy", "Matplotlib", "Seaborn", "OpenCV",
    "Hugging Face", "LangChain",

    # Databases
    "SQL", "MySQL", "PostgreSQL", "MongoDB", "SQLite", "Firebase",
    "Redis", "Oracle",

    # Data Visualization & BI
    "Power BI", "Tableau", "Excel", "Google Sheets",

    # Tools & Platforms
    "Git", "GitHub", "Docker", "Kubernetes", "Linux", "AWS",
    "Google Cloud", "Azure", "VS Code", "Jupyter Notebook",

    # Other
    "Statistics", "Mathematics", "Probability",
    "Data Structures", "Algorithms", "OOP",
]


# ---------------------------------------------------------------
# ROLE REQUIREMENTS
# Each role has a list of skills a recruiter (ATS) looks for.
# We compare these against what the resume has.
# ---------------------------------------------------------------
ROLE_REQUIREMENTS = {
    "AI/ML Intern": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "Pandas",
        "NumPy",
        "Scikit-Learn",
        "TensorFlow",
        "PyTorch",
        "Matplotlib",
        "Statistics",
        "Git",
    ],
    "Data Analyst Intern": [
        "Python",
        "SQL",
        "Excel",
        "Power BI",
        "Tableau",
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Seaborn",
        "Statistics",
        "Data Analysis",
    ],
    "Python Developer Intern": [
        "Python",
        "Django",
        "Flask",
        "REST API",
        "SQL",
        "Git",
        "GitHub",
        "OOP",
        "Data Structures",
        "Algorithms",
    ],
    "Web Developer Intern": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Node.js",
        "Bootstrap",
        "Git",
        "GitHub",
        "REST API",
        "SQL",
    ],
}


# ---------------------------------------------------------------
# FUNCTION: get_matched_and_missing_skills
# ---------------------------------------------------------------
# Purpose:
#   Given a list of skills found in the resume and the target role,
#   return two lists:
#     - matched_skills : skills the resume HAS that the role needs
#     - missing_skills : skills the resume is MISSING for that role
#
# Parameters:
#   resume_skills (list) : skills extracted from the resume
#   role (str)           : selected internship role name
#
# Returns:
#   tuple (matched_skills, missing_skills)
# ---------------------------------------------------------------
def get_matched_and_missing_skills(resume_skills, role):
    required = ROLE_REQUIREMENTS.get(role, [])

    # Convert everything to lowercase for fair comparison
    resume_lower = [s.lower() for s in resume_skills]

    matched_skills = []
    missing_skills = []

    for skill in required:
        if skill.lower() in resume_lower:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    return matched_skills, missing_skills


# ---------------------------------------------------------------
# FUNCTION: calculate_match_percentage
# ---------------------------------------------------------------
# Purpose:
#   Calculate how many required skills are present in the resume.
#
# Formula:
#   (matched skills / total required skills) × 100
#
# Parameters:
#   matched_skills (list) : skills found in both resume and role
#   role (str)            : selected internship role
#
# Returns:
#   float : match percentage (0.0 to 100.0)
# ---------------------------------------------------------------
def calculate_match_percentage(matched_skills, role):
    required = ROLE_REQUIREMENTS.get(role, [])
    if len(required) == 0:
        return 0.0
    return round((len(matched_skills) / len(required)) * 100, 2)


# ---------------------------------------------------------------
# FUNCTION: predict_best_role
# ---------------------------------------------------------------
# Purpose:
#   Auto-suggest the best role based on the resume's skills.
#   Checks all roles, picks the one with the highest match %.
#
# Parameters:
#   resume_skills (list) : skills extracted from resume
#
# Returns:
#   tuple (best_role, best_score)
# ---------------------------------------------------------------
def predict_best_role(resume_skills):
    best_role = None
    best_score = -1

    for role in ROLE_REQUIREMENTS:
        matched, _ = get_matched_and_missing_skills(resume_skills, role)
        score = calculate_match_percentage(matched, role)
        if score > best_score:
            best_score = score
            best_role = role

    return best_role, round(best_score, 2)
