import sqlite3
import json
from pathlib import Path


# Find the database from the project root
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "database" / "internship.db"


def get_candidate_profile(profile_id):
    """
    Retrieve one candidate profile from the SQLite database.
    """

    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            email,
            phone,
            education,
            skills,
            experience,
            projects,
            qualifications,
            resume_filename,
            resume_path
        FROM student_profiles
        WHERE id = ?
        """,
        (profile_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    profile = {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "phone": row[3],
        "education": json.loads(row[4]) if row[4] else [],
        "skills": json.loads(row[5]) if row[5] else [],
        "experience": json.loads(row[6]) if row[6] else [],
        "projects": json.loads(row[7]) if row[7] else [],
        "qualifications": json.loads(row[8]) if row[8] else [],
        "resume_filename": row[9],
        "resume_path": row[10]
    }

    return profile


if __name__ == "__main__":

    profile_id = 2

    candidate = get_candidate_profile(profile_id)

    if candidate:

        print("\n===== CANDIDATE PROFILE =====\n")

        print(f"Profile ID: {candidate['id']}")
        print(f"Name: {candidate['name']}")
        print(f"Email: {candidate['email']}")
        print(f"Phone: {candidate['phone']}")

        print(
            f"Education: {candidate['education']}"
        )

        print(
            f"Skills: {candidate['skills']}"
        )

        print(
            f"Experience: {candidate['experience']}"
        )

        print(
            f"Projects: {candidate['projects']}"
        )

        print(
            f"Qualifications: {candidate['qualifications']}"
        )

    else:

        print(
            f"No candidate found with Profile ID {profile_id}"
        )