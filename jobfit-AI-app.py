import streamlit as st
from modules.resume_parser import extract_text_from_pdf
from modules.skills import extract_skills
from modules.matcher import (
    load_jobs,
    calculate_match,
    get_missing_skills
)
from modules.recommender import generate_suggestions
from modules.gemini import get_ai_suggestions
from modules.jd_matcher import compare_resume_with_jd
from modules.ats_score import (calculate_ats_score, resume_strength)


# ----------------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="JobFit AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------------------------------
# GLOBAL STYLE / BACKGROUND
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* ---------- Background image with dark overlay for readability ---------- */
    .stApp {
        background:
            linear-gradient(rgba(10, 14, 28, 0.82), rgba(10, 14, 28, 0.88)),
            url("https://images.unsplash.com/photo-1521791136064-7986c2920216?auto=format&fit=crop&w=1920&q=80");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* ---------- Typography ---------- */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', 'Inter', sans-serif;
        color: #EAF0FF;
    }

    /* ---------- Hero header ---------- */
    .hero-box {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 18px;
        padding: 2.2rem 2rem;
        margin-bottom: 1.8rem;
        text-align: center;
        backdrop-filter: blur(6px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    }
    .hero-title {
        font-size: 2.6rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
        background: linear-gradient(90deg, #7F5AF0, #2CB67D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #C8D0E0;
    }

    /* ---------- Glass cards ---------- */
    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 1.5rem 1.6rem;
        margin-bottom: 1.2rem;
        backdrop-filter: blur(8px);
        box-shadow: 0 6px 24px rgba(0, 0, 0, 0.3);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .glass-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45);
    }

    .job-title {
        font-size: 1.35rem;
        font-weight: 700;
        color: #FFFFFF;
        margin-bottom: 0.2rem;
    }

    .score-pill {
        display: inline-block;
        padding: 0.25rem 0.9rem;
        border-radius: 999px;
        font-weight: 700;
        font-size: 0.95rem;
        color: #0A0E1C;
        background: linear-gradient(90deg, #2CB67D, #7F5AF0);
    }

    .best-match-banner {
        background: linear-gradient(120deg, rgba(127, 90, 240, 0.25), rgba(44, 182, 125, 0.25));
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 18px;
        padding: 1.8rem;
        text-align: center;
        margin: 1.5rem 0;
        backdrop-filter: blur(8px);
    }

    /* ---------- Section headers ---------- */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        margin-top: 1.4rem;
        margin-bottom: 0.8rem;
        border-left: 5px solid #7F5AF0;
        padding-left: 0.7rem;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: rgba(10, 14, 28, 0.85);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* ---------- Misc widget tweaks ---------- */
    .stProgress > div > div > div {
        background-image: linear-gradient(90deg, #7F5AF0, #2CB67D);
    }
    div[data-testid="stMetricValue"] {
        color: #2CB67D;
    }
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------------------------------------
# HERO HEADER
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">🤖 JobFit AI</div>
        <div class="hero-subtitle">AI-Powered Resume & Job Matching Assistant — Upload your resume and discover the best matching jobs instantly.</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------------------------------------------------------
# SIDEBAR — RESUME UPLOAD
# ----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 📄 Upload Resume")
    st.caption("PDF format only")
    uploaded_file = st.file_uploader(
        "Drop your resume here",
        type=["pdf"],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown(
        """
        **How it works**
        1. Upload your resume (PDF)
        2. We extract your skills
        3. We match you to the best jobs
        4. Get AI-powered improvement tips
        """
    )

# ----------------------------------------------------------------------------
# MAIN FLOW
# ----------------------------------------------------------------------------
if uploaded_file is not None:

    st.success(f"✅ **{uploaded_file.name}** uploaded successfully!")

    # Extract Resume Text
    resume_text = extract_text_from_pdf(uploaded_file)

    with st.expander("📄 View Extracted Resume Text", expanded=False):
        st.text_area("Resume Content", value=resume_text, height=280, label_visibility="collapsed")

    # Extract Skills
    skills = extract_skills(resume_text)

    st.markdown('<div class="section-header">🛠 Extracted Skills</div>', unsafe_allow_html=True)
    skill_badges = " ".join(
        [f"<span class='score-pill' style='margin:3px;'>{s}</span>" for s in skills]
    )
    st.markdown(f"<div>{skill_badges}</div>", unsafe_allow_html=True)
    # --------------------------------------------------------
# Resume vs Job Description
# --------------------------------------------------------
# --------------------------------------------------------
# Job Description
# --------------------------------------------------------

st.markdown(
    '<div class="section-header">📋 Job Description</div>',
    unsafe_allow_html=True
)

job_description = st.text_area(
    "Paste Job Description",
    height=250,
    placeholder="Paste LinkedIn / Naukri / Indeed Job Description here..."
)


if job_description:

    st.markdown(
        '<div class="section-header">🎯 Resume vs Job Description Match</div>',
        unsafe_allow_html=True
    )

    jd_score, jd_matched, jd_missing = compare_resume_with_jd(
        resume_text,
        job_description
    )

    st.metric(
        "Resume Match Score",
        f"{jd_score}%"
    )

    st.progress(jd_score / 100)

    col1, col2 = st.columns(2)

    with col1:

        st.success("✅ Matched Keywords")

        if jd_matched:
            st.write(", ".join(jd_matched))
        else:
            st.write("No keywords matched.")

    with col2:

        st.error("❌ Missing Keywords")

        if jd_missing:
            st.write(", ".join(jd_missing))
        else:
            st.write("No missing keywords.")
# --------------------------------------------------------
# ATS SCORE
# --------------------------------------------------------

if job_description:

    ats_score = calculate_ats_score(
        resume_text,
        job_description
    )

    strength = resume_strength(ats_score)

    st.markdown(
        '<div class="section-header">📊 ATS Score</div>',
        unsafe_allow_html=True
    )
    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "ATS Score",
            f"{ats_score}%"
        )

    with c2:
        st.metric(
            "Resume Strength",
            strength
        )

    # Load Jobs
    jobs = load_jobs()

    st.markdown('<div class="section-header">📋 Available Jobs</div>', unsafe_allow_html=True)
    st.dataframe(jobs, use_container_width=True)

    # Variables for Best Match
    best_score = 0
    best_job = ""
    best_matched_skills = []
    best_missing_skills = []

    st.markdown('<div class="section-header">🎯 Job Match Results</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    columns = [col1, col2]

    for index, row in jobs.iterrows():

        score, matched = calculate_match(skills, row["Skills"])
        missing = get_missing_skills(skills, row["Skills"])

        if score > best_score:
            best_score = score
            best_job = row["Job Title"]
            best_matched_skills = matched
            best_missing_skills = missing

        target_col = columns[index % 2]
        with target_col:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"<div class='job-title'>💼 {row['Job Title']}</div>", unsafe_allow_html=True)
            st.markdown(f"<span class='score-pill'>{score}% Match</span>", unsafe_allow_html=True)
            st.progress(score / 100)

            st.write("✅ **Matched Skills:**", ", ".join(matched) if matched else "—")

            if missing:
                st.warning("❌ Missing: " + ", ".join(missing))
            else:
                st.success("🎉 You have all the required skills!")
            st.markdown('</div>', unsafe_allow_html=True)

    # Best Matching Job
    st.markdown(
        f"""
        <div class="best-match-banner">
            <h2>🏆 Best Matching Job</h2>
            <h1 style="margin:0;">{best_job}</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    m1, m2, m3 = st.columns(3)
    m1.metric("Best Match Score", f"{best_score}%")
    m2.metric("Matched Skills", len(best_matched_skills))
    m3.metric("Missing Skills", len(best_missing_skills))

    bc1, bc2 = st.columns(2)
    with bc1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### ✅ Matched Skills")
        st.write(", ".join(best_matched_skills) if best_matched_skills else "—")
        st.markdown('</div>', unsafe_allow_html=True)
    with bc2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### ❌ Missing Skills")
        if best_missing_skills:
            st.write(", ".join(best_missing_skills))
        else:
            st.success("No missing skills 🎉")
        st.markdown('</div>', unsafe_allow_html=True)

    # AI Resume Suggestions
    st.markdown('<div class="section-header">🤖 AI Resume Suggestions</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    suggestions = generate_suggestions(best_missing_skills)
    for suggestion in suggestions:
        st.write("✅", suggestion)
    st.markdown('</div>', unsafe_allow_html=True)

    # AI Career Advisor
    st.markdown('<div class="section-header">🤖 AI Career Advisor</div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    with st.spinner("Analyzing Resume..."):
        advice = get_ai_suggestions(resume_text)
    st.write(advice)
    st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown(
        """
        <div class="glass-card" style="text-align:center; padding: 3rem;">
            <h2>👋 Get Started</h2>
            <p>Upload your resume from the sidebar to discover your best-matching jobs, AI career advice, and live openings.</p>
        </div>
        """,
        unsafe_allow_html=True
    )