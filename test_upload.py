import requests
import os

# Test the resume analysis API
url = 'http://127.0.0.1:8000/api/resume/'
resume_path = r'C:\Users\susan\Desktop\Resume-Analyzer\ats-checker\core\resume\Susanta_Data_Science_CV_2026_02.pdf'

if os.path.exists(resume_path):
    with open(resume_path, 'rb') as f:
        files = {'resume': f}
        data = {'job_description': '1'}
        
        print("Sending request to API...")
        response = requests.post(url, files=files, data=data)
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response: {response.json()}")
else:
    print(f"Resume file not found at: {resume_path}")
    print("\nAvailable resumes:")
    resume_dir = os.path.dirname(resume_path)
    if os.path.exists(resume_dir):
        for file in os.listdir(resume_dir):
            if file.endswith('.pdf'):
                print(f"  - {file}")
