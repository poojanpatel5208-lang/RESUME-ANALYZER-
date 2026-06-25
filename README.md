<<<<<<< HEAD
# 📄 AI Resume Analyzer — Complete Project Guide

> A beginner-friendly AI/ML project for 3rd-year Computer Engineering students applying for AI/ML internships.

---

## 📁 Project Structure

```
resume-analyzer/
│
├── app.py              ← Main Streamlit web app (UI + orchestration)
├── skills.py           ← Skills database, role requirements, matching logic
├── ats_score.py        ← ATS score calculation and feedback
├── role_match.py       ← Strengths, weaknesses, and suggestions generator
├── resume_parser.py    ← PDF text extraction and section detection
├── requirements.txt    ← All Python libraries needed
└── sample_resumes/     ← Folder to store sample PDF resumes for testing
```

---

## ⚙️ Installation Steps

### Step 1: Install Python
Make sure Python 3.9 or above is installed.
```bash
python --version
```

### Step 2: Create a Virtual Environment (Recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Step 3: Install Required Libraries
```bash
pip install -r requirements.txt
```

### Step 4: Run the App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📂 File Explanations

### 1. `app.py` — Main Application File
The entry point of the project. It:
- Sets up the Streamlit page configuration and custom CSS
- Handles the file upload widget
- Calls all other modules in sequence
- Renders the final UI (metrics, charts, pills, suggestions)

**Key functions:**
- `draw_ats_gauge(score)` — Draws a semicircular ATS score gauge using matplotlib
- `draw_skill_bar_chart(resume_skills)` — Horizontal bar chart showing skill category coverage

---

### 2. `resume_parser.py` — PDF Reader & Section Detector
Handles all text extraction from the uploaded PDF.

| Function | What it does |
|---|---|
| `extract_text_from_pdf(pdf_file)` | Opens PDF using pdfplumber and returns full text |
| `extract_skills_from_text(text)` | Scans text for known skills using regex |
| `check_resume_sections(text)` | Returns True/False for Projects, Education, Contact |
| `extract_contact_info(text)` | Returns detected email and phone number |

---

### 3. `skills.py` — Skills Database & Matching Engine
Contains the master skill list and role requirements.

| Item | Description |
|---|---|
| `ALL_SKILLS` | List of 60+ technical skills to detect |
| `ROLE_REQUIREMENTS` | Dict mapping role → required skills list |
| `get_matched_and_missing_skills()` | Returns matched & missing skills for a role |
| `calculate_match_percentage()` | Computes (matched/total) × 100 |
| `predict_best_role()` | Checks all roles, picks highest match |

---

### 4. `ats_score.py` — ATS Score Calculator
Calculates the Applicant Tracking System score.

| Function | What it does |
|---|---|
| `calculate_ats_score(match_pct, sections)` | Returns total score and component breakdown |
| `get_ats_feedback(score)` | Returns label + color based on score range |

---

### 5. `role_match.py` — Feedback Generator
Produces human-readable insights.

| Function | What it does |
|---|---|
| `generate_strengths()` | Lists positives based on found skills and sections |
| `generate_weaknesses()` | Lists gaps and missing sections |
| `generate_suggestions()` | Returns actionable tips to improve the resume |

---

## 📊 How the ATS Score Works

ATS (Applicant Tracking System) is software used by companies to filter resumes automatically before a human sees them.

Our scoring model:

```
ATS Score = Skill Match Score + Projects + Education + Contact

Where:
  Skill Match Score = 0.60 × match_percentage     (max: 60 points)
  Projects Section  = 20 if present, else 0
  Education Section = 10 if present, else 0
  Contact Info      = 10 if present, else 0

Total = max 100 points
```

**Example:**
- Skill match = 75%  → Skill Score = 0.60 × 75 = 45
- Has Projects       → +20
- Has Education      → +10
- Has Contact        → +10
- **ATS Score = 85 / 100**

---

## 🎓 Interview Questions & Answers

### 🔹 Q1. What is the purpose of this project?
**A:** This project helps students automatically analyze their resumes for AI/ML internships. It extracts skills, calculates an ATS score, identifies skill gaps, and provides personalized suggestions — all without any human recruiter involvement.

---

### 🔹 Q2. What is an ATS score?
**A:** ATS stands for Applicant Tracking System. Most companies use ATS software to filter resumes before human review. It scores resumes based on keyword matches, section completeness, and relevance to the job. A higher ATS score means higher chances of passing the initial screening.

---

### 🔹 Q3. What library did you use to extract text from the PDF?
**A:** I used `pdfplumber`, a Python library that reads text from PDF files page by page. It handles multi-page PDFs and extracts text in a clean format. The function `pdfplumber.open(file)` opens the PDF, and we loop through `pdf.pages` to get each page's text.

---

### 🔹 Q4. How did you detect skills in the resume?
**A:** I used Python's `re` (regular expressions) module. For each skill in our `ALL_SKILLS` list, I searched the resume text using `re.search(r'\b' + skill + r'\b', text.lower())`. The `\b` is a word boundary that ensures we match the exact skill word and not partial matches. For example, "C" shouldn't match inside "C++" accidentally.

