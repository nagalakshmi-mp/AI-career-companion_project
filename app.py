import os

import streamlit as st

from src.resume_parser import extract_resume_text
from src.llm_extractor import extract_candidate_information
from src.database import (
    initialize_database,
    save_student_profile,
    add_application,
    get_all_applications,
    get_application_by_id,
    update_application,
    delete_application,
    search_applications,
    get_upcoming_deadlines,
    get_scheduled_interviews,
    get_application_statistics
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Career Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "candidate_profile" not in st.session_state:
    st.session_state.candidate_profile = None

if "profile_id" not in st.session_state:
    st.session_state.profile_id = None

if "ranked_jobs" not in st.session_state:
    st.session_state.ranked_jobs = []


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        margin-bottom: 30px;
    }

    .feature-card {
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        margin-bottom: 15px;
        min-height: 150px;
    }

    .profile-card {
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("🎓 AI Career Companion")

st.sidebar.write(
    "Your intelligent internship and career assistant"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "📄 My Resume",
        "🔎 Find Jobs",
        "📊 Skill Gap",
        "✍️ Resume Assistant",
        "💌 Cover Letter",
        "🎤 Interview Prep",
        "💬 Career Assistant",
        "📋 Application Tracker"
    ]
)

st.sidebar.divider()

st.sidebar.caption(
    "AI Career Companion"
)

