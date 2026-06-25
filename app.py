# ============================================================
# app.py
# ------------------------------------------------------------
# This is the MAIN FILE of the Resume Analyzer project.
# It builds the Streamlit web interface and ties together
# all modules (resume_parser, skills, ats_score, role_match).
#
# HOW TO RUN:
#   streamlit run app.py
# ============================================================

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# Import our custom modules
from resume_parser import extract_text_from_pdf, extract_skills_from_text, check_resume_sections, extract_contact_info
from skills import get_matched_and_missing_skills, calculate_match_percentage, predict_best_role
from ats_score import calculate_ats_score, get_ats_feedback
from role_match import generate_strengths, generate_weaknesses, generate_suggestions


# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS STYLING
# ============================================================
st.markdown("""
<style>
    /* Main background */
    .main { background-color: #0f1117; }

    /* Score card style */
    .score-card {
        background: linear-gradient(135deg, #1a1f2e, #252b3b);
        border: 1px solid #3a4060;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
    }

    /* Skill pill badges */
    .skill-pill {
        display: inline-block;
        background-color: #1e3a5f;
        color: #60a5fa;
        border: 1px solid #2563eb;
        border-radius: 20px;
        padding: 4px 14px;
        margin: 4px;
        font-size: 13px;
        font-weight: 500;
    }

    /* Missing skill pills */
    .skill-pill-missing {
        display: inline-block;
        background-color: #3b1f1f;
        color: #f87171;
        border: 1px solid #dc2626;
        border-radius: 20px;
        padding: 4px 14px;
        margin: 4px;
        font-size: 13px;
        font-weight: 500;
    }

    /* Matched skill pills */
    .skill-pill-matched {
        display: inline-block;
        background-color: #1a3320;
        color: #4ade80;
        border: 1px solid #16a34a;
        border-radius: 20px;
        padding: 4px 14px;
        margin: 4px;
        font-size: 13px;
        font-weight: 500;
    }

    /* Section headers */
    .section-header {
        font-size: 20px;
        font-weight: 700;
        color: #e2e8f0;
        border-left: 4px solid #3b82f6;
        padding-left: 12px;
        margin: 20px 0 10px 0;
    }

    /* Suggestion box */
    .suggestion-box {
        background-color: #1a1f2e;
        border-left: 3px solid #f59e0b;
        border-radius: 6px;
        padding: 10px 15px;
        margin: 6px 0;
        font-size: 14px;
        color: #d1d5db;
    }

    /* Hide Streamlit default header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTION: draw_ats_gauge
# ============================================================
# Purpose:
#   Draw a semicircular gauge chart using matplotlib to
#   visually display the ATS score.
#
# Parameters:
#   score (int) : ATS score from 0 to 100
# ============================================================
def draw_ats_gauge(score):
    fig, ax = plt.subplots(figsize=(5, 3))
    fig.patch.set_facecolor('#0f1117')
    ax.set_facecolor('#0f1117')

    # Draw the grey background arc (full semicircle)
    theta = np.linspace(np.pi, 0, 100)
    ax.plot(np.cos(theta), np.sin(theta), color='#374151', linewidth=20, solid_capstyle='round')

    # Determine color based on score
    if score >= 80:
        color = '#4ade80'   # Green
    elif score >= 60:
        color = '#facc15'   # Yellow
    elif score >= 40:
        color = '#fb923c'   # Orange
    else:
        color = '#f87171'   # Red

    # Draw the colored arc based on score
    filled = int(score)
    theta_fill = np.linspace(np.pi, np.pi - (np.pi * filled / 100), 100)
    ax.plot(np.cos(theta_fill), np.sin(theta_fill), color=color, linewidth=20, solid_capstyle='round')

    # Display score text in center
    ax.text(0, 0.1, f"{score}", fontsize=40, fontweight='bold',
            color=color, ha='center', va='center')
    ax.text(0, -0.25, "ATS Score", fontsize=12, color='#9ca3af', ha='center')
    ax.text(0, -0.5, "out of 100", fontsize=10, color='#6b7280', ha='center')

    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-0.7, 1.2)
    ax.axis('off')
    plt.tight_layout()
    return fig


# ============================================================
# HELPER FUNCTION: draw_skill_bar_chart
# ============================================================
# Purpose:
#   Create a horizontal bar chart showing skill category coverage.
#
# Parameters:
#   resume_skills (list) : skills found in the resume
# ============================================================
def draw_skill_bar_chart(resume_skills):
    # Define skill categories
    categories = {
        "AI/ML": ["Python", "Machine Learning", "Deep Learning", "TensorFlow",
                  "PyTorch", "Scikit-Learn", "Keras", "NLP", "Computer Vision"],
        "Data": ["Pandas", "NumPy", "SQL", "Power BI", "Tableau",
                 "Matplotlib", "Seaborn", "Excel"],
        "Web Dev": ["HTML", "CSS", "JavaScript", "React", "Node.js",
                    "Django", "Flask", "Bootstrap"],
        "Tools": ["Git", "GitHub", "Docker", "Linux", "AWS",
                  "VS Code", "Jupyter Notebook"],
        "Languages": ["Python", "Java", "C++", "JavaScript", "R", "SQL"],
    }

    labels = []
    values = []
    resume_set = set(resume_skills)

    for cat, skills in categories.items():
        matched = len(resume_set.intersection(set(skills)))
        total = len(skills)
        labels.append(cat)
        values.append(round((matched / total) * 100, 1))

    fig, ax = plt.subplots(figsize=(6, 3.5))
    fig.patch.set_facecolor('#1a1f2e')
    ax.set_facecolor('#1a1f2e')

    colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
    bars = ax.barh(labels, values, color=colors, height=0.5, edgecolor='none')

    # Add value labels inside bars
    for bar, val in zip(bars, values):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                f"{val}%", va='center', color='#d1d5db', fontsize=10)

    ax.set_xlim(0, 115)
    ax.set_xlabel("Coverage %", color='#9ca3af', fontsize=10)
    ax.tick_params(colors='#9ca3af', labelsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#374151')
    ax.spines['left'].set_color('#374151')
    plt.tight_layout()
    return fig


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 📄 Resume Analyzer")
    st.markdown("**For AI/ML Internship Applications**")
    st.markdown("---")
    st.markdown("### How it works:")
    st.markdown("1. Upload your PDF resume")
    st.markdown("2. Select your target role")
    st.markdown("3. Get instant analysis")
    st.markdown("---")
    st.markdown("### Scoring Formula:")
    st.markdown("- 🎯 Skill Match → **60%**")
    st.markdown("- 📁 Projects → **20%**")
    st.markdown("- 🎓 Education → **10%**")
    st.markdown("- 📞 Contact Info → **10%**")
    st.markdown("---")
    st.markdown("*Built for 3rd-year CS/CE students*")


# ============================================================
# MAIN PAGE HEADER
# ============================================================
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='color: #3b82f6; font-size: 2.5em; font-weight: 800;'>
        🤖 AI Resume Analyzer
    </h1>
    <p style='color: #9ca3af; font-size: 1.1em;'>
        Analyze your resume for AI/ML Internship Applications
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


# ============================================================
# SECTION 1: UPLOAD + ROLE SELECTION
# ============================================================
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="section-header">📤 Upload Your Resume</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Upload a PDF resume",
        type=["pdf"],
        help="Only PDF files are supported."
    )

with col2:
    st.markdown('<div class="section-header">🎯 Select Target Role</div>', unsafe_allow_html=True)
    role = st.selectbox(
        "Choose the role you're applying for:",
        options=[
            "AI/ML Intern",
            "Data Analyst Intern",
            "Python Developer Intern",
            "Web Developer Intern",
        ]
    )


# ============================================================
# MAIN ANALYSIS — Runs only after upload
# ============================================================
if uploaded_file is not None:

    # ---- Step 1: Extract text from PDF ----
    with st.spinner("🔍 Reading your resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)

    if not resume_text or resume_text.startswith("Error"):
        st.error("❌ Could not read the PDF. Please ensure it's a text-based PDF (not scanned image).")
    else:

        # ---- Step 2: Extract skills & sections ----
        resume_skills   = extract_skills_from_text(resume_text)
        sections        = check_resume_sections(resume_text)
        contact_info    = extract_contact_info(resume_text)

        # ---- Step 3: Skill matching ----
        matched_skills, missing_skills = get_matched_and_missing_skills(resume_skills, role)
        match_pct = calculate_match_percentage(matched_skills, role)

        # ---- Step 4: ATS Score ----
        ats_result = calculate_ats_score(match_pct, sections)
        ats_feedback = get_ats_feedback(ats_result["total_score"])

        # ---- Step 5: Strengths, Weaknesses, Suggestions ----
        strengths   = generate_strengths(resume_skills, matched_skills, sections)
        weaknesses  = generate_weaknesses(missing_skills, sections, match_pct)
        suggestions = generate_suggestions(missing_skills, sections, role, match_pct)

        # ---- Step 6: Best role prediction ----
        best_role, best_score = predict_best_role(resume_skills)

        st.success("✅ Resume analyzed successfully!")
        st.markdown("---")

        # ============================================================
        # SECTION 2: TOP METRICS ROW
        # ============================================================
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("🧠 Skills Found",    len(resume_skills))
        m2.metric("✅ Skills Matched",  len(matched_skills))
        m3.metric("❌ Skills Missing",  len(missing_skills))
        m4.metric("📊 Match %",         f"{match_pct}%")

        st.markdown("---")

        # ============================================================
        # SECTION 3: ATS SCORE + BREAKDOWN
        # ============================================================
        st.markdown('<div class="section-header">📊 ATS Score</div>', unsafe_allow_html=True)
        col_gauge, col_breakdown = st.columns([1, 1.5])

        with col_gauge:
            gauge_fig = draw_ats_gauge(ats_result["total_score"])
            st.pyplot(gauge_fig, use_container_width=True)
            st.markdown(
                f"<div style='text-align:center; color:#9ca3af; font-size:14px;'>"
                f"{ats_feedback['emoji']} {ats_feedback['label']}</div>",
                unsafe_allow_html=True
            )

        with col_breakdown:
            st.markdown("#### Score Breakdown")
            for component, score_str in ats_result["breakdown"].items():
                pts, total = score_str.split("/")
                progress_val = int(pts) / int(total)
                st.write(f"**{component}** — `{score_str}`")
                st.progress(progress_val)

        st.markdown("---")

        # ============================================================
        # SECTION 4: EXTRACTED SKILLS + SKILL CHART
        # ============================================================
        st.markdown('<div class="section-header">🧩 Extracted Skills</div>', unsafe_allow_html=True)
        col_skills, col_chart = st.columns([1, 1.2])

        with col_skills:
            if resume_skills:
                pills_html = "".join([
                    f'<span class="skill-pill">{s}</span>'
                    for s in resume_skills
                ])
                st.markdown(pills_html, unsafe_allow_html=True)
            else:
                st.warning("No skills detected. Make sure your resume mentions technical skills clearly.")

        with col_chart:
            if resume_skills:
                bar_fig = draw_skill_bar_chart(resume_skills)
                st.pyplot(bar_fig, use_container_width=True)

        st.markdown("---")

        # ============================================================
        # SECTION 5: SKILL MATCH ANALYSIS
        # ============================================================
        st.markdown('<div class="section-header">🎯 Skill Match Analysis</div>', unsafe_allow_html=True)
        st.write(f"**Role:** {role} | **Match:** {match_pct}%")

        c_match, c_missing = st.columns(2)

        with c_match:
            st.markdown("##### ✅ Matched Skills")
            if matched_skills:
                pills_html = "".join([
                    f'<span class="skill-pill-matched">{s}</span>'
                    for s in matched_skills
                ])
                st.markdown(pills_html, unsafe_allow_html=True)
            else:
                st.info("No matching skills found.")

        with c_missing:
            st.markdown("##### ❌ Missing Skills")
            if missing_skills:
                pills_html = "".join([
                    f'<span class="skill-pill-missing">{s}</span>'
                    for s in missing_skills
                ])
                st.markdown(pills_html, unsafe_allow_html=True)
            else:
                st.success("🎉 You have all the required skills!")

        st.markdown("---")

        # ============================================================
        # SECTION 6: STRENGTHS & WEAKNESSES
        # ============================================================
        st.markdown('<div class="section-header">💪 Resume Strengths & Weaknesses</div>', unsafe_allow_html=True)
        col_str, col_weak = st.columns(2)

        with col_str:
            st.markdown("##### 💚 Strengths")
            for s in strengths:
                st.markdown(f"✅ {s}")

        with col_weak:
            st.markdown("##### 🔴 Weaknesses")
            for w in weaknesses:
                st.markdown(f"⚠️ {w}")

        st.markdown("---")

        # ============================================================
        # SECTION 7: SUGGESTIONS
        # ============================================================
        st.markdown('<div class="section-header">💡 Suggestions for Improvement</div>', unsafe_allow_html=True)
        for i, suggestion in enumerate(suggestions, 1):
            st.markdown(
                f'<div class="suggestion-box"><b>#{i}</b> {suggestion}</div>',
                unsafe_allow_html=True
            )

        st.markdown("---")

        # ============================================================
        # SECTION 8: SUITABLE ROLE PREDICTION
        # ============================================================
        st.markdown('<div class="section-header">🏆 Suitable Role Prediction</div>', unsafe_allow_html=True)

        col_pred, col_contact = st.columns(2)

        with col_pred:
            st.markdown(f"""
            <div class="score-card">
                <div style='font-size:40px;'>🎯</div>
                <div style='color:#4ade80; font-size:22px; font-weight:700; margin:10px 0;'>
                    {best_role}
                </div>
                <div style='color:#9ca3af; font-size:14px;'>
                    Best match based on your skills
                </div>
                <div style='color:#facc15; font-size:16px; margin-top:10px;'>
                    Match Score: {best_score}%
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_contact:
            st.markdown("#### 📋 Detected Contact Info")
            if contact_info["email"]:
                st.markdown(f"📧 **Email:** {contact_info['email']}")
            else:
                st.markdown("📧 **Email:** Not found")

            if contact_info["phone"]:
                st.markdown(f"📱 **Phone:** {contact_info['phone']}")
            else:
                st.markdown("📱 **Phone:** Not found")

            st.markdown("#### 📂 Resume Sections Detected")
            st.write(f"{'✅' if sections.get('projects') else '❌'} Projects Section")
            st.write(f"{'✅' if sections.get('education') else '❌'} Education Section")
            st.write(f"{'✅' if sections.get('contact') else '❌'} Contact Information")

        st.markdown("---")

        # ============================================================
        # SECTION 9: RAW TEXT (Expandable — for debugging)
        # ============================================================
        with st.expander("🔎 View Extracted Resume Text (for debugging)"):
            st.text_area("Raw Text", resume_text, height=300)

else:
    # Show placeholder when no file is uploaded
    st.markdown("""
    <div style='text-align:center; padding: 60px; color: #4b5563;'>
        <div style='font-size: 64px;'>📄</div>
        <h3 style='color:#6b7280;'>Upload your resume PDF to get started</h3>
        <p>The analyzer will extract skills, calculate ATS score, and give you personalized suggestions.</p>
    </div>
    """, unsafe_allow_html=True)
