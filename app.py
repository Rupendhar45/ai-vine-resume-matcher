import streamlit as st
import fitz
import re

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI VINE Resume Matcher",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# PREMIUM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main page */
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(16,185,129,0.10), transparent 25%),
            radial-gradient(circle at 90% 10%, rgba(37,99,235,0.10), transparent 25%),
            #f8fafc;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */
    .brand {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 35px;
        padding: 8px 0;
    }

    .brand-icon {
        width: 64px;
        height: 64px;
        min-width: 64px;
        border-radius: 18px;
        background: linear-gradient(135deg, #10b981, #2563eb);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 34px;
        box-shadow: 0 12px 30px rgba(37,99,235,0.18);
    }

    .brand-title {
        font-size: 34px;
        font-weight: 800;
        color: #172033;
        line-height: 1.1;
    }

    .brand-subtitle {
        color: #64748b;
        font-size: 15px;
        margin-top: 5px;
    }

    /* Hero */
    .hero {
        background: rgba(255,255,255,0.82);
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        padding: 38px 30px;
        text-align: center;
        margin-bottom: 28px;
        box-shadow: 0 15px 45px rgba(15,23,42,0.06);
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 14px;
        border-radius: 999px;
        background: #ecfdf5;
        color: #047857;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 14px;
    }

    .hero h1 {
        color: #172033;
        font-size: 42px;
        margin: 0;
        font-weight: 800;
    }

    .hero h1 span {
        color: #2563eb;
    }

    .hero p {
        color: #64748b;
        font-size: 17px;
        margin-top: 14px;
        line-height: 1.6;
    }

    /* Upload cards */
    .upload-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 22px;
        min-height: 170px;
        box-shadow: 0 10px 30px rgba(15,23,42,0.05);
        margin-bottom: 10px;
    }

    .upload-title {
        font-size: 19px;
        font-weight: 750;
        color: #172033;
        margin-bottom: 8px;
    }

    .upload-description {
        color: #64748b;
        font-size: 14px;
        margin-bottom: 16px;
    }

    /* Result cards */
    .result-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(15,23,42,0.05);
    }

    .section-title {
        font-size: 24px;
        font-weight: 800;
        color: #172033;
        margin: 28px 0 16px 0;
    }

    .skill-chip {
        display: inline-block;
        padding: 7px 12px;
        margin: 4px;
        border-radius: 999px;
        background: #ecfdf5;
        color: #047857;
        font-size: 13px;
        font-weight: 650;
        border: 1px solid #bbf7d0;
    }

    .missing-chip {
        display: inline-block;
        padding: 7px 12px;
        margin: 4px;
        border-radius: 999px;
        background: #fff7ed;
        color: #c2410c;
        font-size: 13px;
        font-weight: 650;
        border: 1px solid #fed7aa;
    }

    .footer {
        text-align: center;
        color: #94a3b8;
        margin-top: 50px;
        font-size: 13px;
    }

    /* Hide Streamlit menu/footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="brand">
        <div class="brand-icon">🌱</div>
        <div>
            <div class="brand-title">AI VINE</div>
            <div class="brand-subtitle">AI Talent Intelligence</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# HERO
# =========================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-badge">AI-POWERED RESUME INTELLIGENCE</div>
        <h1>Match Your Resume <span>With Any Job.</span></h1>
        <p>
            Upload your resume and job description.
            AI VINE instantly identifies your skill match,
            missing skills and improvement areas.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SKILL DATABASE
# =========================================================

SKILLS = {
    # Programming
    "python": ["python"],
    "java": ["java"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "c": ["c programming"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "c sharp"],
    "go": ["golang"],
    "rust": ["rust"],
    "php": ["php"],
    "ruby": ["ruby"],
    "kotlin": ["kotlin"],
    "swift": ["swift"],

    # Backend
    "spring boot": ["spring boot", "springboot"],
    "spring": ["spring framework", "spring"],
    "spring security": ["spring security"],
    "spring cloud": ["spring cloud"],
    "microservices": ["microservices", "microservice"],
    "hibernate": ["hibernate"],
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    ".net": [".net", "dotnet"],
    "asp.net": ["asp.net", "asp net"],
    "node.js": ["node.js", "nodejs", "node js"],
    "express.js": ["express.js", "expressjs"],
    "rest api": ["rest api", "restful api", "restful apis"],
    "graphql": ["graphql"],

    # Frontend
    "html": ["html", "html5"],
    "css": ["css", "css3"],
    "react": ["react", "react.js", "reactjs"],
    "angular": ["angular"],
    "vue": ["vue", "vue.js"],
    "bootstrap": ["bootstrap"],
    "tailwind": ["tailwind", "tailwind css"],

    # Databases
    "mysql": ["mysql"],
    "postgresql": ["postgresql", "postgres"],
    "mongodb": ["mongodb", "mongo db"],
    "oracle": ["oracle database", "oracle db"],
    "sql": ["sql"],
    "nosql": ["nosql"],
    "redis": ["redis"],

    # Cloud
    "aws": ["aws", "amazon web services"],
    "azure": ["azure", "microsoft azure"],
    "google cloud": ["google cloud", "gcp", "google cloud platform"],

    # DevOps
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "jenkins": ["jenkins"],
    "ci/cd": ["ci/cd", "cicd", "continuous integration", "continuous delivery"],
    "terraform": ["terraform"],
    "ansible": ["ansible"],
    "devops": ["devops"],

    # Messaging
    "kafka": ["kafka", "apache kafka"],
    "rabbitmq": ["rabbitmq"],

    # Testing
    "selenium": ["selenium"],
    "appium": ["appium"],
    "postman": ["postman"],
    "junit": ["junit"],
    "pytest": ["pytest"],
    "unit testing": ["unit testing", "unit tests"],
    "integration testing": ["integration testing"],

    # AI / ML
    "machine learning": ["machine learning", "machine-learning"],
    "deep learning": ["deep learning"],
    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],
    "nlp": ["nlp", "natural language processing"],
    "generative ai": ["generative ai", "genai"],
    "llm": ["llm", "large language model", "large language models"],
    "langchain": ["langchain"],
    "ollama": ["ollama"],

    # Data
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "power bi": ["power bi"],
    "tableau": ["tableau"],
    "spark": ["apache spark", "spark"],

    # Tools
    "git": ["git"],
    "github": ["github"],
    "gitlab": ["gitlab"],
    "jira": ["jira"],
    "linux": ["linux"],
    "windows": ["windows"],

    # Architecture
    "distributed systems": ["distributed systems"],
    "system design": ["system design"],
    "event driven architecture": [
        "event-driven architecture",
        "event driven architecture"
    ],
    "cloud native": ["cloud-native", "cloud native"],

    # Business / General
    "problem solving": ["problem solving", "problem-solving"],
    "communication": ["communication skills"],
    "leadership": ["leadership"],
    "stakeholder management": ["stakeholder management"],
}

# =========================================================
# TEXT EXTRACTION
# =========================================================

def extract_pdf_text(uploaded_file):
    text = ""

    try:
        uploaded_file.seek(0)

        pdf_bytes = uploaded_file.read()

        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text("text") + "\n"

    except Exception as e:
        st.error(f"Could not read PDF: {e}")

    return text


def extract_file_text(uploaded_file):

    if uploaded_file is None:
        return ""

    if uploaded_file.type == "application/pdf":
        return extract_pdf_text(uploaded_file)

    try:
        uploaded_file.seek(0)
        return uploaded_file.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""


# =========================================================
# TEXT NORMALIZATION
# =========================================================

def normalize_text(text):

    text = text.lower()

    # Preserve technical symbols
    text = text.replace("–", "-")
    text = text.replace("—", "-")

    # Multiple spaces
    text = re.sub(r"\s+", " ", text)

    return text


# =========================================================
# FIND SKILLS
# =========================================================

def find_skills(text):

    normalized = normalize_text(text)

    found = []

    for skill, aliases in SKILLS.items():

        for alias in aliases:

            alias_normalized = alias.lower()

            # Special handling for short terms
            if len(alias_normalized) <= 2:
                pattern = r"(?<![a-z0-9])" + re.escape(alias_normalized) + r"(?![a-z0-9])"
            else:
                pattern = re.escape(alias_normalized)

            if re.search(pattern, normalized):

                found.append(skill)
                break

    return sorted(set(found))


# =========================================================
# MATCH SKILLS
# =========================================================

def calculate_match(resume_skills, job_skills):

    if not job_skills:
        return 0, [], []

    matched = [
        skill for skill in job_skills
        if skill in resume_skills
    ]

    missing = [
        skill for skill in job_skills
        if skill not in resume_skills
    ]

    score = round((len(matched) / len(job_skills)) * 100)

    return score, matched, missing


# =========================================================
# GENERAL RECOMMENDATIONS
# =========================================================

def generate_recommendations(score, matched, missing):

    recommendations = []

    if score >= 80:
        recommendations.append(
            "Your resume has a strong skill alignment with this job."
        )

    elif score >= 60:
        recommendations.append(
            "Your resume has a moderate-to-strong skill alignment. "
            "Highlight the matched skills more clearly."
        )

    elif score >= 40:
        recommendations.append(
            "Your resume has a partial skill match. "
            "Review the missing requirements before applying."
        )

    else:
        recommendations.append(
            "This job has a low skill match with the current resume."
        )

    if missing:
        top_missing = missing[:5]

        recommendations.append(
            "Priority skills to consider adding only if you genuinely "
            "have experience with: "
            + ", ".join(top_missing)
            + "."
        )

    if matched:
        recommendations.append(
            "Make sure your strongest matched skills appear in your "
            "Professional Summary and Skills section."
        )

    recommendations.append(
        "Do not add technologies to your resume that you have not actually used."
    )

    return recommendations


# =========================================================
# UPLOAD SECTION
# =========================================================

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """
        <div class="upload-card">
            <div class="upload-title">📄 Your Resume</div>
            <div class="upload-description">
                Upload your latest resume in PDF or TXT format.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    resume_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "txt"],
        key="resume",
        label_visibility="collapsed",
    )

with col2:

    st.markdown(
        """
        <div class="upload-card">
            <div class="upload-title">💼 Job Description</div>
            <div class="upload-description">
                Upload any job description in PDF or TXT format.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    job_file = st.file_uploader(
        "Upload Job Description",
        type=["pdf", "txt"],
        key="job",
        label_visibility="collapsed",
    )


# =========================================================
# ANALYZE BUTTON
# =========================================================

st.write("")

analyze = st.button(
    "✨ Analyze Resume Match",
    type="primary",
    use_container_width=False,
)


# =========================================================
# ANALYSIS
# =========================================================

if analyze:

    if not resume_file or not job_file:

        st.warning(
            "Please upload both your Resume and Job Description."
        )

    else:

        with st.spinner("Analyzing resume and job description..."):

            resume_text = extract_file_text(resume_file)
            job_text = extract_file_text(job_file)

            if not resume_text.strip():
                st.error(
                    "Could not extract text from the resume. "
                    "Please use a text-based PDF."
                )
                st.stop()

            if not job_text.strip():
                st.error(
                    "Could not extract text from the job description."
                )
                st.stop()

            # Find skills
            resume_skills = find_skills(resume_text)
            job_skills = find_skills(job_text)

            # Calculate
            score, matched, missing = calculate_match(
                resume_skills,
                job_skills
            )

            recommendations = generate_recommendations(
                score,
                matched,
                missing
            )

        # =================================================
        # RESULTS
        # =================================================

        st.markdown(
            '<div class="section-title">🎯 Resume Match Analysis</div>',
            unsafe_allow_html=True,
        )

        # Metrics
        m1, m2, m3, m4 = st.columns(4)

        with m1:
            st.metric(
                "Overall Match",
                f"{score}%"
            )

        with m2:
            st.metric(
                "Required Skills",
                len(job_skills)
            )

        with m3:
            st.metric(
                "Matched",
                len(matched)
            )

        with m4:
            st.metric(
                "Missing",
                len(missing)
            )

        # Progress
        st.progress(
            score / 100,
            text=f"Skill Match: {score}%"
        )

        # =================================================
        # MATCHED SKILLS
        # =================================================

        st.markdown(
            '<div class="section-title">✅ Matched Skills</div>',
            unsafe_allow_html=True,
        )

        if matched:

            matched_html = ""

            for skill in matched:
                matched_html += (
                    f'<span class="skill-chip">{skill}</span>'
                )

            st.markdown(
                matched_html,
                unsafe_allow_html=True
            )

        else:

            st.info(
                "No matching skills were detected."
            )

        # =================================================
        # MISSING SKILLS
        # =================================================

        st.markdown(
            '<div class="section-title">⚠️ Missing Skills</div>',
            unsafe_allow_html=True,
        )

        if missing:

            missing_html = ""

            for skill in missing:
                missing_html += (
                    f'<span class="missing-chip">{skill}</span>'
                )

            st.markdown(
                missing_html,
                unsafe_allow_html=True
            )

        else:

            st.success(
                "Excellent! All detected job skills are present in the resume."
            )

        # =================================================
        # RECOMMENDATIONS
        # =================================================

        st.markdown(
            '<div class="section-title">💡 Recommendations</div>',
            unsafe_allow_html=True,
        )

        for recommendation in recommendations:

            st.info(recommendation)

        # =================================================
        # JOB SKILLS
        # =================================================

        with st.expander("🔎 View Skills Detected From Job Description"):

            if job_skills:
                st.write(", ".join(job_skills))
            else:
                st.write(
                    "No skills from the current skill library were detected."
                )

        # =================================================
        # RESUME SKILLS
        # =================================================

        with st.expander("📄 View Skills Detected From Resume"):

            if resume_skills:
                st.write(", ".join(resume_skills))
            else:
                st.write(
                    "No skills from the current skill library were detected."
                )

        # =================================================
        # REPORT
        # =================================================

        report = f"""
AI VINE - RESUME MATCH REPORT

Overall Match: {score}%

Required Skills: {len(job_skills)}
Matched Skills: {len(matched)}
Missing Skills: {len(missing)}

MATCHED SKILLS
-------------
{", ".join(matched) if matched else "None"}

MISSING SKILLS
--------------
{", ".join(missing) if missing else "None"}

RECOMMENDATIONS
---------------
{" ".join(recommendations)}

IMPORTANT
---------
Only add skills to your resume that you genuinely have experience with.
"""

        st.download_button(
            "⬇️ Download Match Report",
            data=report,
            file_name="AI_VINE_resume_match_report.txt",
            mime="text/plain",
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        AI VINE · AI Talent Intelligence · Resume Match Engine
    </div>
    """,
    unsafe_allow_html=True,
)