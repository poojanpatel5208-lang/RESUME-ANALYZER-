# ============================================================
# resume_parser.py
# ------------------------------------------------------------
# This file handles:
#   1. Extracting raw text from a PDF resume
#   2. Detecting skills inside that text
#   3. Checking for key resume sections
# ============================================================

import pdfplumber   # Library to read PDF files
import re           # Regular expressions for pattern matching
from skills import ALL_SKILLS  # Our custom skills list


# ---------------------------------------------------------------
# FUNCTION: extract_text_from_pdf
# ---------------------------------------------------------------
# Purpose:
#   Open a PDF file and extract all text from every page.
#
# How it works:
#   pdfplumber opens the PDF, reads each page, and returns the
#   text. We join all pages into a single string.
#
# Parameters:
#   pdf_file : a file-like object (from Streamlit's file_uploader)
#
# Returns:
#   str : full text content of the resume
# ---------------------------------------------------------------
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:                   # Some pages may be empty
                    text += page_text + "\n"    # Add newline between pages
    except Exception as e:
        text = f"Error reading PDF: {e}"
    return text


# ---------------------------------------------------------------
# FUNCTION: extract_skills_from_text
# ---------------------------------------------------------------
# Purpose:
#   Scan the resume text and find which skills from ALL_SKILLS
#   are mentioned.
#
# How it works:
#   For each skill in our database, we check if that skill
#   appears in the resume text (case-insensitive search).
#   We use regex word boundaries (\b) to avoid partial matches.
#   Example: "C" should not match inside "C++" or "C#" accidentally.
#
# Parameters:
#   text (str) : raw text extracted from the resume
#
# Returns:
#   list : skills found in the resume
# ---------------------------------------------------------------
def extract_skills_from_text(text):
    found_skills = []
    text_lower = text.lower()

    for skill in ALL_SKILLS:
        # Use regex to find whole-word skill matches
        # re.escape handles special chars like "C++"
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return found_skills


# ---------------------------------------------------------------
# FUNCTION: check_resume_sections
# ---------------------------------------------------------------
# Purpose:
#   Detect whether key sections are present in the resume.
#   This is used to calculate the ATS score.
#
# Sections we check for:
#   - Projects   (important for freshers / students)
#   - Education  (degree, university info)
#   - Contact    (email, phone number)
#
# How it works:
#   We look for common keywords/headings that indicate each section.
#   Email and phone are detected using regex patterns.
#
# Parameters:
#   text (str) : raw resume text
#
# Returns:
#   dict : {section_name: True/False}
# ---------------------------------------------------------------
def check_resume_sections(text):
    text_lower = text.lower()

    sections = {}

    # Check for Projects section
    project_keywords = ["project", "projects", "personal projects", "academic projects"]
    sections["projects"] = any(kw in text_lower for kw in project_keywords)

    # Check for Education section
    education_keywords = ["education", "bachelor", "b.tech", "b.e.", "b.sc",
                          "university", "college", "degree", "engineering"]
    sections["education"] = any(kw in text_lower for kw in education_keywords)

    # Check for Contact Info using regex
    # Email pattern: something@something.something
    email_pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    # Phone pattern: 10-digit numbers or common formats
    phone_pattern = r'(\+91[\-\s]?)?[6-9]\d{9}|(\d{3}[\-\s]?\d{3}[\-\s]?\d{4})'

    has_email = bool(re.search(email_pattern, text))
    has_phone = bool(re.search(phone_pattern, text))
    sections["contact"] = has_email or has_phone

    return sections


# ---------------------------------------------------------------
# FUNCTION: extract_contact_info
# ---------------------------------------------------------------
# Purpose:
#   Pull out the candidate's email and phone number from the text.
#   Used to display basic contact details in the UI.
#
# Parameters:
#   text (str) : raw resume text
#
# Returns:
#   dict : {"email": ..., "phone": ...}
# ---------------------------------------------------------------
def extract_contact_info(text):
    contact = {"email": None, "phone": None}

    email_pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'(\+91[\-\s]?)?[6-9]\d{9}'

    email_match = re.search(email_pattern, text)
    phone_match = re.search(phone_pattern, text)

    if email_match:
        contact["email"] = email_match.group()
    if phone_match:
        contact["phone"] = phone_match.group()

    return contact
