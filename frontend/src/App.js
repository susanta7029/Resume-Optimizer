import React, { useState, useEffect } from 'react';
import { apiService } from './services/api';
import './App.css';

function App() {
  const [jobs, setJobs] = useState([]);
  const [selectedJob, setSelectedJob] = useState('');
  const [resumeFile, setResumeFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');
  const [toast, setToast] = useState({ show: false, message: '', type: '' });
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);

  useEffect(() => {
    fetchJobs();
  }, []);

  useEffect(() => {
    if (toast.show) {
      const timer = setTimeout(() => {
        setToast({ show: false, message: '', type: '' });
      }, 4000);
      return () => clearTimeout(timer);
    }
  }, [toast.show]);

  const showToast = (message, type = 'info') => {
    setToast({ show: true, message, type });
  };

  const fetchJobs = async () => {
    try {
      const data = await apiService.getJobs();
      const jobsArray = Array.isArray(data) ? data : [];
      setJobs(jobsArray);
      if (jobsArray.length === 0) {
        showToast('No job positions available', 'warning');
      }
    } catch (err) {
      setJobs([]);
      setError('Failed to load jobs');
      showToast('Failed to connect to backend', 'error');
    }
  };

  const fetchHistory = async () => {
    try {
      const data = await apiService.getHistory();
      const historyArray = Array.isArray(data) ? data : [];
      setHistory(historyArray);
      showToast(`Loaded ${historyArray.length} past analyses`, 'success');
    } catch (err) {
      setHistory([]);
      showToast('Failed to load history', 'error');
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && file.type === 'application/pdf') {
      setResumeFile(file);
      setError('');
      showToast(`${file.name} selected`, 'success');
    } else {
      setError('Please select a PDF file');
      setResumeFile(null);
      showToast('Invalid file type', 'error');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!resumeFile) {
      setError('Please upload your resume');
      showToast('Please select a resume file', 'warning');
      return;
    }
    
    if (!selectedJob) {
      setError('Please select a job position');
      showToast('Please select a job position', 'warning');
      return;
    }

    setLoading(true);
    setError('');
    showToast('Analyzing your resume...', 'info');

    try {
      const data = await apiService.analyzeResume(selectedJob, resumeFile);
      setResults(data);
      showToast('Resume analyzed successfully!', 'success');
    } catch (err) {
      setError('Failed to analyze resume');
      showToast('Error analyzing resume', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResumeFile(null);
    setSelectedJob('');
    setResults(null);
    setError('');
    showToast('Ready for new analysis', 'info');
  };

  const downloadReport = () => {
    if (!results) return;
    
    showToast('Generating report...', 'info');
    
    const reportContent = `
RESUME ANALYSIS REPORT
======================

Match Score: ${results.rank}%
Status: ${results.rank >= 80 ? 'Excellent Match!' : results.rank >= 60 ? 'Good Match' : 'Needs Improvement'}

TOTAL EXPERIENCE: ${results.total_experience} years

SKILLS IDENTIFIED (${results.skills.length}):
${results.skills.map(skill => ` ${skill}`).join('\n')}

PROJECT CATEGORIES:
${results.project_categories.map(cat => ` ${cat}`).join('\n')}

${results.suggestions ? `\nSUGGESTIONS FOR IMPROVEMENT:\n${results.suggestions.map((s, i) => `${i + 1}. ${s}`).join('\n')}` : ''}

Report generated on: ${new Date().toLocaleString()}
`;

    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `Resume_Analysis_Report_${Date.now()}.txt`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
    
    showToast('Report downloaded!', 'success');
  };

  const toggleHistory = () => {
    if (!showHistory) {
      fetchHistory();
    }
    setShowHistory(!showHistory);
  };

  return (
    <div className="app-container">
      {toast.show && (
        <div className={`toast toast-${toast.type}`}>
          {toast.message}
        </div>
      )}

      <header className="app-header">
        <h1> ATS Resume Analyzer</h1>
        <p>Analyze your resume against job descriptions using AI</p>
      </header>

      <div className="main-content">
        <div className="analyzer-section">
          <form onSubmit={handleSubmit} className="upload-form">
            <div className="form-group">
              <label htmlFor="resume-upload"> Upload Your Resume (PDF)</label>
              <input
                type="file"
                id="resume-upload"
                accept=".pdf"
                onChange={handleFileChange}
                disabled={loading}
              />
              {resumeFile && (
                <p className="file-info">Selected: {resumeFile.name}</p>
              )}
            </div>

            <div className="form-group">
              <label htmlFor="job-select"> Select Job Position</label>
              <select
                id="job-select"
                value={selectedJob}
                onChange={(e) => setSelectedJob(e.target.value)}
                disabled={loading}
              >
                <option value="">-- Choose a position --</option>
                {jobs.map((job) => (
                  <option key={job.id} value={job.id}>
                    {job.job_title}
                  </option>
                ))}
              </select>
            </div>

            {error && <p className="error-message">{error}</p>}

            <div className="button-group">
              <button type="submit" disabled={loading} className="btn-primary">
                {loading ? (
                  <>
                    <span className="spinner"></span>
                    Analyzing...
                  </>
                ) : (
                  'Analyze Resume'
                )}
              </button>
              <button type="button" onClick={handleReset} className="btn-secondary">
                Reset
              </button>
              <button type="button" onClick={toggleHistory} className="btn-secondary">
                {showHistory ? 'Hide History' : 'View History'}
              </button>
            </div>
          </form>

          {results && (
            <div className="results-section">
              <h2> Analysis Results</h2>
              
              <div className={`score-card ${results.rank >= 80 ? 'excellent' : results.rank >= 60 ? 'good' : 'average'}`}>
                <h3>Match Score</h3>
                <div className="score">{results.rank}%</div>
                <p className="score-label">
                  {results.rank >= 80 ? 'Excellent Match!' : results.rank >= 60 ? 'Good Match' : 'Needs Improvement'}
                </p>
              </div>

              <div className="info-grid">
                <div className="info-card">
                  <h3> Total Experience</h3>
                  <p>{results.total_experience} years</p>
                </div>

                <div className="info-card">
                  <h3> Skills Found</h3>
                  <p>{results.skills.length} skills</p>
                  <div className="skill-tags">
                    {results.skills.map((skill, index) => (
                      <span key={index} className="tag">{skill}</span>
                    ))}
                  </div>
                </div>

                <div className="info-card">
                  <h3> Project Categories</h3>
                  <ul className="category-list">
                    {results.project_categories.map((category, index) => (
                      <li key={index}>{category}</li>
                    ))}
                  </ul>
                </div>
              </div>

              {results.suggestions && results.suggestions.length > 0 && (
                <div className="suggestions-card">
                  <h3> AI Suggestions for Improvement</h3>
                  <ul className="suggestions-list">
                    {results.suggestions.map((suggestion, index) => (
                      <li key={index}>{suggestion}</li>
                    ))}
                  </ul>
                </div>
              )}

              <button onClick={downloadReport} className="btn-download">
                 Download Report
              </button>
            </div>
          )}
        </div>

        {showHistory && (
          <div className="history-section">
            <h2> Analysis History</h2>
            {history.length === 0 ? (
              <p className="no-history">No analysis history available</p>
            ) : (
              <div className="history-list">
                {history.map((item, index) => (
                  <div key={item.id} className="history-item">
                    <div className="history-header">
                      <h4>Analysis #{history.length - index}</h4>
                      <span className="history-date">
                        {new Date(item.analyzed_at).toLocaleDateString()}
                      </span>
                    </div>
                    <div className="history-details">
                      <p><strong>Job:</strong> {item.job_title}</p>
                      <p><strong>Score:</strong> <span className={`score-badge ${item.rank >= 80 ? 'excellent' : item.rank >= 60 ? 'good' : 'average'}`}>{item.rank}%</span></p>
                      <p><strong>Experience:</strong> {item.total_experience} years</p>
                      <p><strong>Skills:</strong> {item.skills.length} identified</p>
                      <p><strong>Categories:</strong> {item.project_categories.join(', ')}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
