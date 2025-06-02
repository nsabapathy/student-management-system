import axios from 'axios';

// Create an instance of axios with default configurations
const api = axios.create({
  // We're using relative URLs to work with Vite's proxy setup
  baseURL: '/api', // Set the base URL to use the proxy configuration
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  // Add timeout to avoid long-hanging requests
  timeout: 15000,
});

// Add a request interceptor to automatically add the auth token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    // Debug log the request URL
    console.log('API Request URL:', config.url);
    
    // FastAPI endpoints work better without trailing slashes for this application
    // Do not add trailing slashes to URLs
    
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle common error scenarios
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Log the error for debugging
    console.log('API Error:', error);
    
    // Log more detailed information about the request
    if (error.config) {
      console.log('Request URL:', error.config.url);
      console.log('Request Method:', error.config.method);
      console.log('Request Data:', error.config.data);
    }
    
    // Log response details if available
    if (error.response) {
      console.log('Response Status:', error.response.status);
      console.log('Response Data:', error.response.data);
    }
    
    // Handle authentication errors (401/403) by redirecting to login
    if (error.response && (error.response.status === 401 || error.response.status === 403)) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    
    // Add better error handling for network errors
    if (error.code === 'ERR_NETWORK' || error.message === 'Network Error') {
      console.error('Network Error: Unable to connect to the API.');
    }
    
    return Promise.reject(error);
  }
);

export default api;
