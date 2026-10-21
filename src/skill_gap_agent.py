from job_data import get_job_by_id
from candidate_profile import get_candidate_profile
from matching_agent import normalize_text, get_candidate_skills


def analyze_skill_gap(candidate_profile, job):
    """
    Analyze the skill gap between a candidate
    and a selected internship/job.
    """

    # Get candidate skills
    candidate_skills = get_candidate_skills(
        candidate_profile
    )

    # Get job required skills
    required_skills = normalize_text(
        job.get("required_skills", "")
    )

    # Get job preferred skills
    preferred_skills = normalize_text(
        job.get("preferred_skills", "")
    )

    # Find matching required skills
    matching_required = (
        candidate_skills.intersection(
            required_skills
        )
    )

    # Find missing required skills
    missing_required = (
        required_skills - candidate_skills
    )

    # Find matching preferred skills
    matching_preferred = (
        candidate_skills.intersection(
            preferred_skills
        )
    )

    # Find missing preferred skills
    missing_preferred = (
        preferred_skills - candidate_skills
    )

    # --------------------------------------------------
    # CREATE RECOMMENDATIONS
    # --------------------------------------------------

    recommendations = []

    for skill in sorted(missing_required):

        recommendations.append(
            f"Learn or improve "
            f"{skill.replace('_', ' ').title()} "
            f"because it is a required skill for this job."
        )

    for skill in sorted(missing_preferred):

        recommendations.append(
            f"Consider learning "
            f"{skill.replace('_', ' ').title()} "
            f"to strengthen your profile."
        )

    if not recommendations:

        recommendations.append(
            "No major skill gaps were identified."
        )

    # --------------------------------------------------
    # DETERMINE GAP LEVEL
    # --------------------------------------------------

    if len(missing_required) == 0:

        gap_level = "Low"

    elif len(missing_required) <= 1:

        gap_level = "Moderate"

    else:

        gap_level = "High"

    # --------------------------------------------------
    # RETURN ANALYSIS
    # --------------------------------------------------

    return {

        "job_id": job.get("job_id"),

        "job_title": job.get("job_title"),

        "company": job.get("company"),

        "matching_required_skills":
            sorted(matching_required),

        "missing_required_skills":
            sorted(missing_required),

        "matching_preferred_skills":
            sorted(matching_preferred),

        "missing_preferred_skills":
            sorted(missing_preferred),

        "gap_level":
            gap_level,

        "recommendations":
            recommendations
    }


if __name__ == "__main__":

    # --------------------------------------------------
    # LOAD YOUR ACTUAL CANDIDATE PROFILE
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
    # SELECT A JOB
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
    # ANALYZE SKILL GAP
    # --------------------------------------------------

    result = analyze_skill_gap(
        candidate,
        job
    )

    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------

    print("\n===== SKILL GAP ANALYSIS =====\n")

    print(
        f"Candidate: {candidate['name']}"
    )

    print(
        f"Job: {result['job_title']}"
    )

    print(
        f"Company: {result['company']}"
    )

    print(
        f"Gap Level: {result['gap_level']}"
    )

    print(
        "\nMatching Required Skills:"
    )

    print(
        result["matching_required_skills"]
    )

    print(
        "\nMissing Required Skills:"
    )

    print(
        result["missing_required_skills"]
    )

    print(
        "\nMatching Preferred Skills:"
    )

    print(
        result["matching_preferred_skills"]
    )

    print(
        "\nMissing Preferred Skills:"
    )

    print(
        result["missing_preferred_skills"]
    )

    print(
        "\nRecommendations:"
    )

    for recommendation in result[
        "recommendations"
    ]:

        print(
            f"- {recommendation}"
        )