---

### 🔹 Q5. What formula did you use for the Skill Match Percentage?
**A:**
```
Match % = (Number of matched skills / Total required skills for the role) × 100
```
For example, if AI/ML Intern requires 11 skills and the resume has 7 of them:
Match % = (7 / 11) × 100 = 63.6%

---

### 🔹 Q6. How does the role prediction work?
**A:** The `predict_best_role()` function in `skills.py` loops through all 4 roles and calculates the skill match percentage for each. The role with the highest match percentage is predicted as the most suitable role.

---

### 🔹 Q7. Why did you use Streamlit instead of Flask or React?
**A:** Streamlit is the best choice for AI/ML projects because:
1. It's pure Python — no HTML/CSS/JS needed
2. You can build interactive UIs with just a few lines
3. It's industry-standard for ML demos and dashboards
4. File upload, charts, and metrics are built-in components

---

### 🔹 Q8. What is `pdfplumber` and why did you use it over PyPDF2?
**A:** `pdfplumber` is more accurate than `PyPDF2` for text extraction. It handles multi-column layouts, tables, and special characters better. It's built on top of `pdfminer` and is widely used in data extraction projects.

---

### 🔹 Q9. What does `re.escape()` do in your code?
**A:** `re.escape()` escapes special characters in a string so they're treated as literal characters in a regex pattern. For example, "C++" contains "+" which is a special regex character. Without `re.escape()`, the pattern would break. With it, "C\+\+" is searched as a literal string.

---

### 🔹 Q10. How would you improve this project further?
**A:** Several improvements are possible:
1. **Use NLP (spaCy/BERT)** for smarter, context-aware skill extraction instead of simple keyword matching
2. **Add a job description input** so users can paste a JD and compare against their resume
3. **Use a real ML model** (e.g., TF-IDF + cosine similarity) to compute semantic similarity between resume and JD
4. **Store results in a database** for tracking progress over multiple resume versions
5. **Add grammar/spelling checks** using language tool APIs
6. **Deploy to cloud** (Streamlit Community Cloud or Heroku) so others can use it

---

### 🔹 Q11. What is TF-IDF and could it be used here?
**A:** TF-IDF (Term Frequency–Inverse Document Frequency) is a text vectorization technique from scikit-learn. It converts text into numerical vectors based on word importance. In this project, we could use TF-IDF to compute similarity between a resume and a job description instead of simple keyword matching. `from sklearn.feature_extraction.text import TfidfVectorizer` and `cosine_similarity` would be the tools to use.

---

### 🔹 Q12. What is the difference between matched_skills and resume_skills?
**A:**
- `resume_skills` = ALL skills detected anywhere in the resume (e.g., Python, HTML, SQL, etc.)
- `matched_skills` = Only the skills that are BOTH in the resume AND required by the selected role

A resume might have 20 skills, but if you're applying for AI/ML Intern and 7 of those match the AI/ML requirements, then matched_skills = 7.

---

### 🔹 Q13. What are word boundaries in regex (`\b`)?
**A:** `\b` in a regex pattern means "match at the boundary between a word character and a non-word character." It ensures we match complete words only. Example: pattern `\bC\b` matches "C" in "C programming" but NOT in "C++" or "Cisco". This prevents false positives in skill detection.

---

### 🔹 Q14. How do you handle a scanned PDF (image-based PDF)?
**A:** `pdfplumber` only works with text-based PDFs. For scanned PDFs, we would need OCR (Optical Character Recognition). The tool for that is `pytesseract` (Python wrapper for Google's Tesseract OCR engine). We'd convert each PDF page to an image using `pdf2image`, then extract text from the image using `pytesseract.image_to_string()`. This is a good future enhancement.

---

### 🔹 Q15. Can you explain the project architecture/flow?
**A:** The flow is:
```
User uploads PDF
     ↓
resume_parser.py → extract_text_from_pdf() → Raw text string
     ↓
resume_parser.py → extract_skills_from_text() → List of skills
     ↓
skills.py → get_matched_and_missing_skills() → Matched + Missing
     ↓
ats_score.py → calculate_ats_score() → Score out of 100
     ↓
role_match.py → generate_suggestions() → Improvement tips
     ↓
app.py → Render everything in Streamlit UI
```

This is a modular architecture where each file has a single responsibility (Single Responsibility Principle in software design).

---

## 🚀 Future Enhancements (Good for interviews)

| Enhancement | Technology |
|---|---|
| Semantic skill matching | spaCy, BERT embeddings |
| Job Description comparison | TF-IDF + Cosine Similarity |
| OCR for scanned PDFs | pytesseract + pdf2image |
| Cloud deployment | Streamlit Community Cloud |
| Resume version history | SQLite database |
| Grammar checker | LanguageTool API |
| Cover letter generator | OpenAI / Gemini API |

---

*Made for 3rd-year Computer Engineering students aiming for AI/ML internships.*
=======
# RESUME-ANALYZER-
AI-powered Resume Analyzer using Python and Streamlit
