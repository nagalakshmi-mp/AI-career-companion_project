from job_data import get_job_by_id
from candidate_profile import get_candidate_profile
from matching_agent import normalize_text, get_candidate_skills


def generate_resume_suggestions(candidate_profile, job):
    """
    Generate job-specific resume customization suggestions.

    The agent only recommends information that already exists
    in the candidate profile. It does not invent skills,
    experience, education, or projects.
    """

    candidate_skills = get_candidate_skills(
        candidate_profile
    )

    required_skills = normalize_text(
        job.get("required_skills", "")
    )

    preferred_skills = normalize_text(
        job.get("preferred_skills", "")
    )

    # --------------------------------------------------
    # FIND RELEVANT SKILLS
    # --------------------------------------------------

    matching_required = (
        candidate_skills.intersection(
            required_skills
        )
    )

    matching_preferred = (
        candidate_skills.intersection(
            preferred_skills
        )
    )

    missing_required = (
        required_skills - candidate_skills
    )

    # --------------------------------------------------
    # RESUME SUGGESTIONS
    # --------------------------------------------------

    suggestions = []

    # Highlight matching required skills
    if matching_required:

        skills_text = ", ".join(
            skill.replace("_", " ").title()
            for skill in sorted(matching_required)
        )

        suggestions.append(
            f"Highlight these relevant skills in the "
            f"Skills section: {skills_text}."
        )

    # Highlight matching preferred skills
    if matching_preferred:

        skills_text = ", ".join(
            skill.replace("_", " ").title()
            for skill in sorted(matching_preferred)
        )

        suggestions.append(
            f"Also highlight these preferred skills "
            f"if they are supported by your resume: "
            f"{skills_text}."
        )

    # --------------------------------------------------
    # EXPERIENCE
    # --------------------------------------------------

    experience = candidate_profile.get(
        "experience", []
    )

    if experience:

        suggestions.append(
            "Place your most relevant experience "
            "prominently in the Experience section."
        )

    else:

        suggestions.append(
            "Since no clear professional experience "
            "was detected, emphasize academic work, "
            "projects, certifications, and technical skills."
        )

    # --------------------------------------------------
    # PROJECTS
    # --------------------------------------------------

    projects = candidate_profile.get(
        "projects", []
    )

    if projects:

        suggestions.append(
            "Highlight projects that demonstrate "
            "skills relevant to this job."
        )

    else:

        suggestions.append(
            "Add your relevant academic or personal "
            "projects to demonstrate practical skills."
        )

    # --------------------------------------------------
    # MISSING SKILLS
    # --------------------------------------------------

    if missing_required:

        missing_text = ", ".join(
            skill.replace("_", " ").title()
            for skill in sorted(missing_required)
        )

        suggestions.append(
            f"The job requires {missing_text}, but "
            f"these skills were not found in your "
            f"current profile. Add them to your resume "
            f"only if you genuinely have these skills."
        )

    # --------------------------------------------------
    # KEYWORD SUGGESTION
    # --------------------------------------------------

    job_title = job.get(
        "job_title",
        "this position"
    )

    suggestions.append(
        f"Make sure your resume clearly reflects "
        f"experience and skills relevant to the "
        f"{job_title} role."
    )

    # --------------------------------------------------
    # IMPORTANT SAFETY RULE
    # --------------------------------------------------

    suggestions.append(
        "Do not add skills, experience, projects, "
        "qualifications, or achievements that you "
        "do not actually have."
    )

    return {

        "job_id": job.get("job_id"),

        "job_title": job.get("job_title"),

        "company": job.get("company"),

        "matching_skills": sorted(
            matching_required
        ),

        "preferred_matching_skills": sorted(
            matching_preferred
        ),

        "missing_required_skills": sorted(
            missing_required
        ),

        "suggestions": suggestions
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
    # GENERATE RESUME SUGGESTIONS
    # --------------------------------------------------

    result = generate_resume_suggestions(
        candidate,
        job
    )

    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------

    print("\n===== RESUME AGENT =====\n")

    print(
        f"Candidate: {candidate['name']}"
    )

    print(
        f"Target Job: {result['job_title']}"
    )

    print(
        f"Company: {result['company']}"
    )

    print(
        "\nRelevant Skills:"
    )

    print(
        result["matching_skills"]
    )

    print(
        "\nPreferred Matching Skills:"
    )

    print(
        result["preferred_matching_skills"]
    )

    print(
        "\nMissing Required Skills:"
    )

    print(
        result["missing_required_skills"]
    )

    print(
        "\nResume Customization Suggestions:"
    )

    for suggestion in result[
        "suggestions"
    ]:

        print(
            f"- {suggestion}"
        )