st.sidebar.caption(
    "Internship & Career Support System"
)


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">🎓 AI Career Companion</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        "Your personal AI-powered internship and career assistant"
        "</div>",
        unsafe_allow_html=True
    )

    st.divider()

    st.subheader("Welcome! 👋")

    st.write(
        """
        This platform helps students discover suitable internships,
        understand their skill gaps, improve their resumes, prepare
        for interviews, and receive personalized career guidance.
        """
    )

    st.divider()

    st.subheader("🚀 Career Tools")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">
            <h3>📄 Resume</h3>
            <p>
            Upload your resume and automatically create
            your candidate profile.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Open Resume",
            key="dashboard_resume"
        ):
            st.info(
                "Select '📄 My Resume' from the sidebar."
            )

    with col2:

        st.markdown(
            """
            <div class="feature-card">
            <h3>🔎 Job Matching</h3>
            <p>
            Find internships and jobs that match
            your skills and qualifications.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Find Jobs",
            key="dashboard_jobs"
        ):
            st.info(
                "Select '🔎 Find Jobs' from the sidebar."
            )

    with col3:

        st.markdown(
            """
            <div class="feature-card">
            <h3>📊 Skill Gap</h3>
            <p>
            Identify missing skills required for
            your target internships and jobs.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "Check Skills",
            key="dashboard_skills"
        ):
            st.info(
                "The skill-gap module will be connected next."
            )

    st.write("")

    col4, col5, col6 = st.columns(3)

    with col4:

        st.markdown(
            """
            <div class="feature-card">
            <h3>✍️ Resume Assistant</h3>
            <p>
            Improve your resume content and make
            it more suitable for job applications.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col5:

        st.markdown(
            """
            <div class="feature-card">
            <h3>💌 Cover Letter</h3>
            <p>
            Generate personalized cover letters
            for internship applications.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col6:

        st.markdown(
            """
            <div class="feature-card">
            <h3>🎤 Interview Prep</h3>
            <p>
            Practice interview questions and
            prepare for your target role.
            </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    st.subheader("💡 How it works")

    step1, step2, step3, step4 = st.columns(4)

    with step1:
        st.markdown("### 1️⃣")
        st.write("Upload Resume")

    with step2:
        st.markdown("### 2️⃣")
        st.write("Build Profile")

    with step3:
        st.markdown("### 3️⃣")
        st.write("Find Opportunities")

    with step4:
        st.markdown("### 4️⃣")
        st.write("Improve & Prepare")


# ============================================================
# MY RESUME
# ============================================================

elif page == "📄 My Resume":

    st.title("📄 My Resume")

    st.write(
        "Upload your resume to create or update your candidate profile."
    )

    st.divider()

    # --------------------------------------------------------
    # STUDENT INFORMATION
    # --------------------------------------------------------

    st.subheader("👤 Student Information")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Name"
        )

    with col2:

        email = st.text_input(
            "Email"
        )

    phone = st.text_input(
        "Phone Number"
    )

    # --------------------------------------------------------
    # RESUME UPLOAD
    # --------------------------------------------------------

    st.subheader("📤 Resume Upload")

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"]
    )

    if uploaded_file is not None:

        st.success(
            f"Resume selected: {uploaded_file.name}"
        )

        if st.button(
            "🚀 Process Resume",
            type="primary"
        ):

            try:

                # ------------------------------------------------
                # CREATE UPLOADS FOLDER
                # ------------------------------------------------

                os.makedirs(
                    "uploads",
                    exist_ok=True
                )

                # ------------------------------------------------
                # SAVE RESUME
                # ------------------------------------------------

                resume_path = os.path.join(
                    "uploads",
                    uploaded_file.name
                )

                with open(
                    resume_path,
                    "wb"
                ) as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )

                st.info(
                    "Resume uploaded successfully."
                )

                # ------------------------------------------------
                # EXTRACT TEXT
                # ------------------------------------------------

                with st.spinner(
                    "📖 Reading your resume..."
                ):

                    resume_text = extract_resume_text(
                        resume_path
                    )

                if not resume_text.strip():

                    st.error(
                        "Could not extract text from the resume."
                    )

                    st.stop()

                st.success(
                    "✅ Resume text extracted successfully."
                )

                # ------------------------------------------------
                # EXTRACT CANDIDATE INFORMATION
                # ------------------------------------------------

                with st.spinner(
                    "🤖 Analyzing your resume..."
                ):

                    extracted_profile = (
                        extract_candidate_information(
                            resume_text
                        )
                    )

                # ------------------------------------------------
                # USER ENTERED INFORMATION
                # ------------------------------------------------

                if name.strip():

                    extracted_profile["name"] = name

                if email.strip():

                    extracted_profile["email"] = email

                if phone.strip():

                    extracted_profile["phone"] = phone

                # ------------------------------------------------
                # SAVE PROFILE IN SESSION STATE
                # ------------------------------------------------

                st.session_state.candidate_profile = (
                    extracted_profile
                )

                # Clear old job results because this is a new
                # profile processing operation.
                st.session_state.ranked_jobs = []

                # ------------------------------------------------
                # DISPLAY PROFILE
                # ------------------------------------------------

                st.divider()

                st.header(
                    "👤 Candidate Profile"
                )

                # ------------------------------------------------
                # BASIC INFORMATION
                # ------------------------------------------------

                st.subheader(
                    "Basic Information"
                )

                profile_col1, profile_col2, profile_col3 = st.columns(3)

                with profile_col1:

                    st.write("**Name**")

                    st.write(
                        extracted_profile.get(
                            "name",
                            ""
                        )
                    )

                with profile_col2:

                    st.write("**Email**")

                    st.write(
                        extracted_profile.get(
                            "email",
                            ""
                        )
                    )

                with profile_col3:

                    st.write("**Phone**")

                    st.write(
                        extracted_profile.get(
                            "phone",
                            ""
                        )
                    )

                # ------------------------------------------------
                # EDUCATION
                # ------------------------------------------------

                st.subheader(
                    "🎓 Education"
                )

                education = extracted_profile.get(
                    "education",
                    []
                )

                if education:

                    for item in education:

                        st.write(
                            f"• {item}"
                        )

                else:

                    st.write(
                        "No education information detected."
                    )

                # ------------------------------------------------
                # SKILLS
                # ------------------------------------------------

                st.subheader(
                    "🛠️ Skills"
                )

                skills = extracted_profile.get(
                    "skills",
                    []
                )

                if skills:

                    st.write(
                        ", ".join(skills)
                    )

                else:

                    st.write(
                        "No skills detected."
                    )

                # ------------------------------------------------
                # EXPERIENCE
                # ------------------------------------------------

                st.subheader(
                    "💼 Experience"
                )

                experience = extracted_profile.get(
                    "experience",
                    []
                )

                if experience:

                    for item in experience:

                        st.write(
                            f"• {item}"
                        )

                else:

                    st.write(
                        "No experience information detected."
                    )

                # ------------------------------------------------
                # PROJECTS
                # ------------------------------------------------

                st.subheader(
                    "🚀 Projects"
                )

                projects = extracted_profile.get(
                    "projects",
                    []
                )

                if projects:

                    for item in projects:

                        st.write(
                            f"• {item}"
                        )

                else:

                    st.write(
                        "No projects detected."
                    )

                # ------------------------------------------------
                # QUALIFICATIONS
                # ------------------------------------------------

                st.subheader(
                    "📚 Qualifications"
                )

                qualifications = extracted_profile.get(
                    "qualifications",
                    []
                )

                if qualifications:

                    for item in qualifications:

                        st.write(
                            f"• {item}"
                        )

                else:

                    st.write(
                        "No qualifications detected."
                    )

                # ------------------------------------------------
                # SAVE PROFILE TO DATABASE
                # ------------------------------------------------

                profile_id = save_student_profile(
                    extracted_profile,
                    uploaded_file.name,
                    resume_path
                )

                st.session_state.profile_id = profile_id

                st.success(
                    f"✅ Candidate profile saved successfully. "
                    f"Profile ID: {profile_id}"
                )

                st.info(
                    "💡 Your profile is now available for Job Matching."
                )

            except Exception as error:

                st.error(
                    f"❌ Error: {error}"
                )


# ============================================================
# FIND JOBS
# ============================================================

elif page == "🔎 Find Jobs":

    st.title("🔎 Find Internship & Job Opportunities")

    st.write(
        "Find internships and jobs that match your resume, "
        "skills, education, experience, and projects."
    )

    st.divider()

    # --------------------------------------------------------
    # GET PROFILE FROM SESSION
    # --------------------------------------------------------

    candidate_profile = st.session_state.get(
        "candidate_profile"
    )

    if candidate_profile is None:

        st.warning(
            "⚠️ Please upload and process your resume first."
        )

        st.info(
            "Go to **📄 My Resume**, process your resume, "
            "and then return to **🔎 Find Jobs**."
        )

    else:

        candidate_name = candidate_profile.get(
            "name",
            "Candidate"
        )

        st.success(
            f"✅ Resume profile loaded for **{candidate_name}**"
        )

        st.subheader(
            "🔎 Search Matching Jobs"
        )

        top_k = st.selectbox(
            "How many matching jobs do you want to see?",
            [5, 10, 15],
            index=1
        )

        if st.button(
            "🔍 Search Matching Jobs",
            type="primary"
        ):

            with st.spinner(
                "🤖 Analyzing your profile and finding matching jobs..."
            ):

                try:

                    from src.matching_agent import (
                        rag_based_job_matching
                    )

                    ranked_jobs = rag_based_job_matching(
                        candidate_profile,
                        top_k=top_k
                    )

                    st.session_state.ranked_jobs = (
                        ranked_jobs
                    )

                except Exception as error:

                    st.error(
                        "❌ Something went wrong while searching for jobs."
                    )

                    st.exception(error)

        # ----------------------------------------------------
        # DISPLAY JOB RESULTS
        # ----------------------------------------------------

        ranked_jobs = st.session_state.get(
            "ranked_jobs",
            []
        )

        if ranked_jobs:

            st.divider()

            st.subheader(
                f"🎯 {len(ranked_jobs)} Matching Opportunities"
            )

            for rank, job in enumerate(
                ranked_jobs,
                start=1
            ):

                score = job.get(
                    "compatibility_score",
                    0
                )

                title = job.get(
                    "job_title",
                    "Unknown Job"
                )

                company = job.get(
                    "company",
                    "Unknown Company"
                )

                location = job.get(
                    "location",
                    "Location not specified"
                )

                st.markdown(
                    f"### #{rank} {title}"
                )

                st.write(
                    f"🏢 **Company:** {company}"
                )

                st.write(
                    f"📍 **Location:** {location}"
                )

                st.metric(
                    "Match Percentage",
                    f"{score:.1f}%"
                )

                with st.expander(
                    "📋 View Match Details"
                ):

                    matching_required = job.get(
                        "matching_required_skills",
                        []
                    )

                    missing_required = job.get(
                        "missing_required_skills",
                        []
                    )

                    matching_preferred = job.get(
                        "matching_preferred_skills",
                        []
                    )

                    reasoning = job.get(
                        "reasoning",
                        "No explanation available."
                    )

                    st.write(
                        "**✅ Matching Required Skills**"
                    )

                    if matching_required:

                        st.write(
                            ", ".join(
                                map(
                                    str,
                                    matching_required
                                )
                            )
                        )

                    else:

                        st.write(
                            "None identified"
                        )

                    st.write(
                        "**⚠️ Missing Required Skills**"
                    )

                    if missing_required:

                        st.write(
                            ", ".join(
                                map(
                                    str,
                                    missing_required
                                )
                            )
                        )

                    else:

                        st.write(
                            "None identified"
                        )

                    st.write(
                        "**⭐ Matching Preferred Skills**"
                    )

                    if matching_preferred:

                        st.write(
                            ", ".join(
                                map(
                                    str,
                                    matching_preferred
                                )
                            )
                        )

                    else:

                        st.write(
                            "None identified"
                        )

                    st.write(
                        "**💡 Why this job matches**"
                    )

                    st.write(
                        reasoning
                    )

                st.divider()


# ============================================================
# SKILL GAP
# ============================================================


# ============================================================
# SKILL GAP
# ============================================================

elif page == "📊 Skill Gap":
    st.title("📊 Skill Gap Analysis")
    st.write(
        "Analyze the skills you have and identify the skills you need "
        "to improve for a selected job opportunity."
    )

    candidate_profile = st.session_state.get("candidate_profile")

    if not candidate_profile:
        st.warning("Please upload and process your resume first.")
    else:
        st.success(
            f"Resume profile loaded for **{candidate_profile.get('name', 'Candidate')}**"
        )

        st.subheader("🎯 Select a Job")

        ranked_jobs = st.session_state.get("ranked_jobs", [])

        if not ranked_jobs:
            st.info(
                "Please go to **Find Jobs**, search for matching jobs, "
                "and then return here to analyze the skill gap."
            )
        else:
            # Create job selection options
            job_options = {}

            for job in ranked_jobs:
                job_id = job.get("job_id")
                job_title = job.get("job_title", "Unknown Job")
                company = job.get("company", "Unknown Company")

                if job_id:
                    display_name = f"{job_title} — {company} ({job_id})"
                    job_options[display_name] = job_id

            if job_options:
                selected_job_display = st.selectbox(
                    "Choose a job from your matched jobs:",
                    list(job_options.keys())
                )

                selected_job_id = job_options[selected_job_display]

                if st.button("🔍 Analyze Skill Gap"):
                    from src.job_data import get_job_by_id
                    from src.skill_gap_agent import analyze_skill_gap

                    selected_job = get_job_by_id(selected_job_id)

                    if not selected_job:
                        st.error("Could not find the selected job.")
                    else:
                        result = analyze_skill_gap(
                            candidate_profile,
                            selected_job
                        )

                        st.subheader("💼 Selected Job")

                        st.write(
                            f"**Job:** {result['job_title']}"
                        )
                        st.write(
                            f"**Company:** {result['company']}"
                        )

                        st.subheader("📌 Skill Gap Level")

                        gap_level = result["gap_level"]

                        if gap_level == "Low":
                            st.success(f"🟢 {gap_level}")
                        elif gap_level == "Moderate":
                            st.warning(f"🟡 {gap_level}")
                        else:
                            st.error(f"🔴 {gap_level}")

                        st.subheader("✅ Matching Required Skills")

                        if result["matching_required_skills"]:
                            for skill in result["matching_required_skills"]:
                                st.write(
                                    f"• {skill.replace('_', ' ').title()}"
                                )
                        else:
                            st.info("No matching required skills found.")

                        st.subheader("⚠️ Missing Required Skills")

                        if result["missing_required_skills"]:
                            for skill in result["missing_required_skills"]:
                                st.write(
                                    f"• {skill.replace('_', ' ').title()}"
                                )
                        else:
                            st.success(
                                "No missing required skills."
                            )

                        st.subheader("⭐ Matching Preferred Skills")

                        if result["matching_preferred_skills"]:
                            for skill in result["matching_preferred_skills"]:
                                st.write(
                                    f"• {skill.replace('_', ' ').title()}"
                                )
                        else:
                            st.info(
                                "No matching preferred skills found."
                            )

                        st.subheader("📚 Missing Preferred Skills")

                        if result["missing_preferred_skills"]:
                            for skill in result["missing_preferred_skills"]:
                                st.write(
                                    f"• {skill.replace('_', ' ').title()}"
                                )
                        else:
                            st.success(
                                "No missing preferred skills."
                            )

                        st.subheader("🚀 Recommendations")

                        for recommendation in result["recommendations"]:
                            st.write(f"• {recommendation}")

            else:
                st.warning("No matched jobs are available.")

                # ============================================================
# RESUME ASSISTANT
# ============================================================

elif page == "✍️ Resume Assistant":

    st.title("✍️ Resume Assistant")

    st.write(
        "Improve your resume by reviewing your skills, education, "
        "experience, projects, and qualifications."
    )

    st.divider()

    candidate_profile = st.session_state.get("candidate_profile")

    if not candidate_profile:

        st.warning("⚠️ Please upload and process your resume first.")

        st.info(
            "Go to **📄 My Resume**, process your resume, "
            "and then return to **✍️ Resume Assistant**."
        )

    else:

        candidate_name = candidate_profile.get(
            "name",
            "Candidate"
        )

        st.success(
            f"✅ Resume profile loaded for **{candidate_name}**"
        )

        st.subheader("📋 Resume Overview")

        # --------------------------------------------------------
        # SKILLS
        # --------------------------------------------------------

        skills = candidate_profile.get(
            "skills",
            []
        )

        st.write("### 🛠️ Skills")

        if skills:

            for skill in skills:
                st.write(
                    f"• {skill}"
                )

        else:

            st.info(
                "No skills were detected in your resume."
            )

        # --------------------------------------------------------
        # EDUCATION
        # --------------------------------------------------------

        education = candidate_profile.get(
            "education",
            []
        )

        st.write("### 🎓 Education")

        if education:

            for item in education:
                st.write(
                    f"• {item}"
                )

        else:

            st.info(
                "No education information was detected."
            )

        # --------------------------------------------------------
        # EXPERIENCE
        # --------------------------------------------------------

        experience = candidate_profile.get(
            "experience",
            []
        )

        st.write("### 💼 Experience")

        if experience:

            for item in experience:
                st.write(
                    f"• {item}"
                )

        else:

            st.info(
                "No experience information was detected."
            )

        # --------------------------------------------------------
        # PROJECTS
        # --------------------------------------------------------

        projects = candidate_profile.get(
            "projects",
            []
        )

        st.write("### 🚀 Projects")

        if projects:

            for item in projects:
                st.write(
                    f"• {item}"
                )

        else:

            st.info(
                "No projects were detected."
            )

        # --------------------------------------------------------
        # QUALIFICATIONS
        # --------------------------------------------------------

        qualifications = candidate_profile.get(
            "qualifications",
            []
        )

        st.write("### 📚 Qualifications")

        if qualifications:

            for item in qualifications:
                st.write(
                    f"• {item}"
                )

        else:

            st.info(
                "No additional qualifications were detected."
            )

        st.divider()

        # --------------------------------------------------------
        # RESUME IMPROVEMENT SUGGESTIONS
        # --------------------------------------------------------

        st.subheader("💡 Resume Improvement Suggestions")

        suggestions = []

        if not skills:
            suggestions.append(
                "Add a clear Skills section containing your technical and professional skills."
            )

        if not education:
            suggestions.append(
                "Add your educational qualifications, degree, institution, and relevant dates."
            )

        if not experience:
            suggestions.append(
                "If you have internship, training, freelance, or work experience, add it with clear responsibilities."
            )

        if not projects:
            suggestions.append(
                "Add relevant academic or personal projects and briefly explain the technologies used."
            )

        if not qualifications:
            suggestions.append(
                "Consider adding relevant certifications, courses, achievements, or qualifications."
            )

        if skills and projects:
            suggestions.append(
                "Your resume contains both skills and projects. Make sure the technologies listed in your Skills section are demonstrated in your projects."
            )

        if not suggestions:
            suggestions.append(
                "Your extracted resume profile contains the major sections. Review each section and make sure the information is accurate and up to date."
            )

        for suggestion in suggestions:

            st.write(
                f"• {suggestion}"
            )

        st.divider()

        st.subheader("🎯 Career Readiness Summary")

        section_count = 0

        if skills:
            section_count += 1

        if education:
            section_count += 1

        if experience:
            section_count += 1

        if projects:
            section_count += 1

        if qualifications:
            section_count += 1

        if section_count >= 4:

            st.success(
                "Your resume profile contains several important sections. "
                "You can now use Job Matching and Skill Gap Analysis to further improve your profile."
            )

        elif section_count >= 2:

            st.warning(
                "Your resume profile has some important information, "
                "but adding more sections can make your profile more complete."
            )

        else:

            st.info(
                "Your resume profile contains limited information. "
                "Consider adding more relevant details to strengthen your resume."
            )


      # ============================================================
# COVER LETTER
# ============================================================

elif page == "💌 Cover Letter":

    st.title("💌 Cover Letter Generator")

    st.write(
        "Generate a personalized cover letter based on your "
        "resume profile and a selected job opportunity."
    )

    st.divider()

    candidate_profile = st.session_state.get("candidate_profile")

    if not candidate_profile:

        st.warning("⚠️ Please upload and process your resume first.")

        st.info(
            "Go to **📄 My Resume**, process your resume, "
            "and then return to **💌 Cover Letter**."
        )

    else:

        candidate_name = candidate_profile.get(
            "name",
            "Candidate"
        )

        st.success(
            f"✅ Resume profile loaded for **{candidate_name}**"
        )

        st.subheader("🎯 Select a Job")

        ranked_jobs = st.session_state.get(
            "ranked_jobs",
            []
        )

        if not ranked_jobs:

            st.info(
                "Please go to **🔎 Find Jobs**, search for matching jobs, "
                "and then return here to generate a cover letter."
            )

        else:

            job_options = {}

            for job in ranked_jobs:

                job_id = job.get("job_id")
                job_title = job.get(
                    "job_title",
                    "Unknown Job"
                )
                company = job.get(
                    "company",
                    "Unknown Company"
                )

                if job_id:

                    display_name = (
                        f"{job_title} — {company} ({job_id})"
                    )

                    job_options[display_name] = job_id

            selected_job_display = st.selectbox(
                "Choose a job:",
                list(job_options.keys())
            )

            selected_job_id = job_options[
                selected_job_display
            ]

            if st.button(
                "✉️ Generate Cover Letter",
                type="primary"
            ):

                from src.job_data import get_job_by_id

                selected_job = get_job_by_id(
                    selected_job_id
                )

                if not selected_job:

                    st.error(
                        "Could not find the selected job."
                    )

                else:

                    job_title = selected_job.get(
                        "job_title",
                        "the position"
                    )

                    company = selected_job.get(
                        "company",
                        "the company"
                    )

                    skills = candidate_profile.get(
                        "skills",
                        []
                    )

                    education = candidate_profile.get(
                        "education",
                        []
                    )

                    projects = candidate_profile.get(
                        "projects",
                        []
                    )

                    experience = candidate_profile.get(
                        "experience",
                        []
                    )

                    skill_text = (
                        ", ".join(skills)
                        if skills
                        else "relevant technical skills"
                    )

                    education_text = (
                        "; ".join(education)
                        if education
                        else "a background in Computer Science"
                    )

                    project_text = (
                        "; ".join(projects)
                        if projects
                        else "academic and technical projects"
                    )

                    experience_text = (
                        "; ".join(experience)
                        if experience
                        else "academic and project-based experience"
                    )

                    cover_letter = f"""
Dear Hiring Manager,

I am writing to express my interest in the {job_title} position at {company}. I am currently pursuing my education in Computer Science and I am interested in applying my technical knowledge in a practical internship environment.

My technical skills include {skill_text}. My educational background includes {education_text}. I have also gained practical exposure through {project_text} and {experience_text}.

I am particularly interested in this opportunity because it would allow me to apply my technical knowledge, develop my professional skills, and gain valuable industry experience. I am eager to learn, contribute to the team, and take on new challenges.

I would be grateful for the opportunity to discuss how my skills and background could contribute to {company}. Thank you for considering my application.

Sincerely,

{candidate_name}
"""

                    st.divider()

                    st.subheader(
                        "📄 Generated Cover Letter"
                    )

                    st.text_area(
                        "Your personalized cover letter:",
                        cover_letter.strip(),
                        height=500
                    )

                    st.success(
                        "✅ Cover letter generated successfully!"
                    )    

                    # ============================================================
# INTERVIEW PREPARATION
# ============================================================

elif page == "🎤 Interview Prep":

    st.title("🎤 Interview Preparation")
    st.write(
        "Prepare for your interview using your resume profile "
        "and the job you selected."
    )

    st.divider()

    # Get candidate profile from session
    candidate_profile = st.session_state.get("candidate_profile")

    if not candidate_profile:
        st.warning("⚠️ Please upload and process your resume first.")

    else:
        st.success(
            f"Candidate: {candidate_profile.get('name', 'Candidate')}"
        )

        # Get matched jobs
        ranked_jobs = st.session_state.get("ranked_jobs", [])

        if not ranked_jobs:
            st.info(
                "Please go to 🔎 Find Jobs and generate your job matches first."
            )

        else:
            st.subheader("🎯 Select a Job")

            job_options = {}

            for job in ranked_jobs:
                job_id = job.get("job_id")
                job_title = job.get("job_title", "Unknown Job")
                company = job.get("company", "Unknown Company")

                if job_id:
                    display_name = f"{job_title} — {company}"
                    job_options[display_name] = job_id

            if not job_options:
                st.warning("No suitable jobs were found.")

            else:
                selected_job_display = st.selectbox(
                    "Choose the job you want to prepare for:",
                    list(job_options.keys())
                )

                selected_job_id = job_options[selected_job_display]

                if st.button(
                    "🎤 Generate Interview Preparation",
                    type="primary"
                ):

                    try:
                        from src.job_data import get_job_by_id
                        from src.interview_agent import (
                            generate_interview_preparation
                        )

                        selected_job = get_job_by_id(selected_job_id)

                        if not selected_job:
                            st.error("Could not find the selected job.")

                        else:
                            result = generate_interview_preparation(
                                candidate_profile,
                                selected_job
                            )

                            st.session_state.interview_preparation = result
                            st.session_state.interview_job_id = selected_job_id

                            st.success(
                                "✅ Interview preparation generated successfully!"
                            )

                    except Exception as e:
                        st.error("❌ Error generating interview preparation.")
                        st.exception(e)

            # Display generated interview preparation
            result = st.session_state.get("interview_preparation")

            if result:

                st.divider()

                st.header(
                    f"📋 Interview Preparation — "
                    f"{result.get('job_title', 'Selected Job')}"
                )

                st.write(
                    f"**Company:** {result.get('company', 'Unknown Company')}"
                )

                # Technical Questions
                st.subheader("💻 Technical Questions")

                for number, question in enumerate(
                    result.get("technical_questions", []),
                    start=1
                ):
                    st.write(f"**{number}.** {question}")

                # Resume / Project Questions
                st.subheader("📄 Resume / Project Questions")

                for number, question in enumerate(
                    result.get("resume_questions", []),
                    start=1
                ):
                    st.write(f"**{number}.** {question}")

                # HR Questions
                st.subheader("👩‍💼 HR Questions")

                for number, question in enumerate(
                    result.get("hr_questions", []),
                    start=1
                ):
                    st.write(f"**{number}.** {question}")

                # Preparation Topics
                st.subheader("📚 Preparation Topics")

                for topic in result.get("preparation_topics", []):
                    st.write(f"• {topic}")  

                  # ============================================================
# CAREER ASSISTANT
# ============================================================

elif page == "💬 Career Assistant":

    st.title("💬 Career Assistant")
    st.write(
        "Get personalized career guidance based on your resume "
        "and matched internship opportunities."
    )

    st.divider()

    # Get candidate profile
    candidate_profile = st.session_state.get(
        "candidate_profile"
    )

    if not candidate_profile:

        st.warning(
            "⚠️ Please upload and process your resume first."
        )

        st.info(
            "Go to **📄 My Resume**, process your resume, "
            "and then return to **💬 Career Assistant**."
        )

    else:

        st.success(
            f"✅ Profile loaded for "
            f"**{candidate_profile.get('name', 'Candidate')}**"
        )

        # Get matched jobs
        ranked_jobs = st.session_state.get(
            "ranked_jobs",
            []
        )

        st.subheader("🚀 Career Guidance")

        if st.button(
            "💬 Generate Career Guidance",
            type="primary"
        ):

            try:

                from src.career_assistant import (
                    generate_career_guidance
                )

                with st.spinner(
                    "🤖 Analyzing your career profile..."
                ):

                    career_result = (
                        generate_career_guidance(
                            candidate_profile,
                            ranked_jobs
                        )
                    )

                st.session_state.career_guidance = (
                    career_result
                )

                st.success(
                    "✅ Career guidance generated successfully!"
                )

            except Exception as e:

                st.error(
                    "❌ Error generating career guidance."
                )

                st.exception(e)

        # Display career guidance
        career_result = st.session_state.get(
            "career_guidance"
        )

        if career_result:

            st.divider()

            # Career Summary
            st.subheader("🎯 Career Summary")

            st.write(
                career_result.get(
                    "career_summary",
                    "No career summary available."
                )
            )

            # Current Skills
            st.subheader("💻 Your Current Skills")

            current_skills = career_result.get(
                "current_skills",
                []
            )

            if current_skills:

                for skill in current_skills:

                    st.write(
                        f"• {skill.replace('_', ' ').title()}"
                    )

            else:

                st.info(
                    "No current skills were detected."
                )

            # Recommended Skills
            st.subheader("📚 Recommended Skills")

            recommended_skills = career_result.get(
                "recommended_skills",
                []
            )

            if recommended_skills:

                for skill in recommended_skills:

                    st.write(
                        f"• {skill.replace('_', ' ').title()}"
                    )

            else:

                st.info(
                    "No additional skills were identified."
                )

            # Career Actions
            st.subheader("📝 Recommended Career Actions")

            career_actions = career_result.get(
                "career_actions",
                []
            )

            for action in career_actions:

                st.write(
                    f"• {action}"
                )

            # Job Direction
            st.subheader("🎯 Suitable Job Directions")

            job_direction = career_result.get(
                "job_direction",
                []
            )

            if job_direction:

                for job in job_direction:

                    st.write(
                        f"• {job}"
                    )

            else:

                st.info(
                    "Go to 🔎 Find Jobs to generate "
                    "job matches for personalized job directions."
                )

# ============================================================
# APPLICATION TRACKER
# ============================================================

if page == "📋 Application Tracker":

    st.title("📋 Application Tracker")
    st.write(
        "Track your internship and job applications, deadlines, "
        "interviews, and follow-ups in one place."
    )

    profile_id = st.session_state.get("profile_id")

    if not profile_id:

        st.warning(
            "Please upload and process your resume first "
            "from the 📄 My Resume page."
        )

    else:

        stats = get_application_statistics(profile_id)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Applications",
                stats["total_applications"]
            )

        with col2:
            st.metric(
                "Active Applications",
                stats["active_applications"]
            )

        with col3:
            st.metric(
                "Upcoming Deadlines",
                stats["upcoming_deadlines"]
            )

        col4, col5, col6 = st.columns(3)

        with col4:
            st.metric(
                "Interviews Scheduled",
                stats["interviews_scheduled"]
            )

        with col5:
            st.metric(
                "Offers Received",
                stats["offers"]
            )

        with col6:
            st.metric(
                "Rejected",
                stats["rejected"]
            )

        st.divider()

        tab1, tab2, tab3, tab4 = st.tabs([
            "➕ Add Application",
            "📋 My Applications",
            "📅 Deadlines",
            "🎤 Interviews"
        ])

        with tab1:

            st.subheader("➕ Add New Application")

            company = st.text_input("Company Name")

            job_title = st.text_input(
                "Internship / Job Title"
            )

            job_description = st.text_area(
                "Job Description"
            )

            col1, col2 = st.columns(2)

            with col1:
                application_date = st.date_input(
                    "Application Date"
                )

            with col2:
                deadline = st.date_input(
                    "Application Deadline"
                )

            status_options = [
                "Saved",
                "Planning to apply",
                "Applied",
                "Application under review",
                "Shortlisted",
                "Interview scheduled",
                "Interview completed",
                "Offer received",
                "Rejected",
                "Withdrawn"
            ]

            status = st.selectbox(
                "Application Status",
                status_options
            )

            interview_date = st.date_input(
                "Interview Date",
                value=None
            )

            interview_status_options = [
                "Not scheduled",
                "Scheduled",
                "Completed",
                "Cancelled"
            ]

            interview_status = st.selectbox(
                "Interview Status",
                interview_status_options
            )

            notes = st.text_area(
                "Notes / Follow-up"
            )

            resume_path = st.text_input(
                "Resume Used",
                value=""
            )

            cover_letter = st.text_area(
                "Cover Letter / Generated Content",
                value=""
            )

            if st.button(
                "💾 Save Application",
                use_container_width=True
            ):

                if not company.strip():

                    st.error(
                        "Please enter the company name."
                    )

                elif not job_title.strip():

                    st.error(
                        "Please enter the internship/job title."
                    )

                else:

                    application_id = add_application(

                        profile_id=profile_id,
                        company=company,
                        job_title=job_title,
                        job_description=job_description,
                        application_date=str(
                            application_date
                        ),
                        deadline=str(
                            deadline
                        ),
                        status=status,
                        interview_date=(
                            str(interview_date)
                            if interview_date
                            else ""
                        ),
                        interview_status=interview_status,
                        notes=notes,
                        resume_path=resume_path,
                        cover_letter=cover_letter
                    )

                    st.success(
                        f"Application saved successfully! "
                        f"Application ID: {application_id}"
                    )

                    st.rerun()

        with tab2:

            st.subheader("📋 My Applications")

            col1, col2 = st.columns(2)

            with col1:
                search_company = st.text_input(
                    "🔍 Search Company"
                )

            with col2:
                search_role = st.text_input(
                    "🔍 Search Role"
                )

            filter_status = st.selectbox(
                "Filter by Status",
                [
                    "All",
                    "Saved",
                    "Planning to apply",
                    "Applied",
                    "Application under review",
                    "Shortlisted",
                    "Interview scheduled",
                    "Interview completed",
                    "Offer received",
                    "Rejected",
                    "Withdrawn"
                ]
            )

            deadline_filter = st.selectbox(
                "Filter by Deadline",
                [
                    "All",
                    "Upcoming",
                    "Past"
                ]
            )

            applications = search_applications(
                profile_id=profile_id,
                company=search_company,
                job_title=search_role,
                status=filter_status,
                deadline_filter=deadline_filter
            )

            if not applications:

                st.info("No applications found.")

            else:

                for application in applications:

                    (
                        app_id,
                        app_profile_id,
                        company_name,
                        role,
                        description,
                        app_date,
                        app_deadline,
                        app_status,
                        app_interview_date,
                        app_interview_status,
                        app_notes,
                        app_resume,
                        app_cover_letter,
                        created_at,
                        updated_at
                    ) = application

                    with st.expander(
                        f"🏢 {company_name} — {role}"
                    ):

                        st.write(
                            f"**Status:** {app_status}"
                        )

                        st.write(
                            f"**Application Date:** {app_date}"
                        )

                        st.write(
                            f"**Deadline:** {app_deadline}"
                        )

                        if description:
                            st.write(
                                f"**Job Description:** {description}"
                            )

                        if app_interview_date:
                            st.write(
                                f"**Interview Date:** "
                                f"{app_interview_date}"
                            )

                        if app_interview_status:
                            st.write(
                                f"**Interview Status:** "
                                f"{app_interview_status}"
                            )

                        if app_notes:
                            st.write(
                                f"**Notes:** {app_notes}"
                            )

                        if app_resume:
                            st.write(
                                f"**Resume Used:** {app_resume}"
                            )

                        if app_cover_letter:

                            with st.expander(
                                "📄 View Cover Letter"
                            ):
                                st.write(app_cover_letter)

                        st.caption(
                            f"Application ID: {app_id}"
                        )

                        st.markdown(
                            "### ✏️ Update Application"
                        )

                        status_options_update = [
                            "Saved",
                            "Planning to apply",
                            "Applied",
                            "Application under review",
                            "Shortlisted",
                            "Interview scheduled",
                            "Interview completed",
                            "Offer received",
                            "Rejected",
                            "Withdrawn"
                        ]

                        current_status_index = (
                            status_options_update.index(
                                app_status
                            )
                            if app_status
                            in status_options_update
                            else 0
                        )

                        new_status = st.selectbox(
                            "Update Status",
                            status_options_update,
                            index=current_status_index,
                            key=f"status_{app_id}"
                        )

                        new_interview_date = st.text_input(
                             "Update Interview Date",
                             value=app_interview_date or "",
                             key=f"interview_date_{app_id}"
                        )

                        new_interview_status = st.selectbox(
                            "Update Interview Status",
                            interview_status_options,
                            index=(
                                interview_status_options.index(
                                    app_interview_status
                                )
                                if app_interview_status
                                in interview_status_options
                                else 0
                            ),
                            key=f"interview_status_{app_id}"
                        )

                        new_notes = st.text_area(
                            "Update Notes",
                            value=app_notes or "",
                            key=f"notes_{app_id}"
                        )

                        if st.button(
                            "🔄 Update",
                            key=f"update_{app_id}"
                        ):

                            update_application(
                                application_id=app_id,
                                company=company_name,
                                job_title=role,
                                job_description=description,
                                application_date=app_date,
                                deadline=app_deadline,
                                status=new_status,
                                interview_date=new_interview_date,
                                interview_status=new_interview_status,
                                notes=new_notes,
                                resume_path=app_resume,
                                cover_letter=app_cover_letter
                            )
                            

                            st.success(
                                "Application updated successfully."
                            )

                            st.rerun()

                        if st.button(
                            "🗑️ Delete Application",
                            key=f"delete_{app_id}"
                        ):

                            delete_application(app_id)

                            st.success(
                                "Application deleted."
                            )

                            st.rerun()

        with tab3:

            st.subheader("📅 Upcoming Deadlines")

            deadlines = get_upcoming_deadlines(
                profile_id,
                days=30
            )

            if not deadlines:

                st.info(
                    "No upcoming deadlines in the next 30 days."
                )

            else:

                for application in deadlines:

                    (
                        app_id,
                        app_profile_id,
                        company_name,
                        role,
                        description,
                        app_date,
                        app_deadline,
                        app_status,
                        app_interview_date,
                        app_interview_status,
                        app_notes,
                        app_resume,
                        app_cover_letter,
                        created_at,
                        updated_at
                    ) = application

                    st.warning(
                        f"📌 **{company_name}** — {role}\n\n"
                        f"Deadline: **{app_deadline}**\n\n"
                        f"Status: **{app_status}**"
                    )

        with tab4:

            st.subheader("🎤 Scheduled Interviews")

            interviews = get_scheduled_interviews(
                profile_id
            )

            if not interviews:

                st.info("No interviews scheduled.")

            else:

                for application in interviews:

                    (
                        app_id,
                        app_profile_id,
                        company_name,
                        role,
                        description,
                        app_date,
                        app_deadline,
                        app_status,
                        app_interview_date,
                        app_interview_status,
                        app_notes,
                        app_resume,
                        app_cover_letter,
                        created_at,
                        updated_at
                    ) = application

                    st.info(
                        f"🎤 **{company_name}** — {role}\n\n"
                        f"Interview Date: **{app_interview_date}**\n\n"
                        f"Interview Status: **{app_interview_status}**"
                    )

