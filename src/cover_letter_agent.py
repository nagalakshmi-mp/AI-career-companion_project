from job_data import get_job_by_id
from candidate_profile import get_candidate_profile
from matching_agent import normalize_text, get_candidate_skills


def generate_cover_letter(candidate_profile, job):
    """
    Generate a personalized cover letter using
    information that already exists in the candidate profile.

    The system does not invent skills, experience,
    projects, qualifications, or achievements.
    """

    candidate_name = candidate_profile.get(
        "name",
        "Candidate"
    )

    education = candidate_profile.get(
        "education",
        []
    )

    experience = candidate_profile.get(
        "experience",
        []
    )

    projects = candidate_profile.get(
        "projects",
        []
    )

    candidate_skills = get_candidate_skills(
        candidate_profile
    )

    required_skills = normalize_text(
        job.get("required_skills", "")
    )

    matching_skills = candidate_skills.intersection(
        required_skills
    )

    job_title = job.get(
        "job_title",
        "the position"
    )

    company = job.get(
        "company",
        "your company"
    )

    responsibilities = job.get(
        "responsibilities",
        ""
    )

    # --------------------------------------------------
    # EDUCATION
    # --------------------------------------------------

    education_text = ""

    if education:

        # Use the first education item as the
        # main educational qualification.
        education_text = education[0]

    else:

        education_text = (
            "my academic background"
        )

    # --------------------------------------------------
    # SKILLS
    # --------------------------------------------------

    if matching_skills:

        skills_text = ", ".join(
            skill.replace("_", " ").title()
            for skill in sorted(matching_skills)
        )

    else:

        skills_text = (
            "my technical skills and academic knowledge"
        )

    # --------------------------------------------------
    # EXPERIENCE / PROJECTS
    # --------------------------------------------------

    practical_experience = ""

    if projects:

        practical_experience = (
            "I have also worked on academic or "
            "personal projects that have helped me "
            "apply my technical knowledge in practical "
            "situations."
        )

    elif experience:

        practical_experience = (
            "My academic and practical experience has "
            "helped me develop problem-solving and "
            "technical skills."
        )

    else:

        practical_experience = (
            "Through my academic studies and learning "
            "activities, I have been developing my "
            "technical and problem-solving skills."
        )

    # --------------------------------------------------
    # COVER LETTER
    # --------------------------------------------------

    cover_letter = f"""
Dear Hiring Manager,

I am writing to express my interest in the
{job_title} position at {company}.

I am currently pursuing {education_text}, and I am
interested in applying my technical knowledge and
learning more through an internship opportunity.

Based on the requirements of the role, I believe my
knowledge of {skills_text} is relevant to this
position. {practical_experience}

I am particularly interested in this opportunity
because it would allow me to develop my technical
skills while contributing to the work carried out
at {company}.

I am a motivated learner and I am willing to improve
my knowledge in areas that are important for the
role. I would be grateful for the opportunity to
discuss how my background and skills could
contribute to your team.

Thank you for considering my application. I look
forward to the opportunity to learn and contribute
as a {job_title} intern.

Sincerely,

{candidate_name}
"""

    return {
        "candidate_name": candidate_name,
        "job_title": job_title,
        "company": company,
        "cover_letter": cover_letter.strip()
    }


if __name__ == "__main__":

    # --------------------------------------------------
    # LOAD ACTUAL CANDIDATE
    # --------------------------------------------------

    PROFILE_ID = 2

    candidate = get_candidate_profile(
        PROFILE_ID
    )

    if not candidate:

        print(
            f"No candidate found with ID {PROFILE_ID}"
        )

        exit()

    # --------------------------------------------------
    # SELECT JOB
    # --------------------------------------------------

    # J001 = Python Developer Intern
    JOB_ID = "J001"

    job = get_job_by_id(
        JOB_ID
    )

    if not job:

        print(
            f"No job found with ID {JOB_ID}"
        )

        exit()

    # --------------------------------------------------
    # GENERATE COVER LETTER
    # --------------------------------------------------

    result = generate_cover_letter(
        candidate,
        job
    )

    # --------------------------------------------------
    # DISPLAY COVER LETTER
    # --------------------------------------------------

    print("\n===== COVER LETTER AGENT =====\n")

    print(
        f"Candidate: {result['candidate_name']}"
    )

    print(
        f"Target Job: {result['job_title']}"
    )

    print(
        f"Company: {result['company']}"
    )

    print("\n===== GENERATED COVER LETTER =====\n")

    print(
        result["cover_letter"]
    )

    print(
        "\n=================================="
    )