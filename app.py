from flask import Flask, render_template, request, jsonify
import os
import requests
import json
import sqlite3
from datetime import datetime
from PyPDF2 import PdfReader

app = Flask(__name__)

# OpenRouter API Key
api_key = "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"

if not api_key:
    raise ValueError("OpenRouter API key is missing. Please check your configuration.")

# Database setup
def init_db():
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            uploaded_at TEXT,
            resume_text TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Function to store resume in the database
def save_resume(filename, resume_text):
    conn = sqlite3.connect("resumes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO resumes (filename, uploaded_at, resume_text) VALUES (?, ?, ?)", 
                   (filename, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), resume_text))
    conn.commit()
    conn.close()

# Function to get OpenRouter Gemini output
def get_gemini_output(pdf_text, prompt):
    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": "google/gemma-3-27b-it:free",
                "messages": [
                    {"role": "user", "content": pdf_text + "\n" + prompt}
                ],
            })
        )
        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "Error: No response from API")
    except Exception as e:
        return f"Error: {str(e)}"

# Function to read PDFs safely
def read_pdf(uploaded_file):
    try:
        pdf_reader = PdfReader(uploaded_file)
        pdf_text = "".join([page.extract_text() or "" for page in pdf_reader.pages])
        if not pdf_text.strip():
            return "Error: No extractable text found in PDF. Try using a text-based resume."
        return pdf_text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    uploaded_file = request.files['resume']
    job_description = request.form.get('job_description', '')
    analysis_option = request.form.get('analysis_option', 'Quick Scan')
    
    pdf_text = read_pdf(uploaded_file)
    
    if "Error" in pdf_text:
        return jsonify({'error': pdf_text}), 400

    # Save resume to database
    save_resume(uploaded_file.filename, pdf_text)

    # Prompt selection based on user input
    prompt_dict = {
        "Quick Scan": f"""
        You are ResumeChecker, an expert in resume analysis. Provide a quick scan:
        1. Identify the most suitable profession.
        2. List 3 key strengths.
        3. Suggest 2 quick improvements.
        
        
        Resume text: {pdf_text}
        Job description: {job_description}
        """,
        "Detailed Analysis": f"""
        You are ResumeChecker, an expert in resume analysis. Provide a detailed analysis:
        1. Identify the most suitable profession.
        2. List 5 strengths.
        3. Suggest 3-5 improvements with recommendations.
        4. Rate (out of 10): Impact, Brevity, Style, Structure, Skills.
        5. Review sections (Summary, Experience, Education).
        6. Give an ATS score out of 100 with a breakdown.
        
        Resume text: {pdf_text}
        Job description: {job_description}
        """,
        "Personalized Job Recommendations": f"""
        You are an intelligent job recommendation assistant.
        Based on a user's resume, skills, experience, interests, and location preferences, suggest the top matching job roles.
        Always provide the job title, a short description, required skills, and why this job is a good match for the user.
        Focus on recommending roles that align closely with their profile, growth potential, and personal goals.
        
        Resume text: {pdf_text}
        Job description: {job_description}
        """,
        "ATS Checker": f"""
        You are an ATS Compliance Checker. Evaluate how well the resume matches the job description.
        
        1. Extract keywords from the job description.
        2. Compare with the resume and identify missing important keywords.
        3. Check for ATS-friendly formatting issues (e.g., headings, font readability).
        4. Provide a match percentage out of 100%.
        5. Suggest 3-5 improvements to increase the ATS score.
        
        Resume text: {pdf_text}
        Job description: {job_description}
        """,
        "ATS Score Checker": f"""
        You are an ATS Score Checker. Analyze the resume and assign an ATS score out of 100 based on keyword relevance, formatting, and structure.
        
        1. Assign an ATS score out of 100 and provide a breakdown of the score.
        2. Offer 3-5 key suggestions for improving the ATS score.
        
        Resume text: {pdf_text}
        Job description: {job_description}
        """
    }

    prompt = prompt_dict.get(analysis_option, prompt_dict["Quick Scan"])
    
    response = get_gemini_output(pdf_text, prompt)
    
    return jsonify({'analysis': response})

if __name__ == '__main__':
    app.run(debug=True)
