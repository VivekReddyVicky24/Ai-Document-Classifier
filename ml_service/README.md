# AI Document Classifier - ML Service (Flask API)

Production-ready Flask-based ML inference API for document classification with PDF text extraction and deep learning embeddings.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Running the Service](#running-the-service)
- [Model Setup](#model-setup)
- [Error Handling](#error-handling)
- [Production Deployment](#production-deployment)

## 🎯 Features

- ✅ PDF text extraction with PyPDF2
- ✅ Deep learning embeddings (Sentence-Transformers)
- ✅ Stack ensemble model for predictions
- ✅ Label encoding/decoding
- ✅ CORS enabled
- ✅ Batch prediction support
- ✅ Comprehensive error handling
- ✅ Production-ready logging
- ✅ Health check endpoints
- ✅ Singleton model pattern for efficiency

## 🛠️ Tech Stack

- **Flask** - Web framework
- **PyPDF2** - PDF text extraction
- **Sentence-Transformers** - Embedding model (BAAI/bge-large-en-v1.5)
- **scikit-learn** - ML models and label encoding
- **PyTorch** - Deep learning backend
- **NumPy** - Numerical computing
- **Flask-CORS** - CORS support
- **python-dotenv** - Environment configuration
- **Werkzeug** - WSGI utilities

## 📦 Installation

### 1. **Install Python (3.8+)**
   - Download from https://www.python.org/

### 2. **Install PyTorch** (Required for Sentence-Transformers)
   
   For CPU:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   ```
   
   For GPU (CUDA 11.8):
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

### 3. **Install ML Service Dependencies**
   ```bash
   cd ml_service
   pip install -r requirements.txt
   ```

### 4. **Verify Installation**
   ```bash
   python -c "import flask; import torch; import sentence_transformers; print('All dependencies installed!')"
   ```

## ⚙️ Configuration

### 1. **Environment Variables**

   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```env
   FLASK_ENV=development
   DEBUG=False
   HOST=0.0.0.0
   PORT=5001
   EMBEDDING_MODEL_NAME=BAAI/bge-large-en-v1.5
   STACK_MODEL_PATH=./models/stack_model.pkl
   LABEL_ENCODER_PATH=./models/label_encoder.pkl
   DEVICE=cpu  # Change to 'cuda' for GPU
   MAX_FILE_SIZE=10485760
   ```

### 2. **Model Files Setup**

   Place pre-trained models in `models/` directory:
   ```
   models/
   ├── stack_model.pkl          # Trained ensemble model
   └── label_encoder.pkl        # Label encoder for decoding
   ```

   **Note:** These files should be generated from your training pipeline.

### 3. **GPU Support** (Optional)

   If you have CUDA GPU:
   ```env
   DEVICE=cuda
   ```

## 📁 Project Structure

```
ml_service/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables
├── .env.example                    # Environment template
├── .gitignore                      # Git ignore rules
│
├── config/
│   └── settings.py                 # Configuration settings
│
├── utils/
│   ├── pdf_processor.py           # PDF text extraction
│   └── ml_model.py                # Model loading & prediction
│
├── models/
│   ├── stack_model.pkl            # Ensemble ML model
│   └── label_encoder.pkl          # Label encoder
│
├── uploads/                        # Temporary file storage
├── logs/                          # Application logs
│
├── README.md                      # This file
├── QUICK_START.md                # Quick setup guide
├── API_DOCUMENTATION.md          # API reference
└── DEPLOYMENT.md                 # Production guide
```

## 📡 API Documentation

### Base URL
```
http://localhost:5001/api
```

### Response Format

All responses follow this format:
```json
{
  "success": true/false,
  "message": "Description",
  "data": {
    // Endpoint-specific data
  }
}
```

### Endpoints

#### 1. Health Check
```
GET /health
GET /health/detailed
```

Returns service status and model readiness.

#### 2. Predict Document Label
```
POST /api/predict
Content-Type: multipart/form-data

Form Data:
- file: <PDF file>

Response (200):
{
  "success": true,
  "message": "Prediction successful",
  "data": {
    "predicted_label": "Invoice",
    "confidence": 0.9542,
    "filename": "document.pdf",
    "pages_processed": 5,
    "text_length": 2847,
    "timestamp": "2024-05-13T10:30:00.000Z"
  }
}
```

#### 3. Batch Prediction
```
POST /api/predict/batch
Content-Type: multipart/form-data

Form Data:
- files: <Multiple PDF files>

Response (200):
{
  "success": true,
  "message": "Processed 3 files",
  "data": {
    "predictions": [
      {
        "filename": "doc1.pdf",
        "predicted_label": "Invoice",
        "confidence": 0.9542,
        "pages_processed": 5
      }
    ],
    "errors": [],
    "total_files": 3,
    "successful": 3,
    "failed": 0,
    "timestamp": "2024-05-13T10:30:00.000Z"
  }
}
```

#### 4. API Information
```
GET /api/info

Response:
{
  "success": true,
  "service": "AI Document Classifier ML Service",
  "version": "1.0.0",
  "endpoints": { ... },
  "models": { ... },
  "configuration": { ... }
}
```

## 🚀 Running the Service

### Development Mode
```bash
python app.py
```

Expected output:
```
============================================================
Starting AI Document Classifier ML Service
============================================================
Initializing ML model...
Loading embedding model...
✓ Embedding model loaded successfully
Loading stack model and label encoder...
✓ Stack model and label encoder loaded successfully
✓ ML model initialized successfully
============================================================
Starting Flask server on 0.0.0.0:5001
Environment: development
Debug: False
============================================================
```

### Production Mode
```bash
export FLASK_ENV=production
export DEBUG=False
python app.py
```

Or with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

## 📊 Model Setup

### Understanding the Model Components

1. **BAAI/bge-large-en-v1.5** (Embedding Model)
   - Generates dense vectors from text
   - Captures semantic meaning
   - Automatically downloaded on first run

2. **stack_model.pkl** (Ensemble Model)
   - Trained on embeddings
   - Makes final predictions
   - Should be in `models/` directory

3. **label_encoder.pkl** (Label Encoder)
   - Converts numeric predictions to label names
   - Required for human-readable output

### Training a New Model

Example training script:
```python
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import StackingClassifier
import pickle

# Load embedding model
embedding_model = SentenceTransformer('BAAI/bge-large-en-v1.5')

# Generate embeddings from your training data
X = embedding_model.encode(training_texts)
y = training_labels

# Train label encoder
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# Train stack model (example with ensemble)
from sklearn.ensemble import RandomForestClassifier
stack_model = RandomForestClassifier(n_estimators=100)
stack_model.fit(X, y_encoded)

# Save models
pickle.dump(stack_model, open('models/stack_model.pkl', 'wb'))
pickle.dump(label_encoder, open('models/label_encoder.pkl', 'wb'))
```

### Downloading Models for Offline Use

Pre-download the embedding model:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('BAAI/bge-large-en-v1.5')
# This saves the model to ~/.cache/huggingface
```

## ⚠️ Error Handling

### Common Errors

| Error | Status | Solution |
|-------|--------|----------|
| Model not ready | 503 | Wait for initialization |
| No file provided | 400 | Include PDF file in request |
| Invalid file type | 400 | Only PDF files allowed |
| File too large | 413 | Max 10MB (configurable) |
| PDF processing error | 400 | Check PDF is valid |
| Prediction error | 500 | Check logs for details |

### Error Response Example
```json
{
  "success": false,
  "message": "Only PDF files are allowed"
}
```

## 🔐 Security Features

- Input validation on all endpoints
- File type validation (PDF only)
- File size limits
- CORS restrictions (configurable)
- Secure filename handling
- Error message sanitization
- Logging of all requests

## 📈 Performance Optimization

### 1. **Singleton Model Pattern**
   - Load models only once on startup
   - Reuse for all predictions
   - Significant performance improvement

### 2. **GPU Acceleration** (Optional)
   - Enable CUDA for faster embeddings
   - Significant speedup for large documents

### 3. **Batch Processing**
   - Process multiple files efficiently
   - Useful for bulk operations

### 4. **Caching**
   - Can implement Redis for embeddings cache
   - Reduces redundant computations

## 📚 API Usage Examples

### Python (Requests)
```python
import requests

# Single prediction
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5001/api/predict', files=files)
    result = response.json()
    print(result['data']['predicted_label'])
```

### cURL
```bash
curl -X POST \
  -F "file=@document.pdf" \
  http://localhost:5001/api/predict
```

### JavaScript (Fetch)
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:5001/api/predict', {
  method: 'POST',
  body: formData
});

const result = await response.json();
console.log(result.data.predicted_label);
```

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Install missing dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Model files not found"
**Solution:** Ensure pickle files are in `models/` directory:
```bash
ls models/stack_model.pkl
ls models/label_encoder.pkl
```

### Issue: "CUDA out of memory"
**Solution:** Use CPU instead:
```env
DEVICE=cpu
```

### Issue: Slow predictions
**Solution:** 
- Switch to GPU if available
- Check document size
- Monitor system resources

## 🚀 Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- Docker containerization
- Kubernetes deployment
- Load balancing
- Monitoring & logging
- Security hardening
- Performance tuning
- Scaling strategies

## 📄 License

ISC

## 🤝 Support

For issues or questions:
- Check logs in `logs/ml_service.log`
- Review API documentation
- Test with cURL or Postman
- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

**Happy Classifying! 🎉**
