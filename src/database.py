import sqlite3
import json
from datetime import datetime


DATABASE_PATH = "database/internship.db"


def get_connection():
    return sqlite3.connect(DATABASE_PATH)


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database():
    """
    Create all required database tables if they do not exist.
    """

    connection = get_connection()
    cursor = connection.cursor()

    # --------------------------------------------------------
    # STUDENT PROFILES TABLE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS student_profiles (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT,

            email TEXT,

            phone TEXT,

            education TEXT,

            skills TEXT,

            experience TEXT,

            projects TEXT,

            qualifications TEXT,

            resume_filename TEXT,

            resume_path TEXT

        )
    """)

    # --------------------------------------------------------
    # APPLICATION TRACKING TABLE
    # --------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            profile_id INTEGER,

            company TEXT NOT NULL,

            job_title TEXT NOT NULL,

            job_description TEXT,

            application_date TEXT,

            deadline TEXT,

            status TEXT DEFAULT 'Saved',

            interview_date TEXT,

            interview_status TEXT,

            notes TEXT,

            resume_path TEXT,

            cover_letter TEXT,

            created_at TEXT,

            updated_at TEXT,

            FOREIGN KEY (profile_id)
                REFERENCES student_profiles(id)

        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# STUDENT PROFILE FUNCTIONS
# ============================================================

def save_student_profile(profile, resume_filename, resume_path):
    """
    Save a structured candidate profile into SQLite.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO student_profiles (
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
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        profile.get("name", ""),

        profile.get("email", ""),

        profile.get("phone", ""),

        json.dumps(
            profile.get("education", [])
        ),

        json.dumps(
            profile.get("skills", [])
        ),

        json.dumps(
            profile.get("experience", [])
        ),

        json.dumps(
            profile.get("projects", [])
        ),

        json.dumps(
            profile.get("qualifications", [])
        ),

        resume_filename,

        resume_path
    ))

    connection.commit()

    profile_id = cursor.lastrowid

    connection.close()

    return profile_id


def get_student_profiles():
    """
    Retrieve all saved student profiles.
    """

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM student_profiles
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# ============================================================
# APPLICATION TRACKING FUNCTIONS
# ============================================================

def add_application(
    profile_id,
    company,
    job_title,
    job_description="",
    application_date="",
    deadline="",
    status="Saved",
    interview_date="",
    interview_status="",
    notes="",
    resume_path="",
    cover_letter=""
):
    """
    Add a new internship/job application.
    """

    connection = get_connection()
    cursor = connection.cursor()

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO applications (

            profile_id,
            company,
            job_title,
            job_description,
            application_date,
            deadline,
            status,
            interview_date,
            interview_status,
            notes,
            resume_path,
            cover_letter,
            created_at,
            updated_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        profile_id,
        company,
        job_title,
        job_description,
        application_date,
        deadline,
        status,
        interview_date,
        interview_status,
        notes,
        resume_path,
        cover_letter,
        current_time,
        current_time

    ))

    connection.commit()

    application_id = cursor.lastrowid

    connection.close()

    return application_id


def get_all_applications(profile_id=None):
    """
    Retrieve all applications.

    If profile_id is provided, only applications belonging
    to that student profile are returned.
    """

    connection = get_connection()
    cursor = connection.cursor()

    if profile_id is not None:

        cursor.execute("""
            SELECT *
            FROM applications
            WHERE profile_id = ?
            ORDER BY id DESC
        """, (profile_id,))

    else:

        cursor.execute("""
            SELECT *
            FROM applications
            ORDER BY id DESC
        """)

    rows = cursor.fetchall()

    connection.close()

    return rows


def get_application_by_id(application_id):
    """
    Retrieve one application using its ID.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM applications
        WHERE id = ?
    """, (application_id,))

    row = cursor.fetchone()

    connection.close()

    return row


def update_application(
    application_id,
    company,
    job_title,
    job_description="",
    application_date="",
    deadline="",
    status="Saved",
    interview_date="",
    interview_status="",
    notes="",
    resume_path="",
    cover_letter=""
):
    """
    Update an existing application.
    """

    connection = get_connection()
    cursor = connection.cursor()

    current_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        UPDATE applications

        SET

            company = ?,
            job_title = ?,
            job_description = ?,
            application_date = ?,
            deadline = ?,
            status = ?,
            interview_date = ?,
            interview_status = ?,
            notes = ?,
            resume_path = ?,
            cover_letter = ?,
            updated_at = ?

        WHERE id = ?
    """, (

        company,
        job_title,
        job_description,
        application_date,
        deadline,
        status,
        interview_date,
        interview_status,
        notes,
        resume_path,
        cover_letter,
        current_time,
        application_id

    ))

    connection.commit()

    connection.close()


def delete_application(application_id):
    """
    Delete an application.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM applications
        WHERE id = ?
    """, (application_id,))

    connection.commit()
    connection.close()


# ============================================================
# SEARCH AND FILTER FUNCTIONS
# ============================================================

def search_applications(
    profile_id=None,
    company="",
    job_title="",
    status="All",
    deadline_filter="All"
):
    """
    Search and filter applications by company,
    job title, status and deadline.
    """

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        SELECT *
        FROM applications
        WHERE 1 = 1
    """

    parameters = []

    if profile_id is not None:
        query += " AND profile_id = ?"
        parameters.append(profile_id)

    if company:
        query += " AND company LIKE ?"
        parameters.append(f"%{company}%")

    if job_title:
        query += " AND job_title LIKE ?"
        parameters.append(f"%{job_title}%")

    if status and status != "All":
        query += " AND status = ?"
        parameters.append(status)

    if deadline_filter == "Upcoming":

        query += """
            AND deadline != ''
            AND date(deadline) >= date('now')
        """

    elif deadline_filter == "Past":

        query += """
            AND deadline != ''
            AND date(deadline) < date('now')
        """

    query += """
        ORDER BY
            CASE
                WHEN deadline = '' THEN 1
                ELSE 0
            END,
            date(deadline) ASC,
            id DESC
    """

    cursor.execute(query, parameters)

    rows = cursor.fetchall()

    connection.close()

    return rows


