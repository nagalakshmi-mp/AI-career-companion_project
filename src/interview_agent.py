from job_data import get_job_by_id
from candidate_profile import get_candidate_profile
from matching_agent import normalize_text, get_candidate_skills


def generate_interview_preparation(candidate_profile, job):
    """
    Generate interview preparation material based on
    the candidate profile and selected job.

    The agent creates:
    - Technical questions
    - Resume/project questions
    - HR questions
    - Preparation topics based on skill gaps
    """

    candidate_skills = get_candidate_skills(
        candidate_profile
    )

    required_skills = normalize_text(
        job.get("required_skills", "")
    )

    missing_skills = (
        required_skills - candidate_skills
    )

    job_title = job.get(
        "job_title",
        "the position"
    )

    company = job.get(
        "company",
        "the company"
    )

    # --------------------------------------------------
    # TECHNICAL QUESTIONS
    # --------------------------------------------------

    technical_questions = []

    for skill in sorted(candidate_skills):

        skill_name = (
            skill.replace("_", " ").title()
        )

        technical_questions.append(
            f"Explain your knowledge of {skill_name} "
            f"and how you have used it."
        )

    # Add questions based on missing skills
    for skill in sorted(missing_skills):

        skill_name = (
            skill.replace("_", " ").title()
        )

        technical_questions.append(
            f"What do you know about {skill_name}, "
            f"and how would you learn or use it?"
        )

    # Keep a reasonable number of questions
    technical_questions = technical_questions[:8]

    if not technical_questions:

        technical_questions.append(
            "What technical skills are most relevant "
            "to this internship?"
        )

    # --------------------------------------------------
    # RESUME / PROJECT QUESTIONS
    # --------------------------------------------------

    resume_questions = [
        "Tell me about yourself and your academic background.",
        "Explain the most important project mentioned in your resume.",
        "What technical skills have you developed during your studies?",
        "What was the biggest challenge you faced while working on a project?",
        "How did you solve a technical problem in one of your projects?",
        "What did you learn from your academic or practical work?"
    ]

    # --------------------------------------------------
    # HR QUESTIONS
    # --------------------------------------------------

    hr_questions = [
        "Why are you interested in this internship?",
        f"Why are you interested in the {job_title} role?",
        f"Why would you like to work with {company}?",
        "What are your strengths?",
        "What is one area you are currently trying to improve?",
        "Where do you see yourself developing professionally?",
        "How do you handle learning a new technology?",
        "How do you work as part of a team?"
    ]

    # --------------------------------------------------
    # PREPARATION TOPICS
    # --------------------------------------------------

    preparation_topics = []

    for skill in sorted(missing_skills):

        skill_name = (
            skill.replace("_", " ").title()
        )

        preparation_topics.append(
            f"Revise and learn the basics of {skill_name}."
        )

    for skill in sorted(candidate_skills):

        skill_name = (
            skill.replace("_", " ").title()
        )

        preparation_topics.append(
            f"Prepare to explain your knowledge of "
            f"{skill_name} with a practical example."
        )

    if not preparation_topics:

        preparation_topics.append(
            "Review the job description and prepare "
            "examples from your academic experience."
        )

    return {

        "job_id": job.get("job_id"),

        "job_title": job_title,

        "company": company,

        "technical_questions":
            technical_questions,

        "resume_questions":
            resume_questions,

        "hr_questions":
            hr_questions,

        "preparation_topics":
            preparation_topics
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
    # GENERATE INTERVIEW PREPARATION
    # --------------------------------------------------

    result = generate_interview_preparation(
        candidate,
        job
    )

    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------

    print("\n===== INTERVIEW AGENT =====\n")

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
        "\n===== TECHNICAL QUESTIONS =====\n"
    )

    for number, question in enumerate(
        result["technical_questions"],
        start=1
    ):

        print(
            f"{number}. {question}"
        )

    print(
        "\n===== RESUME / PROJECT QUESTIONS =====\n"
    )

    for number, question in enumerate(
        result["resume_questions"],
        start=1
    ):

        print(
            f"{number}. {question}"
        )

    print(
        "\n===== HR QUESTIONS =====\n"
    )

    for number, question in enumerate(
        result["hr_questions"],
        start=1
    ):

        print(
            f"{number}. {question}"
        )

    print(
        "\n===== PREPARATION TOPICS =====\n"
    )

    for topic in result[
        "preparation_topics"
    ]:

        print(
            f"- {topic}"
        )