from pathlib import Path
import sys
import re


# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))


# ==========================================================
# IMPORT PROJECT MODULES
# ==========================================================

from candidate_profile import get_candidate_profile
from job_data import get_job_by_id
from rag.job_search import search_jobs_for_candidate


# ==========================================================
# SKILL NORMALIZATION
# ==========================================================

def normalize_skill(skill):
    """
    Normalize one technical skill.

    Examples:
        Machine Learning -> machine_learning
        Computer Vision -> computer_vision
        Cloud Computing -> cloud_computing
        C++ -> cpp
        Node.js -> nodejs
    """

    if not skill:
        return ""

    text = str(skill).lower().strip()

    # ------------------------------------------------------
    # Normalize common variations
    # ------------------------------------------------------

    replacements = {
        "machine learning": "machine_learning",
        "deep learning": "deep_learning",
        "computer vision": "computer_vision",
        "cloud computing": "cloud_computing",
        "artificial intelligence": "artificial_intelligence",
        "natural language processing": "natural_language_processing",
        "data science": "data_science",
        "power bi": "power_bi",
        "scikit-learn": "scikit_learn",
        "scikit learn": "scikit_learn",
        "node.js": "nodejs",
        "node js": "nodejs",
        "spring boot": "spring_boot",
        "sql server": "sql_server",
        "c sharp": "csharp",
        "c++": "cpp",
        "c#": "csharp",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # ------------------------------------------------------
    # Remove unwanted punctuation
    # ------------------------------------------------------

    text = re.sub(
        r"[^a-z0-9_+#]+",
        " ",
        text
    )

    text = text.strip()

    # ------------------------------------------------------
    # Convert remaining spaces to underscores
    #
    # This is important for phrases such as:
    # "cloud computing"
    # "machine learning"
    # ------------------------------------------------------

    text = text.replace(" ", "_")

    return text


# ==========================================================
# TEXT NORMALIZATION
# ==========================================================

def normalize_text(text):
    """
    Convert text into normalized technical terms.

    Multi-word technical skills are preserved.
    """

    if not text:
        return set()

    if isinstance(text, list):

        # Process every list item separately
        result = set()

        for item in text:

            normalized = normalize_skill(item)

            if normalized:
                result.add(normalized)

        return result

    text = str(text).lower()

    # ------------------------------------------------------
    # Replace multi-word skills BEFORE tokenization.
    # ------------------------------------------------------

    replacements = {
        "machine learning": "machine_learning",
        "deep learning": "deep_learning",
        "computer vision": "computer_vision",
        "cloud computing": "cloud_computing",
        "artificial intelligence": "artificial_intelligence",
        "natural language processing": "natural_language_processing",
        "data science": "data_science",
        "power bi": "power_bi",
        "scikit-learn": "scikit_learn",
        "scikit learn": "scikit_learn",
        "node.js": "nodejs",
        "node js": "nodejs",
        "spring boot": "spring_boot",
        "sql server": "sql_server",
        "c sharp": "csharp",
        "c++": "cpp",
        "c#": "csharp",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    # ------------------------------------------------------
    # Normalize punctuation
    # ------------------------------------------------------

    text = re.sub(
        r"[^a-z0-9_+#]+",
        " ",
        text
    )

    return set(
        text.split()
    )


# ==========================================================
# CANDIDATE SKILLS
# ==========================================================

def get_candidate_skills(candidate_profile):

    skills = candidate_profile.get(
        "skills",
        []
    )

    skill_set = set()

    for skill in skills:

        normalized = normalize_skill(
            skill
        )

        if normalized:
            skill_set.add(
                normalized
            )

    return skill_set


# ==========================================================
# EDUCATION MATCHING
# ==========================================================

def check_education_match(
    candidate_profile,
    job
):

    candidate_education = " ".join(
        str(item)
        for item in candidate_profile.get(
            "education",
            []
        )
    ).lower()

    job_education = str(
        job.get(
            "education",
            ""
        )
    ).lower()

    if not job_education.strip():
        return True

    # ------------------------------------------------------
    # Candidate Computer Science / Engineering
    # ------------------------------------------------------

    candidate_has_cs = (
        "computer science" in candidate_education
        or "engineering" in candidate_education
        or "b.e" in candidate_education
        or "btech" in candidate_education
        or "b.tech" in candidate_education
    )

    # ------------------------------------------------------
    # Job Computer Science requirement
    # ------------------------------------------------------

    job_has_cs = (
        "computer science" in job_education
    )

    if candidate_has_cs and job_has_cs:
        return True

    # ------------------------------------------------------
    # Bachelor's / Engineering requirement
    # ------------------------------------------------------

    bachelor_keywords = [
        "bachelor",
        "bachelor's",
        "bachelors",
        "b.e",
        "b.tech",
        "btech",
        "engineering"
    ]

    candidate_has_bachelor = any(
        keyword in candidate_education
        for keyword in bachelor_keywords
    )

    job_requires_bachelor = any(
        keyword in job_education
        for keyword in bachelor_keywords
    )

    if (
        candidate_has_bachelor
        and job_requires_bachelor
    ):
        return True

    # ------------------------------------------------------
    # AI / ML education
    # ------------------------------------------------------

    candidate_has_ai_ml = (
        "artificial intelligence" in candidate_education
        or "machine learning" in candidate_education
        or "computer science" in candidate_education
    )

    job_requires_ai_ml = (
        "artificial intelligence" in job_education
        or "machine learning" in job_education
        or "computer science" in job_education
        or " ai " in f" {job_education} "
        or " ml " in f" {job_education} "
    )

    if (
        candidate_has_ai_ml
        and job_requires_ai_ml
    ):
        return True

    # ------------------------------------------------------
    # General education term overlap
    # ------------------------------------------------------

    candidate_terms = normalize_text(
        candidate_education
    )

    job_terms = normalize_text(
        job_education
    )

    if not job_terms:
        return True

    return bool(
        candidate_terms.intersection(
            job_terms
        )
    )


# ==========================================================
# EXPERIENCE MATCHING
# ==========================================================

def check_experience(
    candidate_profile,
    job
):

    candidate_experience = candidate_profile.get(
        "experience",
        []
    )

    job_experience = str(
        job.get(
            "experience",
            ""
        )
    ).lower()

    # ------------------------------------------------------
    # Candidate has experience information
    # ------------------------------------------------------

    if candidate_experience:

        return {
            "status": "experience_available",
            "score": 10
        }

    # ------------------------------------------------------
    # Job accepts freshers
    # ------------------------------------------------------

    fresher_terms = [
        "0-1",
        "0 - 1",
        "fresher",
        "no experience",
        "0 years",
        "0 year"
    ]

    if any(
        term in job_experience
        for term in fresher_terms
    ):

        return {
            "status": "fresher_eligible",
            "score": 10
        }

    return {
        "status": "experience_required",
        "score": 0
    }


# ==========================================================
# PROJECT MATCHING
# ==========================================================

def calculate_project_match(
    candidate_profile,
    job
):

    projects = candidate_profile.get(
        "projects",
        []
    )

    if not projects:
        return 0

    project_text = " ".join(
        str(project)
        for project in projects
    )

    job_text = " ".join([
        job.get("job_title", ""),
        job.get("job_description", ""),
        job.get("responsibilities", ""),
        job.get("required_skills", ""),
        job.get("preferred_skills", "")
    ])

    project_terms = normalize_text(
        project_text
    )

    job_terms = normalize_text(
        job_text
    )

    if (
        not project_terms
        or not job_terms
    ):
        return 0

    overlap = project_terms.intersection(
        job_terms
    )

    overlap_ratio = (
        len(overlap)
        / len(project_terms)
    )

    return min(
        5,
        overlap_ratio * 5
    )


# ==========================================================
# QUALIFICATION MATCHING
# ==========================================================

def calculate_qualification_match(
    candidate_profile,
    job
):

    qualifications = candidate_profile.get(
        "qualifications",
        []
    )

    if not qualifications:
        return 0

    candidate_text = " ".join(
        str(item)
        for item in qualifications
    )

    job_text = " ".join([
        job.get("qualifications", ""),
        job.get("required_skills", ""),
        job.get("preferred_skills", "")
    ])

    candidate_terms = normalize_text(
        candidate_text
    )

    job_terms = normalize_text(
        job_text
    )

    if (
        not candidate_terms
        or not job_terms
    ):
        return 0

    overlap = candidate_terms.intersection(
        job_terms
    )

    if not overlap:
        return 0

    overlap_ratio = (
        len(overlap)
        / len(candidate_terms)
    )

    return min(
        5,
        overlap_ratio * 5
    )


# ==========================================================
# JOB CONTENT RELEVANCE
# ==========================================================

def calculate_content_match(
    candidate_profile,
    job
):

    candidate_text = " ".join([
        " ".join(
            str(x)
            for x in candidate_profile.get(
                "skills",
                []
            )
        ),
        " ".join(
            str(x)
            for x in candidate_profile.get(
                "qualifications",
                []
            )
        ),
        " ".join(
            str(x)
            for x in candidate_profile.get(
                "projects",
                []
            )
        )
    ])

    job_text = " ".join([
        job.get(
            "job_description",
            ""
        ),
        job.get(
            "responsibilities",
            ""
        )
    ])

    candidate_terms = normalize_text(
        candidate_text
    )

    job_terms = normalize_text(
        job_text
    )

    if (
        not candidate_terms
        or not job_terms
    ):
        return 0

    overlap = candidate_terms.intersection(
        job_terms
    )

    if not overlap:
        return 0

    overlap_ratio = (
        len(overlap)
        / len(candidate_terms)
    )

    return min(
        10,
        overlap_ratio * 10
    )


# ==========================================================
# CALCULATE COMPLETE JOB MATCH
# ==========================================================

def calculate_job_match(
    candidate_profile,
    job
):

    candidate_skills = get_candidate_skills(
        candidate_profile
    )

    # ======================================================
    # REQUIRED SKILLS - 45 POINTS
    # ======================================================

    required_skills = normalize_text(
        job.get(
            "required_skills",
            ""
        )
    )

    matching_required = (
        candidate_skills.intersection(
            required_skills
        )
    )

    missing_required = (
        required_skills
        - candidate_skills
    )

    if required_skills:

        required_score = (
            len(matching_required)
            / len(required_skills)
        ) * 45

    else:

        required_score = 45


    # ======================================================
    # PREFERRED SKILLS - 15 POINTS
    # ======================================================

    preferred_skills = normalize_text(
        job.get(
            "preferred_skills",
            ""
        )
    )

    matching_preferred = (
        candidate_skills.intersection(
            preferred_skills
        )
    )

    missing_preferred = (
        preferred_skills
        - candidate_skills
    )

    if preferred_skills:

        preferred_score = (
            len(matching_preferred)
            / len(preferred_skills)
        ) * 15

    else:

        preferred_score = 0


    # ======================================================
    # EDUCATION - 10 POINTS
    # ======================================================

    education_match = check_education_match(
        candidate_profile,
        job
    )

    education_score = (
        10
        if education_match
        else 0
    )


    # ======================================================
    # EXPERIENCE - 10 POINTS
    # ======================================================

    experience_result = check_experience(
        candidate_profile,
        job
    )

    experience_score = experience_result[
        "score"
    ]


    # ======================================================
    # PROJECTS - 5 POINTS
    # ======================================================

    project_score = calculate_project_match(
        candidate_profile,
        job
    )


    # ======================================================
    # QUALIFICATIONS - 5 POINTS
    # ======================================================

    qualification_score = (
        calculate_qualification_match(
            candidate_profile,
            job
        )
    )


    # ======================================================
    # JOB CONTENT RELEVANCE - 10 POINTS
    # ======================================================

    content_score = calculate_content_match(
        candidate_profile,
        job
    )


    # ======================================================
    # FINAL SCORE
    # ======================================================

    total_score = (
        required_score
        + preferred_score
        + education_score
        + experience_score
        + project_score
        + qualification_score
        + content_score
    )

    compatibility_score = min(
        100,
        total_score
    )


    # ======================================================
    # REASONING
    # ======================================================

    reasoning_parts = []

    if matching_required:

        reasoning_parts.append(
            "Matching required skills: "
            + ", ".join(
                sorted(matching_required)
            )
        )

    if missing_required:

        reasoning_parts.append(
            "Missing required skills: "
            + ", ".join(
                sorted(missing_required)
            )
        )

    if matching_preferred:

        reasoning_parts.append(
            "Matching preferred skills: "
            + ", ".join(
                sorted(matching_preferred)
            )
        )

    if missing_preferred:

        reasoning_parts.append(
            "Missing preferred skills: "
            + ", ".join(
                sorted(missing_preferred)
            )
        )

    if education_match:

        reasoning_parts.append(
            "Education requirement is satisfied."
        )

    else:

        reasoning_parts.append(
            "Education requirement may not be satisfied."
        )

    if (
        experience_result["status"]
        == "fresher_eligible"
    ):

        reasoning_parts.append(
            "Candidate has no listed experience, "
            "and this job accepts freshers."
        )

    elif (
        experience_result["status"]
        == "experience_available"
    ):

        reasoning_parts.append(
            "Candidate has listed experience."
        )

    else:

        reasoning_parts.append(
            "The job may require experience "
            "that is not listed in the candidate profile."
        )

    if project_score > 0:

        reasoning_parts.append(
            "Relevant project information was found."
        )

    else:

        reasoning_parts.append(
            "No relevant project information was found."
        )

    if qualification_score > 0:

        reasoning_parts.append(
            "Some qualification information is relevant."
        )

    else:

        reasoning_parts.append(
            "No strong qualification match was found."
        )

    if content_score > 0:

        reasoning_parts.append(
            "Candidate information overlaps with "
            "the job description or responsibilities."
        )

    else:

        reasoning_parts.append(
            "Limited overlap was found with the "
            "job description or responsibilities."
        )

    reasoning = " ".join(
        reasoning_parts
    )


    # ======================================================
    # RETURN RESULT
    # ======================================================

    return {

        "job_id": job.get(
            "job_id"
        ),

        "job_title": job.get(
            "job_title"
        ),

        "company": job.get(
            "company"
        ),

        "location": job.get(
            "location"
        ),

        "compatibility_score": round(
            compatibility_score,
            2
        ),

        "required_skill_score": round(
            required_score,
            2
        ),

        "preferred_skill_score": round(
            preferred_score,
            2
        ),

        "education_score": round(
            education_score,
            2
        ),

        "experience_score": round(
            experience_score,
            2
        ),

        "project_score": round(
            project_score,
            2
        ),

        "qualification_score": round(
            qualification_score,
            2
        ),

        "description_score": round(
            content_score,
            2
        ),

        "matching_required_skills": sorted(
            matching_required
        ),

        "missing_required_skills": sorted(
            missing_required
        ),

        "matching_preferred_skills": sorted(
            matching_preferred
        ),

        "missing_preferred_skills": sorted(
            missing_preferred
        ),

        "education_match": education_match,

        "experience_status": experience_result[
            "status"
        ],

        "reasoning": reasoning
    }


# ==========================================================
# RAG + MATCHING AGENT
# ==========================================================

def rag_based_job_matching(
    candidate_profile,
    top_k=10
):

    print(
        "\n======================================"
    )

    print(
        "RAG + MATCHING AGENT"
    )

    print(
        "======================================"
    )

    print(
        "\nStep 1: Retrieving a larger job pool using RAG..."
    )

    # ------------------------------------------------------
    # RAG retrieval
    #
    # job_search.py already removes repeated job titles.
    # Therefore, requesting 50 here will return only the
    # available unique job types.
    # ------------------------------------------------------

    retrieval_count = max(
        50,
        top_k
    )

    rag_results = search_jobs_for_candidate(
        candidate_profile,
        top_k=retrieval_count
    )

    metadata_list = rag_results.get(
        "metadatas",
        [[]]
    )[0]

    print(
        f"RAG retrieved "
        f"{len(metadata_list)} jobs."
    )

    print(
        "\nStep 2: Calculating compatibility scores..."
    )

    ranked_jobs = []

    seen_job_ids = set()

    # ------------------------------------------------------
    # Score each retrieved job
    # ------------------------------------------------------

    for metadata in metadata_list:

        job_id = metadata.get(
            "job_id"
        )

        if not job_id:
            continue

        if job_id in seen_job_ids:
            continue

        seen_job_ids.add(
            job_id
        )

        job = get_job_by_id(
            job_id
        )

        if not job:
            continue

        result = calculate_job_match(
            candidate_profile,
            job
        )

        ranked_jobs.append(
            result
        )

    # ------------------------------------------------------
    # Sort by:
    #
    # 1. Overall compatibility
    # 2. Required skill score
    # 3. Preferred skill score
    # ------------------------------------------------------

    ranked_jobs.sort(
        key=lambda item: (
            item["compatibility_score"],
            item["required_skill_score"],
            item["preferred_skill_score"]
        ),
        reverse=True
    )

    # ------------------------------------------------------
    # Return requested number of jobs
    # ------------------------------------------------------

    final_results = ranked_jobs[
        :top_k
    ]

    print(
        f"\nReturning top "
        f"{len(final_results)} jobs after matching."
    )

    return final_results


# ==========================================================
# DISPLAY FINAL RESULTS
# ==========================================================

def display_matching_results(
    ranked_jobs
):

    print(
        "\n======================================"
    )

    print(
        "FINAL RAG + MATCHING RESULTS"
    )

    print(
        "======================================"
    )

    for index, result in enumerate(
        ranked_jobs,
        start=1
    ):

        print(
            f"\n----- Rank {index} -----"
        )

        print(
            f"Job: "
            f"{result['job_title']}"
        )

        print(
            f"Company: "
            f"{result['company']}"
        )

        print(
            f"Location: "
            f"{result['location']}"
        )

        print(
            f"Compatibility Score: "
            f"{result['compatibility_score']:.2f}%"
        )

        print(
            f"Required Skill Score: "
            f"{result['required_skill_score']}"
        )

        print(
            f"Preferred Skill Score: "
            f"{result['preferred_skill_score']}"
        )

        print(
            f"Education Score: "
            f"{result['education_score']}"
        )

        print(
            f"Experience Score: "
            f"{result['experience_score']}"
        )

        print(
            f"Project Score: "
            f"{result['project_score']}"
        )

        print(
            f"Qualification Score: "
            f"{result['qualification_score']}"
        )

        print(
            f"Description Score: "
            f"{result['description_score']}"
        )

        print(
            f"Matching Required Skills: "
            f"{result['matching_required_skills']}"
        )

        print(
            f"Missing Required Skills: "
            f"{result['missing_required_skills']}"
        )

        print(
            f"Matching Preferred Skills: "
            f"{result['matching_preferred_skills']}"
        )

        print(
            f"Missing Preferred Skills: "
            f"{result['missing_preferred_skills']}"
        )

        print(
            f"Education Match: "
            f"{result['education_match']}"
        )

        print(
            f"Experience Status: "
            f"{result['experience_status']}"
        )

        print(
            f"Reasoning: "
            f"{result['reasoning']}"
        )

        print(
            "-" * 70
        )


# ==========================================================
# MAIN TEST
# ==========================================================

if __name__ == "__main__":

    PROFILE_ID = 8

    candidate = get_candidate_profile(
        PROFILE_ID
    )

    if not candidate:

        print(
            f"No candidate found "
            f"with Profile ID {PROFILE_ID}"
        )

        sys.exit()

    print(
        f"\nCandidate: "
        f"{candidate['name']}"
    )

    print(
        f"Skills: "
        f"{candidate['skills']}"
    )

    print(
        f"Education: "
        f"{candidate['education']}"
    )

    ranked_jobs = rag_based_job_matching(
        candidate,
        top_k=10
    )

    display_matching_results(
        ranked_jobs
    )