# ============================================================
# UPCOMING DEADLINES
# ============================================================

def get_upcoming_deadlines(profile_id=None, days=7):
    """
    Get applications with deadlines occurring within
    the specified number of days.
    """

    connection = get_connection()
    cursor = connection.cursor()

    if profile_id is not None:

        cursor.execute("""
            SELECT *
            FROM applications

            WHERE profile_id = ?

            AND deadline != ''

            AND date(deadline)
                BETWEEN date('now')
                AND date('now', '+' || ? || ' days')

            ORDER BY date(deadline) ASC

        """, (profile_id, days))

    else:

        cursor.execute("""
            SELECT *
            FROM applications

            WHERE deadline != ''

            AND date(deadline)
                BETWEEN date('now')
                AND date('now', '+' || ? || ' days')

            ORDER BY date(deadline) ASC

        """, (days,))

    rows = cursor.fetchall()

    connection.close()

    return rows


# ============================================================
# SCHEDULED INTERVIEWS
# ============================================================

def get_scheduled_interviews(profile_id=None):
    """
    Retrieve applications with scheduled interviews.
    """

    connection = get_connection()
    cursor = connection.cursor()

    if profile_id is not None:

        cursor.execute("""
            SELECT *
            FROM applications
            WHERE profile_id = ?
            AND interview_status = 'Scheduled'
            ORDER BY date(interview_date) ASC
        """, (profile_id,))

    else:

        cursor.execute("""
            SELECT *
            FROM applications
            WHERE interview_status = 'Scheduled'
            ORDER BY date(interview_date) ASC
        """)

    rows = cursor.fetchall()

    connection.close()

    return rows


# ============================================================
# APPLICATION DASHBOARD STATISTICS
# ============================================================

def get_application_statistics(profile_id=None):
    """
    Return application tracking statistics for the dashboard.
    """

    connection = get_connection()
    cursor = connection.cursor()

    if profile_id is not None:

        condition = "WHERE profile_id = ?"
        parameters = (profile_id,)

    else:

        condition = ""
        parameters = ()

    # Total applications
    cursor.execute(
        f"""
        SELECT COUNT(*)
        FROM applications
        {condition}
        """,
        parameters
    )

    total_applications = cursor.fetchone()[0]

    # Active applications
    active_statuses = (
        "Saved",
        "Planning to apply",
        "Applied",
        "Application under review",
        "Shortlisted",
        "Interview scheduled",
        "Interview completed"
    )

    placeholders = ",".join(
        ["?"] * len(active_statuses)
    )

    if profile_id is not None:

        cursor.execute(
            f"""
            SELECT COUNT(*)
            FROM applications

            WHERE profile_id = ?

            AND status IN ({placeholders})
            """,
            (profile_id,) + active_statuses
        )

    else:

        cursor.execute(
            f"""
            SELECT COUNT(*)
            FROM applications

            WHERE status IN ({placeholders})
            """,
            active_statuses
        )

    active_applications = cursor.fetchone()[0]

    # Upcoming deadlines
    if profile_id is not None:

        cursor.execute("""
            SELECT COUNT(*)
            FROM applications

            WHERE profile_id = ?

            AND deadline != ''

            AND date(deadline) >= date('now')

            AND date(deadline)
                <= date('now', '+7 days')

        """, (profile_id,))

    else:

        cursor.execute("""
            SELECT COUNT(*)
            FROM applications

            WHERE deadline != ''

            AND date(deadline) >= date('now')

            AND date(deadline)
                <= date('now', '+7 days')
        """)

    upcoming_deadlines = cursor.fetchone()[0]

    # Scheduled interviews
    if profile_id is not None:

        cursor.execute("""
            SELECT COUNT(*)
            FROM applications

            WHERE profile_id = ?

            AND interview_date != ''

        """, (profile_id,))

    else:

        cursor.execute("""
            SELECT COUNT(*)
            FROM applications

            WHERE interview_date != ''
        """)

    interviews_scheduled = cursor.fetchone()[0]

    # Offers
    if profile_id is not None:

        cursor.execute("""
            SELECT COUNT(*)
            FROM applications

            WHERE profile_id = ?

            AND status = 'Offer received'

        """, (profile_id,))

    else:

        cursor.execute("""
            SELECT COUNT(*)
            FROM applications

            WHERE status = 'Offer received'
        """)

    offers = cursor.fetchone()[0]

    # Rejected
    if profile_id is not None:

        cursor.execute("""
            SELECT COUNT(*)
            FROM applications

            WHERE profile_id = ?

            AND status = 'Rejected'

        """, (profile_id,))

    else:

        cursor.execute("""
            SELECT COUNT(*)
            FROM applications

            WHERE status = 'Rejected'
        """)

    rejected = cursor.fetchone()[0]

    connection.close()

    return {
        "total_applications": total_applications,
        "active_applications": active_applications,
        "upcoming_deadlines": upcoming_deadlines,
        "interviews_scheduled": interviews_scheduled,
        "offers": offers,
        "rejected": rejected
    }

print("\n--- APPLICATIONS IN DATABASE ---")

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT id, profile_id, company, job_title, status
    FROM applications
    ORDER BY id DESC
""")

rows = cursor.fetchall()

for row in rows:
    print(row)
connection.close()


