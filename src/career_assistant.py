# ============================================================
# CAREER ASSISTANT AGENT
# ============================================================

from src.matching_agent import get_candidate_skills


def generate_career_guidance(candidate_profile, ranked_jobs=None):
    """
    Generate personalized career guidance based on
    the candidate profile and matched jobs.
    """

    if not candidate_profile:
        return {
            "career_summary": "No candidate profile available.",
            "current_skills": [],
            "recommended_skills": [],
            "career_actions": [],
            "job_direction": []
        }

    # --------------------------------------------------------
    # Candidate information
    # --------------------------------------------------------

    candidate_name = candidate_profile.get(
        "name",
        "Candidate"
    )

    education = candidate_profile.get(
        "education",
        ""
    )

    experience = candidate_profile.get(
        "experience",
        ""
    )

    projects = candidate_profile.get(
        "projects",
        ""
    )

    qualifications = candidate_profile.get(
        "qualifications",
        ""
    )

    # --------------------------------------------------------
    # Candidate skills
    # --------------------------------------------------------

    candidate_skills = get_candidate_skills(
        candidate_profile
    )

    current_skills = sorted(
        candidate_skills
    )

    # --------------------------------------------------------
    # Analyze matched jobs
    # --------------------------------------------------------

    recommended_skills = set()
    job_direction = []

    if ranked_jobs:

        for job in ranked_jobs[:5]:

            job_title = job.get(
                "job_title",
                "Unknown Role"
            )

            company = job.get(
                "company",
                "Unknown Company"
            )

            job_direction.append(
                f"{job_title} at {company}"
            )

            required_skills = job.get(
                "required_skills",
                ""
            )

            if isinstance(
                required_skills,
                str
            ):

                skills = [
                    skill.strip().lower()
                    for skill in required_skills.split(",")
                    if skill.strip()
                ]

                for skill in skills:

                    if skill not in candidate_skills:
                        recommended_skills.add(skill)

    recommended_skills = sorted(
        recommended_skills
    )

    # --------------------------------------------------------
    # Career summary
    # --------------------------------------------------------

    if current_skills:

        skill_text = ", ".join(
            skill.replace("_", " ").title()
            for skill in current_skills
        )

        career_summary = (
            f"{candidate_name} currently has a foundation "
            f"in {skill_text}. Based on the available profile "
            f"and matched internship opportunities, the next "
            f"focus should be strengthening technical skills, "
            f"building practical projects, and preparing for "
            f"technical and HR interviews."
        )

    else:

        career_summary = (
            f"{candidate_name} should focus on developing "
            f"core technical skills and building practical "
            f"projects to prepare for internship opportunities."
        )

    # --------------------------------------------------------
    # Career actions
    # --------------------------------------------------------

    career_actions = []

    if recommended_skills:

        for skill in recommended_skills[:6]:

            career_actions.append(
                f"Learn and practice the basics of "
                f"{skill.replace('_', ' ').title()}."
            )

    career_actions.extend([
        "Build at least one practical project using your technical skills.",
        "Keep your resume updated with projects, certifications, and skills.",
        "Practice explaining your projects clearly during interviews.",
        "Prepare common technical and HR interview questions.",
        "Apply regularly for internships that match your skills."
    ])

    # --------------------------------------------------------
    # Return career guidance
    # --------------------------------------------------------

    return {

        "candidate_name":
            candidate_name,

        "career_summary":
            career_summary,

        "current_skills":
            current_skills,

        "recommended_skills":
            recommended_skills,

        "career_actions":
            career_actions,

        "job_direction":
            job_direction,

        "education":
            education,

        "experience":
            experience,

        "projects":
            projects,

        "qualifications":
            qualifications
    }


# ============================================================
# TEST THE CAREER ASSISTANT
# ============================================================

if __name__ == "__main__":

    print("\n===== CAREER ASSISTANT AGENT =====\n")

    print(
        "Career Assistant Agent loaded successfully."
    )

    print(
        "It can generate personalized career guidance "
        "from a candidate profile and matched jobs."
    )