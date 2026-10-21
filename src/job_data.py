import csv
from pathlib import Path


# Location of the jobs CSV file
BASE_DIR = Path(__file__).resolve().parent.parent
JOBS_FILE = BASE_DIR / "data" / "jobs.csv"


def load_jobs():
    """
    Load internship/job postings from jobs.csv.
    """

    jobs = []

    if not JOBS_FILE.exists():
        print(f"Jobs file not found: {JOBS_FILE}")
        return jobs

    with open(JOBS_FILE, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            jobs.append(row)

    return jobs


def get_job_by_id(job_id):
    """
    Find a particular job using its job ID.
    """

    jobs = load_jobs()

    for job in jobs:
        if job.get("job_id") == job_id:
            return job

    return None


if __name__ == "__main__":
    jobs = load_jobs()

    print(f"Total jobs loaded: {len(jobs)}")

    if jobs:
        print("\nFirst job:")
        print(jobs[0])