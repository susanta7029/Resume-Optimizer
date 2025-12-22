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
    You are an ATS system. Analyze this resume against the job description and extract structured data.

    Job Description:
    {job_description}

    Resume:
    {resume_text}

    Extract and return ONLY valid JSON with:
    {{
        "required_skills_in_job": ["skill1", "skill2", ...],
        "skills_found_in_resume": ["skill1", "skill2", ...],
        "matched_skills": ["skills present in both job and resume"],
        "missing_skills": ["skills in job but not in resume"],
        "required_experience_years": <number from job description, 0 if not specified>,
        "candidate_experience_years": <number from resume>,
        "all_resume_skills": ["all technical and soft skills from resume"],
        "project_categories": ["domains like AI, Web Dev, Cloud, Mobile, etc."],
        "has_relevant_education": <true/false>,
        "suggestions": ["3-5 specific suggestions to improve match"]
    }}
    
    Be thorough in skill extraction. Include variations (e.g., "JavaScript" and "JS" are same skill).
    """

    try:
        client = Groq(api_key=API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        result = response.choices[0].message.content
        logging.debug("LLM analysis result: %s", result)
        analysis = json.loads(result)
        
        # Calculate score programmatically based on extracted data
        score = 0
        
        # Skill matching (up to 50 points)
        matched_skills = len(analysis.get('matched_skills', []))
        required_skills = len(analysis.get('required_skills_in_job', []))
        if required_skills > 0:
            skill_percentage = (matched_skills / required_skills) * 100
            score += min(50, skill_percentage / 2)  # Max 50 points
        
        # Experience matching (up to 25 points)
        required_exp = analysis.get('required_experience_years', 0)
        candidate_exp = analysis.get('candidate_experience_years', 0)
        if required_exp > 0:
            if candidate_exp >= required_exp:
                score += 25
            elif candidate_exp >= required_exp * 0.7:
                score += 20
            elif candidate_exp >= required_exp * 0.5:
                score += 15
            elif candidate_exp >= required_exp * 0.3:
                score += 10
            else:
                score += 5
        else:
            score += 15  # Default if no experience requirement
        
        # Project categories (up to 15 points)
        project_cats = len(analysis.get('project_categories', []))
        score += min(15, project_cats * 3)
        
        # Education (up to 10 points)
        if analysis.get('has_relevant_education', False):
            score += 10
        
        # Round to integer
        score = int(round(score))
        
        # Return formatted response
        return {
            "rank": score,
            "skills": analysis.get('all_resume_skills', []),
            "total_experience": candidate_exp,
            "project_categories": analysis.get('project_categories', []),
            "suggestions": analysis.get('suggestions', [])
        }
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
