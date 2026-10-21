import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
JOBS_FILE = BASE_DIR / "data" / "jobs.csv"


REQUIRED_COLUMNS = [
    "job_id",
    "job_title",
    "company",
    "location",
    "job_description",
    "responsibilities",
    "required_skills",
    "preferred_skills",
    "qualifications",
    "experience",
    "education"
]


def load_jobs():

    with open(
        JOBS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        return list(reader)


def check_columns():

    with open(
        JOBS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        columns = reader.fieldnames

    print("\n===== COLUMN CHECK =====\n")

    for column in REQUIRED_COLUMNS:

        if column in columns:
            print(f"[OK] {column}")

        else:
            print(f"[MISSING] {column}")


def check_empty_fields(jobs):

    print("\n===== EMPTY FIELD CHECK =====\n")

    empty_count = 0

    for job in jobs:

        for field in REQUIRED_COLUMNS:

            value = job.get(field, "").strip()

            if not value:

                print(
                    f"[EMPTY] {job.get('job_id')} -> {field}"
                )

                empty_count += 1

    if empty_count == 0:

        print("No empty required fields found.")

    else:

        print(
            f"\nTotal empty fields: {empty_count}"
        )


def check_duplicate_ids(jobs):

    print("\n===== DUPLICATE JOB ID CHECK =====\n")

    ids = [
        job.get("job_id")
        for job in jobs
    ]

    duplicates = {
        job_id
        for job_id in ids
        if ids.count(job_id) > 1
    }

    if not duplicates:

        print("No duplicate job IDs found.")

    else:

        print(
            "Duplicate IDs:",
            sorted(duplicates)
        )


def check_duplicate_jobs(jobs):

    print("\n===== DUPLICATE JOB CONTENT CHECK =====\n")

    seen = set()
    duplicates = []

    for job in jobs:

        key = (
            job.get("job_title", "").strip().lower(),
            job.get("company", "").strip().lower(),
            job.get("location", "").strip().lower()
        )

        if key in seen:

            duplicates.append(key)

        else:

            seen.add(key)

    if not duplicates:

        print("No duplicate job records found.")

    else:

        print(
            f"Duplicate job records found: "
            f"{len(duplicates)}"
        )


def check_job_relevance(jobs):

    print("\n===== RELEVANCE CHECK =====\n")

    relevant_keywords = [
        "intern",
        "developer",
        "engineer",
        "analyst",
        "machine learning",
        "artificial intelligence",
        "software",
        "data",
        "cloud",
        "cybersecurity",
        "computer vision",
        "testing"
    ]

    irrelevant_jobs = []

    for job in jobs:

        combined_text = " ".join([
            job.get("job_title", ""),
            job.get("job_description", ""),
            job.get("responsibilities", "")
        ]).lower()

        if not any(
            keyword in combined_text
            for keyword in relevant_keywords
        ):

            irrelevant_jobs.append(
                job.get("job_id")
            )

    if not irrelevant_jobs:

        print(
            "All jobs appear relevant "
            "to internship/technology roles."
        )

    else:

        print(
            "Potentially irrelevant jobs:",
            irrelevant_jobs
        )


def show_summary(jobs):

    print("\n===== DATASET SUMMARY =====\n")

    print(
        f"Total job records: {len(jobs)}"
    )

    locations = sorted(
        set(
            job.get("location", "")
            for job in jobs
        )
    )

    print(
        f"Locations: {', '.join(locations)}"
    )

    titles = sorted(
        set(
            job.get("job_title", "")
            for job in jobs
        )
    )

    print(
        f"Unique job titles: {len(titles)}"
    )

    companies = sorted(
        set(
            job.get("company", "")
            for job in jobs
        )
    )

    print(
        f"Unique companies: {len(companies)}"
    )


if __name__ == "__main__":

    print("======================================")
    print("JOB DATASET VALIDATION")
    print("======================================")

    if not JOBS_FILE.exists():

        print(
            f"Jobs file not found: {JOBS_FILE}"
        )

        exit()

    jobs = load_jobs()

    check_columns()

    check_empty_fields(jobs)

    check_duplicate_ids(jobs)

    check_duplicate_jobs(jobs)

    check_job_relevance(jobs)

    show_summary(jobs)

    print("\n======================================")
    print("VALIDATION COMPLETE")
    print("======================================")