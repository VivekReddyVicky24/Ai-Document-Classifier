import React, { useState } from 'react';
import FileUpload from '../components/FileUpload';
import UploadHistory from '../components/UploadHistory';
import '../styles/dashboard.css';

const Dashboard = () => {
  const [successMessage, setSuccessMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [selectedLabel, setSelectedLabel] = useState(null);

  const handleUploadSuccess = (response) => {
    setSuccessMessage('✓ Files uploaded successfully! Processing...');
    setErrorMessage('');
    // Trigger refresh of upload history
    setRefreshTrigger((prev) => prev + 1);

    // Clear success message after 3 seconds
    setTimeout(() => {
      setSuccessMessage('');
    }, 3000);
  };

  const handleUploadError = (message) => {
    setErrorMessage(message);
    setSuccessMessage('');
  };

  const handleCloseMessage = (type) => {
    if (type === 'success') {
      setSuccessMessage('');
    } else {
      setErrorMessage('');
    }
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>📊 AI Document Classifier</h1>
        <p>Upload PDF documents for AI-powered classification</p>
      </div>

      {successMessage && (
        <div className="message success-message">
          <span>{successMessage}</span>
          <button onClick={() => handleCloseMessage('success')} className="close-btn">
            ✕
          </button>
        </div>
      )}

      {errorMessage && (
        <div className="message error-message">
          <span>{errorMessage}</span>
          <button onClick={() => handleCloseMessage('error')} className="close-btn">
            ✕
          </button>
        </div>
      )}

      <div className="dashboard-content">
        <section className="upload-section">
          <FileUpload
            onUploadSuccess={handleUploadSuccess}
            onError={handleUploadError}
          />
        </section>

        <section className="history-section">
          <UploadHistory 
            refreshTrigger={refreshTrigger}
            selectedLabel={selectedLabel}
            onLabelChange={setSelectedLabel}
          />
        </section>
      </div>
    </div>
  );
};

export default Dashboard;
