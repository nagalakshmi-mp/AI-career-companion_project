# Agile Development Methodology

## 1. Overview

The AI Career Companion project was developed using an iterative and incremental development approach inspired by Agile software development principles. The project was divided into four milestones to organize the work into manageable stages, implement features progressively, validate functionality, and improve the application as development progressed.

Instead of developing the entire application at once, individual modules were built and integrated step by step. This approach helped organize requirements, identify implementation issues, and maintain project documentation throughout development.

## 2. Objectives of the Agile Approach

The main objectives of applying an Agile-inspired approach were:

- Divide the project into manageable milestones.
- Develop and integrate features incrementally.
- Validate functionality during development.
- Improve the application based on identified issues and feedback.
- Maintain clear documentation of project features and progress.
- Keep the implementation aligned with the needs of students and internship seekers.

## 3. Development Workflow

The project followed the following general development workflow:

1. **Requirement Analysis:** Identify the career preparation problems faced by students and define the required application features.
2. **Planning:** Divide the work into four milestones and identify the major deliverables for each stage.
3. **Design:** Plan the application structure, data flow, storage, and interaction between modules.
4. **Implementation:** Develop the required features using Python, Streamlit, and supporting libraries.
5. **Integration:** Connect the modules so that candidate profiles, job information, career assistance, and application records can work together.
6. **Testing and Validation:** Check implemented features, identify issues, and make corrections where required.
7. **Documentation and Deployment:** Maintain project documentation and prepare the application for demonstration and deployment.

## 4. Milestone-Based Development

### Milestone 1 — Resume and Candidate Profile Management

**Objective:** Establish the foundation of the AI Career Companion application.

**Major activities:**
- Set up the Python and Streamlit application structure.
- Implement resume upload and text extraction.
- Develop candidate profile management.
- Extract and organize available candidate information.
- Establish database storage for relevant profile information.

**Expected outcome:** A foundation for collecting resume information and maintaining structured candidate profiles.

### Milestone 2 — Job Knowledge Base and Matching

**Objective:** Help candidates discover internship and job opportunities relevant to their profiles.

**Major activities:**
- Prepare a CSV-based job and internship dataset.
- Process job information for retrieval and matching.
- Develop semantic retrieval using Sentence Transformers and ChromaDB where configured.
- Compare candidate skills and profile information with job requirements.
- Develop job matching and skill-gap identification functionality.

**Expected outcome:** A job discovery workflow that helps candidates explore relevant opportunities and identify skills they may need to improve.

### Milestone 3 — Career Guidance and Preparation Tools

**Objective:** Provide additional support for internship applications and interview preparation.

**Major activities:**
- Develop resume assistance functionality.
- Implement job-focused cover letter preparation.
- Provide interview preparation support.
- Develop career guidance through the Career Assistant.
- Connect these features with relevant candidate and job information.

**Expected outcome:** A collection of career preparation tools that supports candidates beyond job discovery.

### Milestone 4 — Application Tracking and Project Validation

**Objective:** Help candidates organize applications and prepare the complete application for demonstration.

**Major activities:**
- Develop application tracking functionality.
- Manage application statuses, deadlines, interview details, and notes.
- Integrate the tracker with the other application modules where supported.
- Validate important workflows and resolve identified issues.
- Improve documentation and prepare the project for demonstration or deployment.

**Expected outcome:** A more complete career assistance application with application management and supporting project documentation.

## 5. Continuous Improvement

An important part of the development approach was improving the application as additional modules were introduced. Issues identified during implementation and validation could be addressed before proceeding with further improvements.

The milestone structure also made it easier to organize code, maintain documentation, and review the progress of individual features.

## 6. Testing and Validation

Testing and validation are important parts of the development lifecycle. Relevant checks for this project include:

- Resume upload and text extraction.
- Candidate profile creation and retrieval.
- Job retrieval and matching.
- Skill-gap identification.
- Resume and cover letter assistance.
- Interview preparation and career guidance.
- Application creation, viewing, updating, and deletion.
- Integration between application modules.
- Application startup and deployment checks.

The results of these checks should be recorded separately in a test report. Only tests that have actually been performed should be marked as passed.

## 7. Benefits of the Approach

The milestone-based Agile-inspired approach provides the following benefits:

- **Manageability:** Complex functionality is divided into smaller development stages.
- **Incremental delivery:** Useful modules can be developed and integrated progressively.
- **Maintainability:** A modular project structure helps organize and update the code.
- **Early issue identification:** Testing during development can reveal problems before final delivery.
- **Traceability:** Milestones help connect project objectives with implemented features.
- **Documentation:** Each development stage can be documented to support future maintenance and evaluation.

## 8. Conclusion

The AI Career Companion project uses a milestone-based, iterative development approach inspired by Agile principles. The four milestones cover resume and profile management, job discovery and matching, career preparation tools, and application tracking with project validation.

This approach provides a structured way to develop, integrate, validate, and document the application progressively. The methodology can continue to support future improvements, including expanded job datasets, enhanced matching, improved testing, and additional career assistance features.
