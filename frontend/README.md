# Resume Analyzer - Frontend

A modern React-based frontend for the AI-powered Resume Analyzer application.

## Features

- 🎯 Select from available job positions
- 📄 Upload resume in PDF format
- 🤖 AI-powered analysis using Groq LLM
- 📊 Visual display of match score, skills, and experience
- 🎨 Modern, responsive UI with smooth animations

## Prerequisites

Before you begin, ensure you have:
- Node.js (v14 or higher) installed
- npm (comes with Node.js)
- Backend server running on `http://127.0.0.1:8000`

## Installation

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

## Running the Application

1. **Make sure the Django backend is running:**
   ```bash
   # In the backend directory (ats-checker/core)
   python manage.py runserver
   ```

2. **Start the React development server:**
   ```bash
   npm start
   ```

3. **Open your browser:**
   - The app will automatically open at `http://localhost:3000`
   - If it doesn't, manually navigate to `http://localhost:3000`

## How to Use

1. **Select Job Position:**
   - Choose from the dropdown menu of available positions

2. **Upload Resume:**
   - Click on the upload area to select your PDF resume
   - Only PDF files are accepted

3. **Analyze:**
   - Click the "Analyze Resume" button
   - Wait for the AI to process your resume

4. **View Results:**
   - See your match score (0-100%)
   - Review identified skills
   - Check total experience
   - See project categories

5. **Analyze Another:**
   - Click "Analyze Another Resume" to start over

## Tech Stack

- **React 18** - UI library
- **Axios** - HTTP client for API calls
- **CSS3** - Styling with gradients and animations

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── services/
│   │   └── api.js          # API service for backend communication
│   ├── App.js              # Main application component
│   ├── App.css             # Application styles
│   ├── index.js            # Entry point
│   └── index.css           # Global styles
└── package.json            # Dependencies and scripts
```

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Runs the test suite
- `npm eject` - Ejects from Create React App (⚠️ irreversible)

## Troubleshooting

### CORS Errors
If you see CORS errors in the console:
- Ensure the Django backend has `django-cors-headers` installed
- Check that `http://localhost:3000` is in `CORS_ALLOWED_ORIGINS` in Django settings

### API Connection Issues
- Verify the backend server is running on `http://127.0.0.1:8000`
- Check the API base URL in `src/services/api.js`

### PDF Upload Fails
- Ensure your file is in PDF format
- Check file size (very large files may timeout)

## Contributing

Feel free to fork this project and submit pull requests for any improvements!

## License

This project is part of the Resume Analyzer system.
