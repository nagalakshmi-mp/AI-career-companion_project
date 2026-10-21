import csv
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
JOBS_FILE = DATA_DIR / "jobs.csv"


JOB_TEMPLATES = [
    {
        "title": "Python Developer Intern",
        "company": "TechNova",
        "location": "Bengaluru",
        "description": "Work on Python software development projects and assist with application development.",
        "responsibilities": "Develop Python applications, debug code and assist the development team.",
        "required": "Python SQL Git",
        "preferred": "Flask Django",
        "qualification": "Programming fundamentals",
        "education": "Bachelor's in Computer Science"
    },
    {
        "title": "Machine Learning Intern",
        "company": "DataMind",
        "location": "Bengaluru",
        "description": "Assist in developing machine learning solutions using real-world datasets.",
        "responsibilities": "Prepare data, train models and evaluate machine learning results.",
        "required": "Python Machine Learning SQL",
        "preferred": "TensorFlow Scikit-learn",
        "qualification": "Machine learning fundamentals",
        "education": "Bachelor's in Computer Science or AI"
    },
    {
        "title": "Web Development Intern",
        "company": "WebWorks",
        "location": "Hyderabad",
        "description": "Assist in building responsive web applications.",
        "responsibilities": "Develop frontend pages and integrate APIs.",
        "required": "HTML CSS JavaScript",
        "preferred": "React Node.js",
        "qualification": "Web development fundamentals",
        "education": "Bachelor's degree"
    },
    {
        "title": "Data Analyst Intern",
        "company": "InsightLabs",
        "location": "Chennai",
        "description": "Analyze datasets and create useful reports for business decisions.",
        "responsibilities": "Clean data, perform analysis and prepare dashboards.",
        "required": "Python SQL Excel",
        "preferred": "Power BI Tableau",
        "qualification": "Data analysis fundamentals",
        "education": "Bachelor's in Computer Science or Data Science"
    },
    {
        "title": "AI Intern",
        "company": "FutureAI",
        "location": "Bengaluru",
        "description": "Assist with artificial intelligence research and development.",
        "responsibilities": "Build AI prototypes and evaluate machine learning models.",
        "required": "Python Machine Learning Deep Learning",
        "preferred": "PyTorch TensorFlow",
        "qualification": "Artificial intelligence fundamentals",
        "education": "Bachelor's in AI ML or Computer Science"
    },
    {
        "title": "Java Developer Intern",
        "company": "CodeCraft",
        "location": "Pune",
        "description": "Assist with Java application development and software testing.",
        "responsibilities": "Develop Java applications, fix bugs and write test cases.",
        "required": "Java SQL Git",
        "preferred": "Spring Boot",
        "qualification": "Object oriented programming",
        "education": "Bachelor's in Computer Science"
    },
    {
        "title": "Cloud Computing Intern",
        "company": "CloudSphere",
        "location": "Hyderabad",
        "description": "Learn and assist with cloud computing infrastructure and applications.",
        "responsibilities": "Deploy applications and assist with cloud infrastructure management.",
        "required": "Python Cloud Computing",
        "preferred": "AWS Azure",
        "qualification": "Cloud computing fundamentals",
        "education": "Bachelor's degree"
    },
    {
        "title": "Cybersecurity Intern",
        "company": "SecureNet",
        "location": "Bengaluru",
        "description": "Assist the security team with cybersecurity monitoring and analysis.",
        "responsibilities": "Monitor security events and assist with vulnerability analysis.",
        "required": "Networking Python",
        "preferred": "Cybersecurity Linux",
        "qualification": "Networking fundamentals",
        "education": "Bachelor's in Computer Science"
    },
    {
        "title": "Software Testing Intern",
        "company": "QualitySoft",
        "location": "Chennai",
        "description": "Assist with software testing and quality assurance activities.",
        "responsibilities": "Create test cases, execute tests and report software defects.",
        "required": "Python SQL",
        "preferred": "Selenium Java",
        "qualification": "Software testing fundamentals",
        "education": "Bachelor's degree"
    },
    {
        "title": "Computer Vision Intern",
        "company": "VisionTech",
        "location": "Bengaluru",
        "description": "Assist with computer vision and image processing projects.",
        "responsibilities": "Process images, develop computer vision prototypes and evaluate results.",
        "required": "Python Computer Vision OpenCV",
        "preferred": "Deep Learning TensorFlow",
        "qualification": "Computer vision fundamentals",
        "education": "Bachelor's in Computer Science or AI"
    }
]


def create_jobs():

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    jobs = []

    job_id = 1

    for round_number in range(15):

        for template in JOB_TEMPLATES:

            job = {
                "job_id": f"J{job_id:03d}",
                "job_title": template["title"],
                "company": f"{template['company']}{round_number + 1}",
                "location": template["location"],
                "job_description": template["description"],
                "responsibilities": template["responsibilities"],
                "required_skills": template["required"],
                "preferred_skills": template["preferred"],
                "qualifications": template["qualification"],
                "experience": "0-1 years",
                "education": template["education"]
            }

            jobs.append(job)

            job_id += 1

    fieldnames = [
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

    with open(
        JOBS_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(jobs)

    print("======================================")
    print("JOB DATASET CREATED")
    print("======================================")
    print(f"Total jobs created: {len(jobs)}")
    print(f"File: {JOBS_FILE}")
    print("======================================")


if __name__ == "__main__":
    create_jobs()