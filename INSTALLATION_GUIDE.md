# Installation Guide — AI Career Companion

## 1. Prerequisites

Before running the project, ensure that you have:

- Python installed.
- Git installed if you want to clone the repository.
- An internet connection for installing dependencies.

## 2. Download the Project

Clone the repository using:

```bash
git clone https://github.com/nagalakshmi-mp/AI-career-companion_project.git
cd AI-career-companion_project
```

Alternatively, download the repository as a ZIP file from GitHub and extract it.

## 3. Install Dependencies

Open a terminal in the project folder and run:

```bash
python -m pip install -r requirements.txt
```

## 4. Run the Application

Start the Streamlit application using:

```bash
python -m streamlit run app.py
```

Streamlit will display a local URL in the terminal. Open that URL in your browser.

## 5. Troubleshooting

- **Missing packages:** Run the dependency installation command again.
- **Database errors:** Check the database configuration and confirm that the required directory exists.
- **Application startup errors:** Review the terminal output for the specific error message.
- **Job data issues:** Confirm that `data/jobs.csv` is present in the expected location.

## 6. Notes

The exact setup requirements may depend on the current source code and environment. Verify the application locally before considering the installation process complete.
