import axios from 'axios';

// Use environment variable for API URL, fallback to localhost for development
const API_BASE_URL = process.env.REACT_APP_API_URL 
  ? `${process.env.REACT_APP_API_URL}/api`
  : 'http://127.0.0.1:8000/api';

export const apiService = {
  // Get all job descriptions
  getJobs: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/jobs/`);
      // Backend returns {status: true, data: [...]}
      return response.data.data || [];
    } catch (error) {
      console.error('Error fetching jobs:', error);
      throw error;
    }
  },

  // Analyze resume
  analyzeResume: async (jobDescriptionId, resumeFile) => {
    try {
      const formData = new FormData();
      formData.append('job_description', jobDescriptionId);
      formData.append('resume', resumeFile);

      const response = await axios.post(`${API_BASE_URL}/resume/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      // Backend returns {status: true, message: '...', data: {...}}
      console.log('API Response:', response.data);
      console.log('Returning data:', response.data.data);
      return response.data.data || response.data;
    } catch (error) {
      console.error('Error analyzing resume:', error);
      console.error('Error response:', error.response?.data);
      throw error;
    }
  },

  // Get analysis history
  getHistory: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/history/`);
      // Backend returns {status: true, data: [...]}
      return response.data.data || [];
    } catch (error) {
      console.error('Error fetching history:', error);
      throw error;
    }
  },
};
