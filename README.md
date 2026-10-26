# AI Career Companion

An AI-powered career assistance platform that helps students prepare for internships and job opportunities through resume analysis, job matching, skill-gap identification, interview preparation, and application tracking.

## Project Overview

AI Career Companion brings essential career preparation tools together in one Streamlit application. Students can upload their resumes, manage candidate profiles, explore relevant opportunities, identify missing skills, prepare application documents, practice interviews, and track their applications.

## Key Features

### 1. Resume and Candidate Profile Management
- Upload resumes and extract resume text.
- Create and manage structured candidate profiles.
- Identify candidate education, skills, and experience where available.

### 2. Internship and Job Search
- Search a dataset of job and internship opportunities.
- Compare candidate profiles with job requirements.
- Display relevant opportunities and matching scores.

### 3. Skill-Gap Analysis
- Identify skills required for a selected role.
- Compare required skills with candidate skills.
- Highlight areas for improvement and learning.

### 4. Resume Assistant
- Help students improve resume content for career opportunities.
- Support role-focused resume preparation.

### 5. Cover Letter Assistant
- Generate job-focused cover letter drafts using relevant candidate and job details.

### 6. Interview Preparation
- Help students prepare for interviews related to selected job roles.
- Support role-specific practice and preparation.

### 7. Career Assistant
- Provide career guidance related to job roles, skills, resumes, and internship preparation.

### 8. Application Tracker
- Track applications by company, job title, status, deadlines, interviews, and notes.
- Help students organize their application progress.

## Technology Stack

- **Programming Language:** Python
- **Web Framework:** Streamlit
- **Data Processing:** Pandas
- **Resume Processing:** PyMuPDF and python-docx, where applicable
- **Database:** SQLite
- **Vector Database:** ChromaDB
- **Embeddings:** Sentence Transformers
- **Dataset:** CSV-based job and internship listings
- **LLM Integration:** OpenAI API, where configured

## System Architecture

1. **Candidate Input:** Resume upload and profile information.
2. **Resume Processing:** Extract and organize candidate information.
3. **Profile Storage:** Store structured profile data in SQLite.
4. **Job Knowledge Base:** Load job and internship listings from a CSV dataset.
5. **Semantic Search:** Generate embeddings and retrieve relevant opportunities using the vector database.
6. **Career Assistance Modules:** Provide job matching, skill-gap analysis, resume assistance, cover letters, interview preparation, and career guidance.
7. **Application Tracking:** Store and manage application progress.

## Project Structure

```text
## 📁 Project Structure

```text
AI-career-companion_project/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── AGILE_METHODOLOGY.md
├── MILESTONE_1_REPORT.md
├── MILESTONE_2_REPORT.md
├── MILESTONE_3_REPORT.md
├── MILESTONE_4_REPORT.md
├── DEFECT_TRACKER.md
├── INSTALLATION_GUIDE.md
├── USER_GUIDE.md
├── CONTRIBUTING.md
├── CHANGELOG.md
│
├── data/
│   ├── README.md
│   └── jobs.csv
│
└── src/
    ├── __init__.py
    ├── candidate_profile.py
    ├── candidate_profile_data.py
    ├── career_assistant.py
    ├── check_jobs.py
    ├── cover_letter_agent.py
    ├── database.py
    ├── generate_jobs.py
    ├── interview_agent.py
    ├── job_data.py
    ├── llm_extractor.py
    ├── matching_agent.py
    ├── resume_agent.py
    ├── resume_parser.py
    ├── skill_gap_agent.py
    └── test_resume.py
```

```

*Note: The structure above illustrates the main project components. Actual subfolders and files may differ. Keep the existing source-code structure required by the application.*

## Installation and Execution

### Prerequisites
- Python installed on your computer.
- The project dependencies listed in `requirements.txt`.

### Steps

1. Clone or download the repository.
2. Open a terminal in the project directory.
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure any required API credentials locally using environment variables. Never commit API keys or `.env` files.
5. Start the application:

   ```bash
   python -m streamlit run app.py
   ```

6. Open the local URL shown in the terminal, usually `http://localhost:8501`.

## Security and Privacy

- Do not upload API keys, passwords, or private credentials.
- Do not commit personal resumes or private candidate records.
- Keep local databases and generated files out of the repository when they contain personal information.
- Use `.gitignore` to exclude sensitive and unnecessary files.

## Development Milestones

- **Milestone 1 — Resume and Candidate Profiles:** Resume upload, text extraction, structured candidate profiles, and database storage.
- **Milestone 2 — Job Knowledge Base and Matching:** Job dataset, retrieval pipeline, embeddings, vector search, job matching, and skill-gap analysis.
- **Milestone 3 — Career Guidance and Mentorship:** Career assistant and guided career-preparation workflows.
- **Milestone 4 — Application Tracking and Evaluation:** Application status tracking, deadlines, interview details, testing, and improvements to matching quality.

## Project Objective

To provide students with a centralized, practical platform for preparing resumes, discovering relevant opportunities, identifying skill gaps, preparing for interviews, and managing internship applications.

## Future Improvements

- Improve job-matching accuracy and evaluation.
- Expand the job and internship dataset.
- Add more learning resources for identified skill gaps.
- Improve automated testing, documentation, and deployment.
- Enhance career recommendations based on candidate profiles.

## Author

Developed as an AI-based career assistance project.
