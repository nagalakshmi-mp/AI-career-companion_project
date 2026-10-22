import chromadb
from sentence_transformers import SentenceTransformer
from pathlib import Path
import sys


# ==========================================================
# PROJECT PATHS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SRC_DIR = BASE_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))


from candidate_profile import get_candidate_profile


# ==========================================================
# VECTOR DATABASE
# ==========================================================

VECTOR_DB_DIR = BASE_DIR / "database" / "chroma_db"

MODEL_NAME = "all-MiniLM-L6-v2"

COLLECTION_NAME = "internship_jobs"


# ==========================================================
# CACHED CHROMA CLIENT
# ==========================================================
#
# Streamlit may execute the application code many times.
# Creating a new PersistentClient every time can cause
# ChromaDB's Rust backend to be stopped and reused incorrectly.
#
# We therefore create ONE client and reuse it.
# ==========================================================

_chroma_client = None


def get_chroma_client():

    global _chroma_client

    if _chroma_client is None:

        VECTOR_DB_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        _chroma_client = chromadb.PersistentClient(
            path=str(VECTOR_DB_DIR)
        )

    return _chroma_client


# ==========================================================
# LOAD VECTOR DATABASE
# ==========================================================

def get_job_collection():

    client = get_chroma_client()

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    return collection


# ==========================================================
# CACHED EMBEDDING MODEL
# ==========================================================
#
# Loading SentenceTransformer repeatedly is unnecessary.
# Reuse the same model during the application session.
# ==========================================================

_embedding_model = None


def load_embedding_model():

    global _embedding_model

    if _embedding_model is None:

        _embedding_model = SentenceTransformer(
            MODEL_NAME
        )

    return _embedding_model


# ==========================================================
# BASIC SEMANTIC SEARCH
# ==========================================================

def search_jobs(
    query,
    top_k=5
):

    model = load_embedding_model()

    collection = get_job_collection()

    query_embedding = model.encode(
        [query]
    )[0].tolist()

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k
    )

    return results


# ==========================================================
# CREATE CANDIDATE SEARCH QUERY
# ==========================================================

def create_candidate_query(
    candidate
):

    skills = ", ".join(
        candidate.get(
            "skills",
            []
        )
    )

    education = " ".join(
        candidate.get(
            "education",
            []
        )
    )

    experience = " ".join(
        candidate.get(
            "experience",
            []
        )
    )

    projects = " ".join(
        candidate.get(
            "projects",
            []
        )
    )

    qualifications = " ".join(
        candidate.get(
            "qualifications",
            []
        )
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

def search_jobs_for_candidate(
    candidate,
    top_k=5
):

    # ------------------------------------------------------
    # Create candidate query
    # ------------------------------------------------------

    query = create_candidate_query(
        candidate
    )

    # ------------------------------------------------------
    # Retrieve a large pool first.
    #
    # This allows RAG to find relevant jobs from the
    # complete dataset before diversity filtering.
    # ------------------------------------------------------

    retrieval_count = 150

    model = load_embedding_model()

    collection = get_job_collection()

    query_embedding = model.encode(
        [query]
    )[0].tolist()

    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=retrieval_count
    )

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    documents = results.get(
        "documents",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    # ------------------------------------------------------
    # SELECT UNIQUE JOB TITLES
    #
    # Chroma returns jobs in semantic similarity order.
    #
    # Therefore, when multiple companies offer the same
    # job title, we keep the first and most semantically
    # relevant occurrence.
    # ------------------------------------------------------

    selected_metadatas = []

    selected_documents = []

    selected_distances = []

    seen_titles = set()

    for index in range(
        len(metadatas)
    ):

        metadata = metadatas[index]

        job_title = str(
            metadata.get(
                "job_title",
                ""
            )
        ).strip()

        # Ignore records without a job title
        if not job_title:
            continue

        # Normalize title for comparison
        normalized_title = (
            job_title
            .lower()
            .strip()
        )

        # --------------------------------------------------
        # Keep only the first occurrence of each job title
        # --------------------------------------------------

        if normalized_title in seen_titles:
            continue

        seen_titles.add(
            normalized_title
        )

        selected_metadatas.append(
            metadata
        )

        selected_documents.append(
            documents[index]
        )

        selected_distances.append(
            distances[index]
        )

        # --------------------------------------------------
        # Stop when requested number of unique job types
        # has been collected.
        # --------------------------------------------------

        if len(selected_metadatas) >= top_k:
            break

    # ------------------------------------------------------
    # Return only unique job-title recommendations.
    #
    # No duplicate-title fallback is used.
    # ------------------------------------------------------

    return {

        "metadatas": [
            selected_metadatas
        ],

        "documents": [
            selected_documents
        ],

        "distances": [
            selected_distances
        ]

    }


# ==========================================================
# DISPLAY RESULTS
# ==========================================================

def display_results(
    results,
    candidate
):

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    print(
        "\n======================================"
    )

    print(
        "CANDIDATE BASED RAG SEARCH"
    )

    print(
        "======================================"
    )

    print(
        f"\nCandidate: "
        f"{candidate.get('name', '')}"
    )

    print(
        f"Skills: "
        f"{candidate.get('skills', [])}"
    )

    print(
        f"\nRetrieved Unique Job Types: "
        f"{len(documents)}"
    )

    for index in range(
        len(documents)
    ):

        metadata = metadatas[index]

        print(
            f"\n----- Retrieved Job "
            f"{index + 1} -----"
        )

        print(
            f"Job ID: "
            f"{metadata.get('job_id', '')}"
        )

        print(
            f"Job Title: "
            f"{metadata.get('job_title', '')}"
        )

        print(
            f"Company: "
            f"{metadata.get('company', '')}"
        )

        print(
            f"Location: "
            f"{metadata.get('location', '')}"
        )

        print(
            f"Required Skills: "
            f"{metadata.get('required_skills', '')}"
        )

        print(
            f"Preferred Skills: "
            f"{metadata.get('preferred_skills', '')}"
        )

        print(
            f"Distance: "
            f"{distances[index]:.4f}"
        )

        print(
            "-" * 70
        )


# ==========================================================
# TEST WITH ACTUAL CANDIDATE
# ==========================================================

if __name__ == "__main__":

    PROFILE_ID = 8

    print(
        "======================================"
    )

    print(
        "CANDIDATE RAG SEARCH TEST"
    )

    print(
        "======================================"
    )

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
        f"\nCandidate loaded: "
        f"{candidate['name']}"
    )

    print(
        f"Skills: "
        f"{candidate['skills']}"
    )

    print(
        "\nSearching the vector database..."
    )

    results = search_jobs_for_candidate(
        candidate,
        top_k=10
    )

    display_results(
        results,
        candidate
    )