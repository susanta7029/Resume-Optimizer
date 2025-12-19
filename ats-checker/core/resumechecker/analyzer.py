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
    you are an ai assistant that analyzes resumes for a software job application.
    Given a resume and a job description, extract the following details:

    1. Identify all skills mentioned in the resume
    2. Calculate the total years of experience
    3. Categorize the projects based on the domain (e.g., AI, Web development, Cloud, etc.)
    4. Rank the resume relevance to the job description on a scale of 0 to 100.
    5. Provide 3-5 specific, actionable suggestions to improve the resume for this job

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Provide the output in a JSON format with the following structure:
    {{
        "rank": <percentage>,
        "skills": ["skill1", "skill2", ...],
        "total_experience": <years>,
        "project_categories": ["category1", "category2", ...],
        "suggestions": ["suggestion1", "suggestion2", ...]
    }}
    """

    try:
        client = Groq(api_key=API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],  # Corrected 'message' to 'messages'
            temperature=0.7,
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
