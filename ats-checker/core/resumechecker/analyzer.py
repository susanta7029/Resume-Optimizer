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
    
    # First, extract structured data from both resume and job description
    extraction_prompt = f"""
    Extract structured information from this resume and job description. Be consistent and thorough.

    Job Description:
    {job_description}

    Resume:
    {resume_text}

    Return valid JSON with:
    {{
        "job_required_skills": ["list ALL technical skills, tools, languages, frameworks mentioned in job description"],
        "job_required_experience": <minimum years required, 0 if not specified>,
        "resume_skills": ["list ALL technical skills, tools, languages, frameworks found in resume"],
        "resume_experience": <total years of experience>,
        "resume_education": "<highest degree and field>",
        "resume_projects": ["brief description of each project domain"],
        "improvement_suggestions": ["5 specific actionable suggestions"]
    }}
    
    Normalize skill names (e.g., "React.js" and "React" → "React", "JavaScript" and "JS" → "JavaScript").
    """
    
    try:
        client = Groq(api_key=API_KEY)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": extraction_prompt}],
            temperature=0,  # Completely deterministic
            max_tokens=2000,
            response_format={"type": "json_object"}
        )
        result = response.choices[0].message.content
        logging.debug("LLM extraction result: %s", result)
        data = json.loads(result)
        
        # Calculate score using deterministic algorithm
        score = calculate_ats_score(data)
        
        # Categorize projects
        project_categories = categorize_projects(data.get('resume_projects', []))
        
        return {
            "rank": score,
            "skills": data.get('resume_skills', []),
            "total_experience": data.get('resume_experience', 0),
            "project_categories": project_categories,
            "suggestions": data.get('improvement_suggestions', [])
        }
        
    except Exception as e:
        logging.error("Error during LLM analysis: %s", e)
        return {
            "rank": 0,
            "skills": [],
            "total_experience": 0,
            "project_categories": [],
            "suggestions": ["Unable to analyze resume. Please try again."]
        }

def calculate_ats_score(data: dict) -> int:
    """Calculate ATS score using deterministic algorithm like professional ATS systems"""
    score = 0
    
    job_skills = set([s.lower().strip() for s in data.get('job_required_skills', [])])
    resume_skills = set([s.lower().strip() for s in data.get('resume_skills', [])])
    
    # 1. Keyword/Skill Match (50 points maximum)
    if len(job_skills) > 0:
        matched_skills = job_skills.intersection(resume_skills)
        skill_match_rate = len(matched_skills) / len(job_skills)
        score += int(skill_match_rate * 50)
        logging.debug(f"Skill match: {len(matched_skills)}/{len(job_skills)} = {skill_match_rate:.2%} → {int(skill_match_rate * 50)} points")
    else:
        score += 25  # Default if no specific skills listed
    
    # 2. Experience Match (25 points maximum)
    required_exp = data.get('job_required_experience', 0)
    candidate_exp = data.get('resume_experience', 0)
    
    if required_exp == 0:
        score += 20  # No specific requirement
    elif candidate_exp >= required_exp:
        score += 25  # Meets or exceeds
    elif candidate_exp >= required_exp * 0.75:
        score += 20  # Close match
    elif candidate_exp >= required_exp * 0.5:
        score += 15  # Partial match
    elif candidate_exp >= required_exp * 0.25:
        score += 10  # Some experience
    else:
        score += 5  # Limited experience
    
    logging.debug(f"Experience: {candidate_exp}/{required_exp} years → {25 if candidate_exp >= required_exp else 20} points")
    
    # 3. Project Diversity (15 points maximum)
    projects = data.get('resume_projects', [])
    num_projects = len(projects)
    if num_projects >= 5:
        score += 15
    elif num_projects >= 3:
        score += 12
    elif num_projects >= 2:
        score += 9
    elif num_projects >= 1:
        score += 6
    
    # 4. Education (10 points maximum)
    education = data.get('resume_education', '').lower()
    if any(degree in education for degree in ['phd', 'doctorate', 'ph.d']):
        score += 10
    elif any(degree in education for degree in ['master', 'msc', 'mba', 'ms']):
        score += 9
    elif any(degree in education for degree in ['bachelor', 'bsc', 'ba', 'bs', 'btech', 'be']):
        score += 7
    elif education:
        score += 5
    
    # Cap at 100
    final_score = min(100, score)
    logging.debug(f"Final ATS Score: {final_score}/100")
    
    return final_score

def categorize_projects(projects: list) -> list:
    """Categorize projects into domains"""
    categories = set()
    keywords_map = {
        'AI/ML': ['ai', 'ml', 'machine learning', 'deep learning', 'neural', 'nlp', 'computer vision', 'tensorflow', 'pytorch'],
        'Web Development': ['web', 'website', 'frontend', 'backend', 'react', 'angular', 'vue', 'django', 'flask', 'node'],
        'Mobile': ['mobile', 'android', 'ios', 'app', 'flutter', 'react native'],
        'Cloud': ['cloud', 'aws', 'azure', 'gcp', 'kubernetes', 'docker'],
        'Data Science': ['data', 'analytics', 'visualization', 'pandas', 'numpy', 'sql', 'database'],
        'DevOps': ['devops', 'ci/cd', 'jenkins', 'deployment', 'infrastructure']
    }
    
    for project in projects:
        project_lower = project.lower()
        for category, keywords in keywords_map.items():
            if any(keyword in project_lower for keyword in keywords):
                categories.add(category)
    
    return list(categories) if categories else ['General Software Development']

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
