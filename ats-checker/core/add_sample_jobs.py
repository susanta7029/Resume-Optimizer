import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from resumechecker.models import JobDesCription

# Sample job descriptions
jobs_data = [
    {
        'job_title': 'Senior Python Developer',
        'job_description': '''About the job
Responsibilities

Requisition Description

Design, develop, and maintain Python-based applications for handling large datasets and ensuring high performance.
Optimize and refactor existing code to improve scalability, processing speed, and efficiency.
Collaborate with the data engineering team to integrate data sources, transform and clean data for analysis.
Utilize multithreading, parallel processing, and asynchronous programming to ensure optimized handling of large data volumes.
Implement robust data pipelines using ETL processes for smooth data ingestion and transformation.
Work with the latest Python libraries and frameworks such as Pandas, NumPy, Polars etc. to streamline data processing tasks.
Ensure code quality through unit testing, code reviews, and continuous integration.
Stay updated with the latest developments in Python and related tools, suggesting improvements to the tech stack.


Key Skills & Qualifications

5-6 years of experience in Python development, with a focus on data-intensive applications.
Strong understanding of Python's core libraries and frameworks for data manipulation (e.g., Pandas, NumPy, Dask, PySpark).
Experience with database systems like SQL, NoSQL databases like Cassandra, PostgreSQL.
Hands-on experience in asynchronous programming, multithreading, and parallel computing.
Proficiency in writing optimized code for high-performance data processing.
Experience with data pipelines, ETL processes, and API integration.
Excellent problem-solving skills with a strong understanding of algorithms and data structures.
Knowledge of version control systems like Git.'''
    },
    {
        'job_title': 'Full Stack Developer (React + Django)',
        'job_description': '''We are looking for a talented Full Stack Developer to join our team!

Responsibilities:
- Develop and maintain web applications using React.js and Django
- Build responsive user interfaces with modern CSS frameworks
- Design and implement RESTful APIs
- Work with PostgreSQL/MySQL databases
- Implement authentication and authorization
- Write clean, maintainable code with proper documentation
- Collaborate with cross-functional teams

Requirements:
- 3+ years of experience with React.js and Django
- Strong knowledge of JavaScript, Python, HTML, CSS
- Experience with REST APIs and JWT authentication
- Familiarity with Git version control
- Understanding of responsive design principles
- Experience with Axios or similar HTTP clients
- Knowledge of state management (Redux, Context API)
- Bachelor's degree in Computer Science or related field'''
    },
    {
        'job_title': 'Machine Learning Engineer',
        'job_description': '''Join our AI team as a Machine Learning Engineer!

Key Responsibilities:
- Design and implement machine learning models for production
- Work with large datasets for training and evaluation
- Deploy ML models using cloud platforms (AWS, Azure, GCP)
- Optimize model performance and accuracy
- Collaborate with data scientists and engineers
- Implement MLOps best practices
- Create data pipelines for model training

Required Skills:
- 3-5 years of ML/AI experience
- Proficiency in Python, TensorFlow, PyTorch, Scikit-learn
- Experience with Pandas, NumPy, Matplotlib, Seaborn
- Knowledge of supervised and unsupervised learning algorithms
- Familiarity with Docker and Kubernetes
- Experience with cloud ML services
- Strong mathematical and statistical background
- Master's degree in CS, Statistics, or related field preferred'''
    },
    {
        'job_title': 'Data Analyst',
        'job_description': '''We're hiring a Data Analyst to help drive business decisions!

Responsibilities:
- Analyze complex datasets to identify trends and insights
- Create dashboards and visualizations using Tableau/Power BI
- Write SQL queries for data extraction and analysis
- Perform exploratory data analysis (EDA)
- Collaborate with stakeholders to understand requirements
- Present findings to non-technical audiences
- Automate reporting processes

Qualifications:
- 2+ years of data analysis experience
- Expert in SQL and Excel
- Experience with Tableau or Power BI
- Knowledge of Python (Pandas, NumPy) is a plus
- Strong statistical analysis skills
- Excellent communication and presentation skills
- Bachelor's degree in relevant field
- Experience in e-commerce or finance is preferred'''
    }
]

# Add jobs to database
print("Adding sample job descriptions...")
for job_data in jobs_data:
    job, created = JobDesCription.objects.get_or_create(
        job_title=job_data['job_title'],
        defaults={'job_description': job_data['job_description']}
    )
    if created:
        print(f"✓ Added: {job.job_title}")
    else:
        print(f"- Already exists: {job.job_title}")

print(f"\nTotal job positions: {JobDesCription.objects.count()}")
print("Done!")
