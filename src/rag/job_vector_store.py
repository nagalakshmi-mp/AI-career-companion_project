import csv
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

JOBS_FILE = BASE_DIR / "data" / "jobs.csv"

VECTOR_DB_DIR = BASE_DIR / "database" / "chroma_db"


# ==========================================================
# EMBEDDING MODEL
# ==========================================================

MODEL_NAME = "all-MiniLM-L6-v2"


# ==========================================================
# LOAD JOB DATA
# ==========================================================

def load_jobs():

    jobs = []

    with open(
        JOBS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            jobs.append(row)

    return jobs


# ==========================================================
# CREATE JOB DOCUMENT
# ==========================================================

def create_job_document(job):

    document = f"""
Job Title: {job.get('job_title', '')}

Company: {job.get('company', '')}

Location: {job.get('location', '')}

Job Description:
{job.get('job_description', '')}

Responsibilities:
{job.get('responsibilities', '')}

Required Skills:
{job.get('required_skills', '')}

Preferred Skills:
{job.get('preferred_skills', '')}

Qualifications:
{job.get('qualifications', '')}

Experience:
{job.get('experience', '')}

Education:
{job.get('education', '')}
"""

    return document.strip()


# ==========================================================
# CREATE VECTOR DATABASE
# ==========================================================

def create_vector_database():

    print("======================================")
    print("RAG JOB VECTOR DATABASE")
    print("======================================")

    # ------------------------------------------------------
    # Check jobs file
    # ------------------------------------------------------

    if not JOBS_FILE.exists():

        print(
            f"Jobs file not found: {JOBS_FILE}"
        )

        return

    # ------------------------------------------------------
    # Load jobs
    # ------------------------------------------------------

    jobs = load_jobs()

    print(
        f"Jobs loaded: {len(jobs)}"
    )

    # ------------------------------------------------------
    # Load embedding model
    # ------------------------------------------------------

    print("\nLoading embedding model...")

    model = SentenceTransformer(
        MODEL_NAME
    )

    print(
        "Embedding model loaded successfully."
    )

    # ------------------------------------------------------
    # Create ChromaDB directory
    # ------------------------------------------------------

    VECTOR_DB_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # ------------------------------------------------------
    # Create ChromaDB client
    # ------------------------------------------------------

    client = chromadb.PersistentClient(
        path=str(VECTOR_DB_DIR)
    )

    # ------------------------------------------------------
    # Create collection
    # ------------------------------------------------------

    collection = client.get_or_create_collection(
        name="internship_jobs"
    )

    # ------------------------------------------------------
    # Prepare documents
    # ------------------------------------------------------

    documents = []

    ids = []

    metadatas = []

    for job in jobs:

        document = create_job_document(
            job
        )

        documents.append(
            document
        )

        ids.append(
            job["job_id"]
        )

        metadatas.append({

            "job_id": job.get(
                "job_id",
                ""
            ),

            "job_title": job.get(
                "job_title",
                ""
            ),

            "company": job.get(
                "company",
                ""
            ),

            "location": job.get(
                "location",
                ""
            ),

            "required_skills": job.get(
                "required_skills",
                ""
            ),

            "preferred_skills": job.get(
                "preferred_skills",
                ""
            ),

            "education": job.get(
                "education",
                ""
            ),

            "experience": job.get(
                "experience",
                ""
            )
        })

    # ------------------------------------------------------
    # Generate embeddings
    # ------------------------------------------------------

    print("\nGenerating embeddings...")

    embeddings = model.encode(
        documents,
        show_progress_bar=True
    )

    print(
        "\nEmbeddings generated successfully."
    )

    # ------------------------------------------------------
    # Store embeddings in ChromaDB
    # ------------------------------------------------------

    print(
        "\nStoring jobs in ChromaDB..."
    )

    collection.upsert(

        ids=ids,

        documents=documents,

        embeddings=embeddings.tolist(),

        metadatas=metadatas
    )

    # ------------------------------------------------------
    # Verify database
    # ------------------------------------------------------

    total_documents = collection.count()

    print("\n======================================")
    print("RAG VECTOR DATABASE CREATED")
    print("======================================")

    print(
        f"Jobs stored in vector database: "
        f"{total_documents}"
    )

    print(
        f"Database location: {VECTOR_DB_DIR}"
    )

    print(
        "Collection name: internship_jobs"
    )

    print("======================================")


# ==========================================================
# RUN PROGRAM
# ==========================================================

if __name__ == "__main__":

    create_vector_database()