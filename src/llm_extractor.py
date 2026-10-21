import re


def extract_candidate_information(resume_text):
    """
    Free rule-based resume information extractor.

    Extracts:
    - Name
    - Email
    - Phone
    - Education
    - Technical Skills
    - Experience
    - Projects
    - Qualifications / Certifications
    - Languages
    - Interests

    Does NOT use OpenAI API or any paid service.
    """

    # ==========================================================
    # 1. BASIC CLEANING
    # ==========================================================

    if not resume_text:
        resume_text = ""

    text = str(resume_text).strip()

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    lines = []

    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()

        if line:
            lines.append(line)

    # ==========================================================
    # 2. NAME
    # ==========================================================

    name = ""

    for line in lines[:15]:

        lower_line = line.lower()

        if (
            "resume" not in lower_line
            and "curriculum vitae" not in lower_line
            and "email" not in lower_line
            and "phone" not in lower_line
            and "mobile" not in lower_line
            and "@" not in line
            and not re.search(r"\d", line)
            and 2 <= len(line.split()) <= 5
        ):
            name = line
            break

    # ==========================================================
    # 3. EMAIL
    # ==========================================================

    email_match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    email = email_match.group(0) if email_match else ""

    # ==========================================================
    # 4. PHONE
    # ==========================================================

    phone_match = re.search(
        r"(?:\+91[\s-]?)?[6-9]\d{9}",
        text
    )

    phone = phone_match.group(0) if phone_match else ""

    # ==========================================================
    # 5. SECTION DETECTION
    # ==========================================================

    def clean_heading(line):

        clean = line.lower().strip()

        clean = clean.replace(":", " ")
        clean = clean.replace("|", " ")

        clean = re.sub(
            r"[^a-zA-Z0-9\s&]",
            " ",
            clean
        )

        clean = re.sub(
            r"\s+",
            " ",
            clean
        ).strip()

        return clean

    def identify_section(line):

        clean = clean_heading(line)

        # ------------------------------------------------------
        # EDUCATION
        # ------------------------------------------------------

        education_headings = [
            "education",
            "educational qualification",
            "educational qualifications",
            "academic qualification",
            "academic qualifications",
            "academics",
            "academic background"
        ]

        if any(
            heading == clean or heading in clean
            for heading in education_headings
        ):
            return "education"

        # ------------------------------------------------------
        # SKILLS
        # ------------------------------------------------------

        skill_headings = [
            "skills",
            "technical skills",
            "technical knowledge",
            "technical knowledge tools",
            "technical skills tools",
            "technical expertise",
            "core skills",
            "programming skills",
            "technologies",
            "technical proficiency"
        ]

        if any(
            heading == clean or heading in clean
            for heading in skill_headings
        ):
            return "skills"

        # ------------------------------------------------------
        # LANGUAGES
        # ------------------------------------------------------

        language_headings = [
            "languages",
            "language",
            "known languages",
            "languages known"
        ]

        if any(
            heading == clean or heading in clean
            for heading in language_headings
        ):
            return "languages"

        # ------------------------------------------------------
        # INTERESTS
        # ------------------------------------------------------

        interest_headings = [
            "interests",
            "interest",
            "hobbies",
            "hobbies interests"
        ]

        if any(
            heading == clean or heading in clean
            for heading in interest_headings
        ):
            return "interests"

        # ------------------------------------------------------
        # EXPERIENCE
        # ------------------------------------------------------

        experience_headings = [
            "experience",
            "work experience",
            "professional experience",
            "internship",
            "internships",
            "employment",
            "work history"
        ]

        if any(
            heading == clean or heading in clean
            for heading in experience_headings
        ):
            return "experience"

        # ------------------------------------------------------
        # PROJECTS
        # ------------------------------------------------------

        project_headings = [
            "projects",
            "project",
            "academic projects",
            "academic project",
            "personal projects",
            "personal project",
            "mini projects",
            "mini project",
            "major projects",
            "major project"
        ]

        if any(
            heading == clean or heading in clean
            for heading in project_headings
        ):
            return "projects"

        # ------------------------------------------------------
        # QUALIFICATIONS / CERTIFICATIONS
        # ------------------------------------------------------

        qualification_headings = [
            "certificates",
            "certificate",
            "certifications",
            "certification",
            "qualifications",
            "qualification",
            "courses",
            "courses certifications",
            "achievements",
            "achievement"
        ]

        if any(
            heading == clean or heading in clean
            for heading in qualification_headings
        ):
            return "qualifications"

        return None

    # ==========================================================
    # 6. COLLECT RESUME SECTIONS
    # ==========================================================

    sections = {
        "education": [],
        "skills": [],
        "languages": [],
        "interests": [],
        "experience": [],
        "projects": [],
        "qualifications": []
    }

    current_section = None

    for line in lines:

        detected_section = identify_section(line)

        if detected_section:

            current_section = detected_section

            continue

        if current_section:

            sections[current_section].append(line)

    # ==========================================================
    # 7. EDUCATION
    # ==========================================================

    education = []

    for item in sections["education"]:

        item = item.strip()

        if item:
            education.append(item)

    education = list(
        dict.fromkeys(education)
    )

    # ==========================================================
    # 8. TECHNICAL SKILLS
    # ==========================================================

    known_technical_skills = [

        "Python",
        "Java",
        "C",
        "C++",
        "C#",
        "JavaScript",
        "TypeScript",

        "HTML",
        "CSS",

        "SQL",
        "MySQL",
        "PostgreSQL",
        "MongoDB",

        "Machine Learning",
        "Deep Learning",
        "Artificial Intelligence",
        "Data Science",
        "Data Analysis",

        "TensorFlow",
        "PyTorch",
        "Scikit-learn",
        "OpenCV",

        "Git",
        "GitHub",

        "Flask",
        "Django",
        "React",
        "Node.js",

        "Power BI",
        "Tableau",
        "Excel",

        "Networking",

        "Cloud Computing",
        "AWS",
        "Azure",

        "Computer Vision",
        "Natural Language Processing"
    ]

    skills = []

    skills_section_text = " ".join(
        sections["skills"]
    )

    for skill in known_technical_skills:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            skills_section_text,
            flags=re.IGNORECASE
        ):
            skills.append(skill)

    skills = list(
        dict.fromkeys(skills)
    )

    # ==========================================================
    # 9. EXPERIENCE
    # ==========================================================

    experience = []

    for item in sections["experience"]:

        item = item.strip()

        if item:
            experience.append(item)

    experience = list(
        dict.fromkeys(experience)
    )

    # ==========================================================
    # 10. PROJECTS
    # ==========================================================

    projects = []

    for item in sections["projects"]:

        item = item.strip()

        if item:
            projects.append(item)

    projects = list(
        dict.fromkeys(projects)
    )

    # ==========================================================
    # 11. PROJECT FALLBACK
    # ==========================================================

    # If there is no explicit Projects section,
    # try to identify project-like information from
    # the rest of the resume.

    if not projects:

        project_keywords = [
            "developed",
            "designed",
            "implemented",
            "built",
            "created",
            "project",
            "application",
            "system",
            "website",
            "model"
        ]

        ignored_sections = [
            "education",
            "skills",
            "languages",
            "interests",
            "experience",
            "qualifications"
        ]

        for index, line in enumerate(lines):

            lower_line = line.lower()

            # Skip obvious section headings
            detected = identify_section(line)

            if detected in ignored_sections:
                continue

            # Skip contact information
            if (
                "@" in line
                or re.fullmatch(
                    r"(?:\+91[\s-]?)?[6-9]\d{9}",
                    line
                )
            ):
                continue

            # Check project-related keywords
            if any(
                keyword in lower_line
                for keyword in project_keywords
            ):

                # Avoid treating ordinary education lines
                # as projects.
                if (
                    "education" not in lower_line
                    and "college" not in lower_line
                    and "university" not in lower_line
                    and "school" not in lower_line
                    and "percentage" not in lower_line
                ):

                    projects.append(line)

                    # Include the following line if it
                    # looks like a project description.
                    if index + 1 < len(lines):

                        next_line = lines[index + 1]

                        if (
                            len(next_line.split()) >= 4
                            and not identify_section(next_line)
                        ):
                            projects.append(next_line)

        projects = list(
            dict.fromkeys(projects)
        )

    # ==========================================================
    # 12. QUALIFICATIONS / CERTIFICATIONS
    # ==========================================================

    qualifications = []

    for item in sections["qualifications"]:

        item = item.strip()

        if item:
            qualifications.append(item)

    qualifications = list(
        dict.fromkeys(qualifications)
    )

    # ==========================================================
    # 13. FALLBACK SKILL DETECTION
    # ==========================================================

    # If no dedicated skills section was detected,
    # search the entire resume for known technical skills.

    if not skills:

        lower_text = text.lower()

        for skill in known_technical_skills:

            if skill.lower() in lower_text:

                skills.append(skill)

        skills = list(
            dict.fromkeys(skills)
        )

    # ==========================================================
    # 14. LANGUAGES
    # ==========================================================

    languages = []

    for item in sections["languages"]:

        parts = re.split(
            r"[,;|•]+",
            item
        )

        for part in parts:

            part = part.strip(
                " -•\t"
            )

            if part:
                languages.append(part)

    languages = list(
        dict.fromkeys(languages)
    )

    # ==========================================================
    # 15. INTERESTS
    # ==========================================================

    interests = []

    for item in sections["interests"]:

        parts = re.split(
            r"[,;|•]+",
            item
        )

        for part in parts:

            part = part.strip(
                " -•\t"
            )

            if part:
                interests.append(part)

    interests = list(
        dict.fromkeys(interests)
    )

    # ==========================================================
    # 16. FINAL CANDIDATE PROFILE
    # ==========================================================

    return {
        "name": name,
        "email": email,
        "phone": phone,
        "education": education,
        "skills": skills,
        "experience": experience,
        "projects": projects,
        "qualifications": qualifications,
        "languages": languages,
        "interests": interests
    }