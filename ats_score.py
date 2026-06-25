# ============================================================
# ats_score.py
# ------------------------------------------------------------
# This file calculates the ATS (Applicant Tracking System) Score.
#
# WHAT IS ATS?
#   ATS is software used by companies to automatically screen
#   resumes. It scores your resume based on keywords, sections,
#   and relevance to the job description.
#
# OUR ATS SCORE FORMULA (out of 100):
#   Skill Match Score  = 60% weightage
#   Projects Section   = 20% weightage
#   Education Section  = 10% weightage
#   Contact Info       = 10% weightage
# ============================================================


# ---------------------------------------------------------------
# FUNCTION: calculate_ats_score
# ---------------------------------------------------------------
# Purpose:
#   Compute an ATS score out of 100 for the given resume.
#
# Parameters:
#   match_percentage (float) : skill match % (0 to 100)
#   sections (dict)          : {"projects": bool, "education": bool, "contact": bool}
#
# Returns:
#   dict with:
#     - total_score     : final ATS score (int, 0–100)
#     - skill_score     : points from skill matching (max 60)
#     - project_score   : points from projects section (0 or 20)
#     - education_score : points from education section (0 or 10)
#     - contact_score   : points from contact info (0 or 10)
#     - breakdown       : human-readable summary of scoring
# ---------------------------------------------------------------
def calculate_ats_score(match_percentage, sections):

    # --- Component 1: Skill Match (60% of total) ---
    # If match% = 80%, then skill_score = 0.60 × 80 = 48 points
    skill_score = round(0.60 * match_percentage)

    # --- Component 2: Projects Section (20 points) ---
    # If resume has a projects section → 20 points, else 0
    project_score = 20 if sections.get("projects", False) else 0

    # --- Component 3: Education Section (10 points) ---
    education_score = 10 if sections.get("education", False) else 0

    # --- Component 4: Contact Information (10 points) ---
    contact_score = 10 if sections.get("contact", False) else 0

    # --- Total ATS Score ---
    total_score = skill_score + project_score + education_score + contact_score

    # Cap the score at 100 (just in case)
    total_score = min(total_score, 100)

    # Breakdown for displaying to the user
    breakdown = {
        "Skill Match (60%)": f"{skill_score}/60",
        "Projects Section (20%)": f"{project_score}/20",
        "Education Section (10%)": f"{education_score}/10",
        "Contact Info (10%)": f"{contact_score}/10",
    }

    return {
        "total_score": total_score,
        "skill_score": skill_score,
        "project_score": project_score,
        "education_score": education_score,
        "contact_score": contact_score,
        "breakdown": breakdown,
    }


# ---------------------------------------------------------------
# FUNCTION: get_ats_feedback
# ---------------------------------------------------------------
# Purpose:
#   Return a short feedback message based on the ATS score range.
#   This helps the student understand how strong their resume is.
#
# Parameters:
#   score (int) : total ATS score (0–100)
#
# Returns:
#   dict with "label" (str) and "color" (str for Streamlit)
# ---------------------------------------------------------------
def get_ats_feedback(score):
    if score >= 80:
        return {
            "label": "Excellent! Your resume is well-optimized for ATS.",
            "color": "green",
            "emoji": "🟢"
        }
    elif score >= 60:
        return {
            "label": "Good! Your resume passes basic ATS checks. A few improvements needed.",
            "color": "orange",
            "emoji": "🟡"
        }
    elif score >= 40:
        return {
            "label": "Average. Your resume needs significant improvements to pass ATS.",
            "color": "red",
            "emoji": "🟠"
        }
    else:
        return {
            "label": "Poor. Your resume is unlikely to pass ATS screening. Please improve it.",
            "color": "red",
            "emoji": "🔴"
        }
