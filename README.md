🧠 Resume Analyzer using Flask and OpenRouter API
A web-based Resume Analysis System built with Flask and powered by OpenRouter API (Google Gemma model).
It allows users to upload PDF resumes and receive detailed analyses, including quick scans, ATS compatibility checks, detailed feedback, and personalized job recommendations.
All resume data is securely stored in a SQLite database for record-keeping and future reference.

📁 Features
* Resume Upload

  * Upload PDF resumes through a simple web interface.

* Analysis Options

  * Quick Scan: Identify suitable professions, key strengths, and immediate improvement areas.

  * Detailed Analysis: Receive in-depth feedback across impact, brevity, style, structure, and skills.

  * ATS Checker: Evaluate ATS (Applicant Tracking System) compatibility and keyword relevance.

  * ATS Score Checker: Get an ATS score along with actionable improvement suggestions.

  * Personalized Job Recommendations: Suggest job roles tailored to the user's skills and experience.

* Database Storage

  * Store resume metadata (filename, upload timestamp) and extracted text in a SQLite database.

* Job Description Integration (Optional)

  * Provide a job description for more targeted resume analysis and matching.

🛠️ Technologies Used

  * Python 🐍

  * Flask

  * SQLite

  * PyPDF2

  * OpenRouter API (Google Gemma Model)

  * Requests

  * HTML/CSS (Basic Frontend)

🔄 Pipeline Overview

1. Resume Upload

  * Users upload their PDF resumes via the web interface.

  * Optionally, a job description can be provided for a customized analysis.

2. PDF Processing

  * Extracts text content from uploaded PDFs using PyPDF2.

  * Validates the extracted text to ensure there’s enough content to analyze.

3. Database Storage

  * Saves resume metadata (filename, timestamp) and extracted text into a SQLite database.

4. Analysis via OpenRouter API

  * Sends the extracted resume text (and optional job description) to the OpenRouter API using different prompts.

  * Processes and displays the analysis results to the user.


    ![Screenshot 2025-04-26 215223](https://github.com/user-attachments/assets/d5c7e2d9-a2b0-42e9-a561-3f005bb574a0)


