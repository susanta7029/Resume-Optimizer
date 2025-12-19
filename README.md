# Resume Analyzer - Full Stack Application

An AI-powered Resume Analyzer that uses Groq LLM to analyze resumes against job descriptions and provide detailed feedback.

## 🎯 Features

- Upload PDF resumes
- Analyze against specific job descriptions
- AI-powered skill extraction
- Match score calculation (0-100%)
- Experience level detection
- Project categorization
- Modern, responsive UI

## 🏗️ Architecture

- **Backend:** Django REST Framework
- **Frontend:** React.js
- **AI:** Groq API (LLM)
- **Database:** SQLite
- **PDF Processing:** pdfplumber

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- pip
- npm

## 🚀 Quick Start

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd ats-checker/core
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows
   python -m venv myenv
   myenv\Scripts\activate

   # Linux/Mac
   python3 -m venv myenv
   source myenv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r ../../requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the server:**
   ```bash
   python manage.py runserver
   ```

   Backend will run at: `http://127.0.0.1:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

   Frontend will run at: `http://localhost:3000`

## 📝 API Endpoints

### Get Job Descriptions
```
GET /api/jobs/
```

### Analyze Resume
```
POST /api/resume/
Content-Type: multipart/form-data

Parameters:
- job_description: <job_id>
- resume: <pdf_file>
```

## 🎨 Usage

1. Open `http://localhost:3000` in your browser
2. Select a job position from the dropdown
3. Upload your resume (PDF only)
4. Click "Analyze Resume"
5. View your results:
   - Match Score
   - Identified Skills
   - Total Experience
   - Project Categories

## 🔧 Configuration

### Environment Variables

Create a `.env` file in `ats-checker/core/`:

```env
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=your_django_secret_key
DEBUG=True
```

### CORS Settings

The backend is configured to accept requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`

## 📁 Project Structure

```
Resume-Analyzer/
├── ats-checker/
│   ├── core/
│   │   ├── manage.py
│   │   ├── core/
│   │   │   ├── settings.py
│   │   │   └── urls.py
│   │   ├── resumechecker/
│   │   │   ├── models.py
│   │   │   ├── views.py
│   │   │   ├── serializer.py
│   │   │   └── analyzer.py
│   │   └── media/
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── services/
│   │       └── api.js
│   └── package.json
└── myenv/
```

## 🐛 Troubleshooting

### Backend Issues

**Module not found:**
```bash
pip install -r requirements.txt
```

**Database errors:**
```bash
python manage.py migrate
```

### Frontend Issues

**Dependencies error:**
```bash
npm install
```

**CORS error:**
- Ensure django-cors-headers is installed
- Check CORS_ALLOWED_ORIGINS in settings.py

## 🔒 Security Notes

- The Groq API key is currently hardcoded with a fallback. For production, use environment variables only.
- DEBUG should be False in production
- Change SECRET_KEY in production

## 📦 Tech Stack

**Backend:**
- Django 5.2.6
- Django REST Framework 3.16.1
- pdfplumber 0.11.8
- Groq 0.31.1
- django-cors-headers 4.6.0

**Frontend:**
- React 18.2.0
- Axios 1.6.0

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Susanta Gope
- GitHub: [@susanta7029](https://github.com/susanta7029)
- LinkedIn: [susantagope28](https://linkedin.com/in/susantagope28)

## 🙏 Acknowledgments

- Groq for providing the LLM API
- Django & React communities
