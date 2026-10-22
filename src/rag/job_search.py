
import csv
import sys
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = BASE_DIR / "src"
JOBS_FILE = BASE_DIR / "data" / "jobs.csv"
VECTOR_DB_DIR = BASE_DIR / "database" / "chroma_db"

if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from candidate_profile import get_candidate_profile


# ==========================================================
# CONFIGURATION
# ==========================================================

MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "internship_jobs"

_chroma_client = None
_embedding_model = None


# ==========================================================
# CHROMADB CLIENT
# ==========================================================

def get_chroma_client():
    global _chroma_client

    if _chroma_client is None:
        VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

        _chroma_client = chromadb.PersistentClient(
            path=str(VECTOR_DB_DIR)
        )

    return _chroma_client


# ==========================================================
# EMBEDDING MODEL
# ==========================================================

def load_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = SentenceTransformer(MODEL_NAME)

    return _embedding_model


# ==========================================================
# LOAD JOBS FROM CSV
# ==========================================================

def load_jobs():
    if not JOBS_FILE.exists():
        raise FileNotFoundError(
            f"Jobs file not found: {JOBS_FILE}"
        )

    with open(JOBS_FILE, "r", encoding="utf-8-sig", newline="") as file:
        jobs = list(csv.DictReader(file))

    if not jobs:
        raise ValueError(
            "No job records found in data/jobs.csv"
        )

    return jobs


# ==========================================================
# CREATE JOB DOCUMENT
# ==========================================================

def create_job_document(job):
    return f"""
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
""".strip()


# ==========================================================
# GET OR BUILD JOB COLLECTION
# ==========================================================

def get_job_collection():
    client = get_chroma_client()

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    # Build the collection from CSV if it is empty.
    if collection.count() == 0:
        jobs = load_jobs()

        documents = []
        ids = []
        metadatas = []

        for index, job in enumerate(jobs):
            document = create_job_document(job)

            job_id = str(
                job.get("job_id") or f"job_{index}"
            )

            documents.append(document)
            ids.append(job_id)

            metadatas.append({
                "job_id": job_id,
                "job_title": str(job.get("job_title", "")),
                "company": str(job.get("company", "")),
                "location": str(job.get("location", "")),
                "required_skills": str(job.get("required_skills", "")),
                "preferred_skills": str(job.get("preferred_skills", "")),
                "education": str(job.get("education", "")),
                "experience": str(job.get("experience", ""))
            })

        model = load_embedding_model()

        # Generate embeddings in batches to limit memory usage.
        batch_size = 64

        for start in range(0, len(documents), batch_size):
            batch_documents = documents[start:start + batch_size]
            batch_ids = ids[start:start + batch_size]
            batch_metadatas = metadatas[start:start + batch_size]

            embeddings = model.encode(
                batch_documents,
                show_progress_bar=False
            ).tolist()

            collection.upsert(
                ids=batch_ids,
                documents=batch_documents,
                embeddings=embeddings,
                metadatas=batch_metadatas
            )

    return collection


# ==========================================================
# BASIC SEMANTIC SEARCH
# ==========================================================

def search_jobs(query, top_k=5):
    model = load_embedding_model()
    collection = get_job_collection()

    query_embedding = model.encode([query])[0].tolist()

    total = collection.count()
    if total == 0:
        return {
            "ids": [[]],
            "metadatas": [[]],
            "documents": [[]],
            "distances": [[]]
        }

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, total)
    )


# ==========================================================
# CREATE CANDIDATE SEARCH QUERY
# ==========================================================

def create_candidate_query(candidate):
    skills = ", ".join(candidate.get("skills") or [])

    education = " ".join(
        str(item) for item in (candidate.get("education") or [])
    ) if isinstance(candidate.get("education"), list) else str(
        candidate.get("education") or ""
    )

    experience = " ".join(
        str(item) for item in (candidate.get("experience") or [])
    ) if isinstance(candidate.get("experience"), list) else str(
        candidate.get("experience") or ""
    )

    projects = " ".join(
        str(item) for item in (candidate.get("projects") or [])
    ) if isinstance(candidate.get("projects"), list) else str(
        candidate.get("projects") or ""
    )

    qualifications = " ".join(
        str(item) for item in (candidate.get("qualifications") or [])
    ) if isinstance(candidate.get("qualifications"), list) else str(
        candidate.get("qualifications") or ""
    )

    query = f"""
Candidate Skills:
{skills}

Education:
{education}

Experience:
{experience}

Projects:
{projects}

Qualifications:
{qualifications}
"""

    return query.strip()


# ==========================================================
# DIVERSE JOB RETRIEVAL
# ==========================================================

def search_jobs_for_candidate(candidate, top_k=5):
    query = create_candidate_query(candidate)

    model = load_embedding_model()
    collection = get_job_collection()

    total = collection.count()
    if total == 0:
        return {
            "metadatas": [[]],
            "documents": [[]],
            "distances": [[]]
        }

    query_embedding = model.encode([query])[0].tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(150, total)
    )

    metadatas = results.get("metadatas", [[]])[0]
    documents = results.get("documents", [[]])[0]
    distances = results.get("distances", [[]])[0]

    selected_metadatas = []
    selected_documents = []
    selected_distances = []
    seen_titles = set()

    for index, metadata in enumerate(metadatas):
        job_title = str(metadata.get("job_title", "")).strip()

        if not job_title:
            continue

        normalized_title = job_title.lower()

        if normalized_title in seen_titles:
            continue

        seen_titles.add(normalized_title)
        selected_metadatas.append(metadata)
        selected_documents.append(documents[index])
        selected_distances.append(distances[index])

        if len(selected_metadatas) >= top_k:
            break

    return {
        "metadatas": [selected_metadatas],
        "documents": [selected_documents],
        "distances": [selected_distances]
    }


# ==========================================================
# DISPLAY RESULTS
# ==========================================================

def display_results(results, candidate):
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    print("\n======================================")
    print("CANDIDATE BASED RAG SEARCH")
    print("======================================")
    print(f"\nCandidate: {candidate.get('name', '')}")
    print(f"Skills: {candidate.get('skills', [])}")
    print(f"\nRetrieved Unique Job Types: {len(documents)}")

    for index, document in enumerate(documents):
        metadata = metadatas[index]

        print(f"\n----- Retrieved Job {index + 1} -----")
        print(f"Job ID: {metadata.get('job_id', '')}")
        print(f"Job Title: {metadata.get('job_title', '')}")
        print(f"Company: {metadata.get('company', '')}")
        print(f"Location: {metadata.get('location', '')}")
        print(f"Required Skills: {metadata.get('required_skills', '')}")
        print(f"Preferred Skills: {metadata.get('preferred_skills', '')}")
        print(f"Distance: {distances[index]:.4f}")
        print(f"Document: {document}")
        print("-" * 70)


# ==========================================================
# OPTIONAL COMMAND-LINE TEST
# ==========================================================

if __name__ == "__main__":
    PROFILE_ID = 8

    print("CANDIDATE RAG SEARCH TEST")

    candidate = get_candidate_profile(PROFILE_ID)

    if not candidate:
        print(f"No candidate found with Profile ID {PROFILE_ID}")
        sys.exit(1)

    print(f"Candidate loaded: {candidate['name']}")
    results = search_jobs_for_candidate(candidate, top_k=10)
    display_results(results, candidate)
