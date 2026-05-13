import React, { useState } from 'react';
import { documentAPI } from '../utils/api';
import '../styles/fileUpload.css';

const FileUpload = ({ onUploadSuccess, onError }) => {
  const [dragActive, setDragActive] = useState(false);
  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [uploadError, setUploadError] = useState(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const validateFiles = (filesToValidate) => {
    return filesToValidate.every((file) => file.type === 'application/pdf');
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    setUploadError(null);

    const droppedFiles = Array.from(e.dataTransfer.files);

    if (!validateFiles(droppedFiles)) {
      setUploadError('Only PDF files are allowed');
      onError?.('Only PDF files are allowed');
      return;
    }

    setFiles((prevFiles) => [...prevFiles, ...droppedFiles]);
  };

  const handleFileInput = (e) => {
    setUploadError(null);
    const selectedFiles = Array.from(e.target.files);

    if (!validateFiles(selectedFiles)) {
      setUploadError('Only PDF files are allowed');
      onError?.('Only PDF files are allowed');
      return;
    }

    setFiles((prevFiles) => [...prevFiles, ...selectedFiles]);
  };

  const removeFile = (index) => {
    setFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (files.length === 0) {
      setUploadError('Please select at least one PDF file');
      onError?.('Please select at least one PDF file');
      return;
    }

    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    try {
      setUploading(true);
      setUploadError(null);
      const response = await documentAPI.uploadFiles(formData);
      onUploadSuccess?.(response.data);
      setFiles([]);
    } catch (error) {
      const errorMessage =
        error.response?.data?.message || 'Failed to upload files. Please try again.';
      setUploadError(errorMessage);
      onError?.(errorMessage);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="file-upload-container">
      <div className="upload-section">
        <div
          className={`drag-drop-area ${dragActive ? 'active' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <div className="upload-icon">📥</div>
          <h3>Drag and drop PDF files here</h3>
          <p>or</p>
          <label className="file-input-label">
            <span>Click to browse</span>
            <input
              type="file"
              multiple
              accept=".pdf"
              onChange={handleFileInput}
              disabled={uploading}
            />
          </label>
          <p className="upload-info">You can select multiple PDF files</p>
        </div>

        {files.length > 0 && (
          <div className="selected-files">
            <h4>Selected Files ({files.length})</h4>
            <ul className="files-list">
              {files.map((file, index) => (
                <li key={index} className="file-item">
                  <span className="file-icon">📄</span>
                  <span className="file-name">{file.name}</span>
                  <span className="file-size">({(file.size / 1024).toFixed(2)} KB)</span>
                  <button
                    type="button"
                    className="remove-btn"
                    onClick={() => removeFile(index)}
                    disabled={uploading}
                  >
                    ✕
                  </button>
                </li>
              ))}
            </ul>

            <button
              className="upload-btn"
              onClick={handleUpload}
              disabled={uploading || files.length === 0}
            >
              {uploading ? (
                <>
                  <span className="spinner-small"></span> Uploading...
                </>
              ) : (
                `Upload ${files.length} File${files.length !== 1 ? 's' : ''}`
              )}
            </button>
          </div>
        )}

        {uploadError && <div className="error-message">{uploadError}</div>}
      </div>
    </div>
  );
};

export default FileUpload;
