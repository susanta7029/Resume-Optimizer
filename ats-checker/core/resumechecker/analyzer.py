import pdfplumber
import spacy
from groq import Groq
import json
import logging
import os


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def extraxt_text_from_pdf(pdf_path):
    text="" 
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

# Load API key from environment variable for security
API_KEY = os.getenv('GROQ_API_KEY')
if not API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set. Please set it in your environment or .env file.")

def analyze_resume_with_llm(resume_text: str, job_description: str) -> dict:
    logging.debug("Starting analysis with LLM")
    prompt = f"""
    You are an expert ATS (Applicant Tracking System) and recruitment specialist. Analyze this resume against the job description with precision.

    RANKING CRITERIA (0-100):
    - 90-100: Exceptional match - most required skills, extensive relevant experience, perfect alignment
    - 75-89: Strong match - many required skills, good experience, strong alignment  
    - 60-74: Good match - some required skills, adequate experience, reasonable fit
    - 40-59: Fair match - few required skills, limited experience, partial fit
    - 0-39: Poor match - minimal required skills, little relevant experience

    IMPORTANT: Be critical and realistic. Most resumes should score between 40-85. Only truly exceptional matches deserve 90+.

    TASKS:
    1. Extract ALL technical and soft skills mentioned (be comprehensive)
    2. Calculate total years of professional experience (sum all work experience)
    3. Identify project domains/categories (e.g., AI/ML, Web Development, Cloud, Mobile, DevOps, Data Science, etc.)
    4. Calculate REALISTIC match score based on:
       - How many required skills from job description are present
       - Relevance of experience to the role
       - Project alignment with job requirements
       - Overall candidate fit
    5. Provide 3-5 SPECIFIC, actionable suggestions to improve match for THIS job

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Return ONLY valid JSON (no markdown, no extra text):
    {{
        "rank": <number between 0-100>,
        "skills": ["skill1", "skill2", ...],
        "total_experience": <years as integer or float>,
        "project_categories": ["category1", "category2", ...],
        "suggestions": ["suggestion1", "suggestion2", ...]
    }}
    """

    try:
        client = Groq(api_key=API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,  # Lower temperature for more consistent, analytical responses
            response_format={"type": "json_object"}
        )
        result = response.choices[0].message.content
        logging.debug("LLM analysis result: %s", result)
        return json.loads(result)
    except Exception as e:
        logging.error("Error during LLM analysis: %s", e)
        return {
            "rank": 0,
            "skills": [],
            "total_experience": 0,
            "project_categories": [],
            "suggestions": ["Unable to generate suggestions due to an error. Please try again."]
        }  # Return a default structure in case of failure

def process_resume(pdf_path, job_description):
    try:
        logging.debug("Extracting text from PDF: %s", pdf_path)
        resume_text = extraxt_text_from_pdf(pdf_path)
        logging.debug("Extracted resume text: %s", resume_text[:500])  # Log first 500 characters
        analysis_result = analyze_resume_with_llm(resume_text, job_description)
        if analysis_result is None:
            logging.error("Analysis result is None. Check LLM function.")
        else:
            logging.debug("Analysis result: %s", analysis_result)
        return analysis_result
    except Exception as e:
        logging.error("Error during resume processing: %s", e)
        return {
            "rank": 0,
            "skills": [],
            "total_experience": 0,
            "project_categories": [],
            "suggestions": ["Error processing resume. Please ensure your PDF is readable and try again."]
        }  # Return a default structure in case of failure
