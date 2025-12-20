import os
import sys
sys.path.insert(0, r'C:\Users\susan\Desktop\Resume-Analyzer\ats-checker\core')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from dotenv import load_dotenv
load_dotenv(r'C:\Users\susan\Desktop\Resume-Analyzer\ats-checker\core\.env')

from groq import Groq

# Test if API key is loaded
api_key = os.getenv('GROQ_API_KEY')
print(f"API Key loaded: {api_key[:20]}..." if api_key else "NO API KEY!")

# Test Groq API
try:
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": "Say 'Hello, API is working!'"}],
        temperature=0.7
    )
    print("API Response:", response.choices[0].message.content)
    print("✅ Groq API is working!")
except Exception as e:
    print(f"❌ Error: {e}")
