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
    You are an expert ATS (Applicant Tracking System) evaluator. Your job is to CRITICALLY analyze how well this specific resume matches this specific job description.

    STEP 1: Extract key requirements from job description
    - List all required technical skills
    - List required years of experience
    - List required domains/technologies
    
    STEP 2: Analyze resume against requirements
    - Count how many required skills are actually present in resume
    - Compare experience level to requirements
    - Check domain/technology alignment
    
    STEP 3: Calculate match score (0-100) using this formula:
    - Start with 0
    - Add 3 points for EACH required skill found in resume
    - Add 10 points if experience meets minimum requirements
    - Add 5 points for each matching domain/technology area
    - Add 10 points if candidate has relevant certifications or education
    - Subtract 10 points if missing critical required skills
    - Subtract 5 points if experience is significantly below requirements
    
    IMPORTANT: Each resume will score DIFFERENTLY based on actual content. Do NOT give similar scores to different resumes.
    
    Example scoring:
    - Junior candidate (1-2 years) applying for senior role (5+ years): 30-50 points
    - Mid-level candidate (3-4 years) with some skills match: 55-70 points  
    - Strong candidate with most skills and good experience: 75-85 points
    - Perfect match with all skills and experience: 90-100 points

    Job Description:
    {job_description}

    Resume:
    {resume_text}

    Now analyze and return ONLY valid JSON:
    {{
        "rank": <calculated score 0-100 based on actual match>,
        "skills": ["list ALL skills from resume"],
        "total_experience": <total years as number>,
        "project_categories": ["all project domains/categories"],
        "suggestions": ["3-5 specific suggestions based on gaps found"]
    }}
    """

    try:
        client = Groq(api_key=API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,  # Very low for analytical, deterministic responses
            max_tokens=2000,  # Ensure detailed analysis
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
