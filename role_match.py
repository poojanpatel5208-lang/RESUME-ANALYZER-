# ============================================================
# role_match.py
# ------------------------------------------------------------
# This file handles:
#   1. Generating resume strengths based on found skills
#   2. Generating resume weaknesses based on missing skills
#   3. Generating personalized improvement suggestions
# ============================================================

from skills import ROLE_REQUIREMENTS


# ---------------------------------------------------------------
# FUNCTION: generate_strengths
# ---------------------------------------------------------------
# Purpose:
#   List positive aspects of the resume based on what the
#   candidate already has.
#
# Parameters:
#   resume_skills  (list) : skills found in the resume
#   matched_skills (list) : skills matching the selected role
#   sections       (dict) : {"projects": bool, "education": bool, "contact": bool}
#
# Returns:
#   list of strength statements (strings)
# ---------------------------------------------------------------
def generate_strengths(resume_skills, matched_skills, sections):
    strengths = []

    # Strength from skill count
    if len(resume_skills) >= 10:
        strengths.append(f"Strong technical profile with {len(resume_skills)} skills detected.")
    elif len(resume_skills) >= 5:
        strengths.append(f"Decent technical skills ({len(resume_skills)} skills found).")

    # Strength from role match
    if len(matched_skills) >= 7:
        strengths.append("Excellent skill match for the selected role.")
    elif len(matched_skills) >= 4:
        strengths.append("Good skill overlap with the selected role requirements.")

    # Section-based strengths
    if sections.get("projects"):
        strengths.append("Projects section present — great for showcasing practical experience.")
    if sections.get("education"):
        strengths.append("Education section is clearly mentioned.")
    if sections.get("contact"):
        strengths.append("Contact information is available for recruiters.")

    # Specific skill strengths
    ai_skills = {"Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch"}
    found_ai = ai_skills.intersection(set(resume_skills))
    if found_ai:
        strengths.append(f"Has core AI/ML skills: {', '.join(found_ai)}.")

    data_skills = {"SQL", "Pandas", "NumPy", "Power BI", "Tableau"}
    found_data = data_skills.intersection(set(resume_skills))
    if found_data:
        strengths.append(f"Has data skills: {', '.join(found_data)}.")

    if not strengths:
        strengths.append("Resume was uploaded successfully and is readable.")

    return strengths


# ---------------------------------------------------------------
# FUNCTION: generate_weaknesses
# ---------------------------------------------------------------
# Purpose:
#   Identify problem areas in the resume.
#
# Parameters:
#   missing_skills (list) : skills required but not found
#   sections       (dict) : resume section presence flags
#   match_pct      (float): skill match percentage
#
# Returns:
#   list of weakness statements (strings)
# ---------------------------------------------------------------
def generate_weaknesses(missing_skills, sections, match_pct):
    weaknesses = []

    # Low skill match
    if match_pct < 40:
        weaknesses.append("Very low skill match for the selected role.")
    elif match_pct < 60:
        weaknesses.append("Skill match is below average — more relevant skills needed.")

    # Missing sections
    if not sections.get("projects"):
        weaknesses.append("No Projects section detected — this is critical for students.")
    if not sections.get("education"):
        weaknesses.append("Education section not clearly found.")
    if not sections.get("contact"):
        weaknesses.append("Contact information (email/phone) not found.")

    # Too many missing skills
    if len(missing_skills) > 5:
        weaknesses.append(f"{len(missing_skills)} required skills are missing for the selected role.")

    # Missing critical skills
    critical = ["Python", "Git", "SQL"]
    for skill in critical:
        if skill in missing_skills:
            weaknesses.append(f"Missing critical skill: {skill}.")

    if not weaknesses:
        weaknesses.append("No major weaknesses detected. Minor tweaks may still help.")

    return weaknesses


# ---------------------------------------------------------------
# FUNCTION: generate_suggestions
# ---------------------------------------------------------------
# Purpose:
#   Provide actionable, personalized tips to improve the resume.
#
# Parameters:
#   missing_skills (list) : skills required but absent in resume
#   sections       (dict) : resume section presence
#   role           (str)  : selected internship role
#   match_pct      (float): skill match percentage
#
# Returns:
#   list of suggestion strings
# ---------------------------------------------------------------
def generate_suggestions(missing_skills, sections, role, match_pct):
    suggestions = []

    # Suggestions for missing sections
    if not sections.get("projects"):
        suggestions.append(
            "📁 Add a 'Projects' section with at least 2–3 hands-on projects "
            "using your tech stack. This is the #1 thing recruiters look for in students."
        )

    if not sections.get("contact"):
        suggestions.append(
            "📧 Add your email, phone number, and LinkedIn profile at the top of your resume."
        )

    # Suggest GitHub
    suggestions.append(
        "🔗 Include your GitHub profile link. Recruiters check it to see your actual code."
    )

    # Skill-based suggestions
    for skill in missing_skills[:5]:   # Show top 5 missing skill suggestions
        suggestions.append(f"📚 Learn and add '{skill}' to your resume for the {role} role.")

    # Role-specific tips
    if role == "AI/ML Intern":
        suggestions.append(
            "🤖 Build a simple ML project (e.g., house price prediction, spam classifier) "
            "and upload it to GitHub."
        )
        suggestions.append(
            "📊 Practice on Kaggle competitions and mention your Kaggle profile."
        )

    elif role == "Data Analyst Intern":
        suggestions.append(
            "📈 Build a data analysis project using real datasets from Kaggle or government sources."
        )
        suggestions.append(
            "📊 Create Power BI or Tableau dashboards and include screenshots in your portfolio."
        )

    elif role == "Python Developer Intern":
        suggestions.append(
            "🐍 Build a Python project using Django or Flask (e.g., a simple web app or REST API)."
        )

    elif role == "Web Developer Intern":
        suggestions.append(
            "🌐 Build a responsive personal portfolio website and host it on GitHub Pages for free."
        )

    # General suggestions
    suggestions.append(
        "✍️ Use strong action verbs in your project descriptions: "
        "'Developed', 'Built', 'Implemented', 'Deployed', 'Designed'."
    )
    suggestions.append(
        "📏 Quantify your achievements: instead of 'Built a classifier', "
        "write 'Built a spam classifier with 94% accuracy using Scikit-Learn'."
    )
    suggestions.append(
        "🗂️ Keep your resume to 1 page if you have less than 1 year of experience."
    )

    if match_pct < 60:
        suggestions.append(
            "🎯 Your skill match is below 60%. Focus on learning the missing skills "
            "before applying to this role."
        )

    return suggestions
