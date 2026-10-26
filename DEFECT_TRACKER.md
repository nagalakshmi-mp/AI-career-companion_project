# Defect Tracker — AI Career Companion

## 1. Purpose

This document records known issues that require investigation or verification in the AI Career Companion project.

## 2. Defect Log

| Defect ID | Description | Severity | Status |
|---|---|---|---|
| BUG-001 | Streamlit Cloud previously reported a SQLite OperationalError during database initialization. | High | Requires verification |
| BUG-002 | A mismatch was previously observed between the dashboard application summary and the Application Tracker records. | Medium | Requires verification |

## 3. Investigation and Resolution

### BUG-001: Database Initialization

**Issue:** The deployed application previously reported an SQLite OperationalError while initializing the database.

**Action required:** Verify the database path, ensure the required directory exists, and check database initialization in the deployed environment.

**Resolution:** Not yet verified.

### BUG-002: Application Tracker Mismatch

**Issue:** The dashboard summary and Application Tracker previously displayed inconsistent application information.

**Action required:** Compare the dashboard counts with the records displayed in the tracker.

**Resolution:** Not yet verified.

## 4. Defect Management Process

1. Reproduce the issue.
2. Record the observed behavior.
3. Identify the cause.
4. Apply a fix.
5. Retest the affected feature.
6. Update the defect status only after verification.

## 5. Notes

The issues listed above were reported previously. Their current status must be confirmed by testing the application. No issue should be marked as resolved without verification.
