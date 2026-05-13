# ML Service API Documentation

Complete API reference for the AI Document Classifier ML Service.

## Base URL

```
http://localhost:5001/api
```

## Response Format

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

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad Request |
| 404 | Not Found |
| 405 | Method Not Allowed |
| 413 | File Too Large |
| 500 | Server Error |
| 503 | Service Unavailable |

---

## Health Check Endpoints

### 1. Basic Health Check

**Endpoint:** `GET /health`

**Response (200):**
```json
{
  "success": true,
  "status": "healthy",
  "service": "AI Document Classifier ML Service",
  "timestamp": "2024-05-13T10:30:00.000Z",
  "model_status": "ready"
}
```

**Example:**
```bash
curl http://localhost:5001/health
```

---

### 2. Detailed Health Check

**Endpoint:** `GET /health/detailed`

**Response (200):**
```json
{
  "success": true,
  "status": "healthy",
  "service": "AI Document Classifier ML Service",
  "environment": "development",
  "debug_mode": false,
  "model_initialized": true,
  "model_error": null,
  "timestamp": "2024-05-13T10:30:00.000Z",
  "embedding_model": "BAAI/bge-large-en-v1.5",
  "api_version": "1.0.0"
}
```

**Example:**
```bash
curl http://localhost:5001/health/detailed
```

---

## Prediction Endpoints

### 3. Single Document Prediction

**Endpoint:** `POST /api/predict`

**Authentication:** None required

**Content-Type:** `multipart/form-data`

**Request Parameters:**
- `file` (required): PDF file

**Constraints:**
- File must be PDF format
- Maximum size: 10MB (configurable)
- Minimum readable text: 10 characters

**Response (200):**
```json
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

**Error Responses:**

Missing file (400):
```json
{
  "success": false,
  "message": "No file provided"
}
```

Invalid file type (400):
```json
{
  "success": false,
  "message": "Only PDF files are allowed"
}
```

File too large (413):
```json
{
  "success": false,
  "message": "File too large. Maximum size: 10.0MB"
}
```

PDF extraction error (400):
```json
{
  "success": false,
  "message": "PDF extraction error: PDF file has no pages"
}
```

Model not ready (503):
```json
{
  "success": false,
  "message": "ML model not ready. Please try again later.",
  "error": "Error message if available"
}
```

**Examples:**

cURL:
```bash
curl -X POST \
  -F "file=@document.pdf" \
  http://localhost:5001/api/predict
```

Python (requests):
```python
import requests

with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:5001/api/predict', files=files)
    result = response.json()
    
    if result['success']:
        print(f"Label: {result['data']['predicted_label']}")
        print(f"Confidence: {result['data']['confidence']}")
    else:
        print(f"Error: {result['message']}")
```

JavaScript (Fetch):
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const response = await fetch('http://localhost:5001/api/predict', {
  method: 'POST',
  body: formData
});

const result = await response.json();
if (result.success) {
  console.log(`Label: ${result.data.predicted_label}`);
  console.log(`Confidence: ${result.data.confidence}`);
}
```

---

### 4. Batch Prediction

**Endpoint:** `POST /api/predict/batch`

**Authentication:** None required

**Content-Type:** `multipart/form-data`

**Request Parameters:**
- `files` (required): Multiple PDF files

**Constraints:**
- Maximum 10 files per request
- Each file: max 10MB
- All must be PDF format

**Response (200):**
```json
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
      },
      {
        "filename": "doc2.pdf",
        "predicted_label": "Report",
        "confidence": 0.8765,
        "pages_processed": 10
      },
      {
        "filename": "doc3.pdf",
        "predicted_label": "Contract",
        "confidence": 0.9123,
        "pages_processed": 3
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

**Partial Success Response (200):**
```json
{
  "success": false,
  "message": "Processed 2 files",
  "data": {
    "predictions": [
      {
        "filename": "doc1.pdf",
        "predicted_label": "Invoice",
        "confidence": 0.9542,
        "pages_processed": 5
      }
    ],
    "errors": [
      {
        "file": "invalid.txt",
        "error": "Invalid file type"
      },
      {
        "file": "empty.pdf",
        "error": "File is empty"
      }
    ],
    "total_files": 3,
    "successful": 1,
    "failed": 2,
    "timestamp": "2024-05-13T10:30:00.000Z"
  }
}
```

**Examples:**

cURL:
```bash
curl -X POST \
  -F "files=@doc1.pdf" \
  -F "files=@doc2.pdf" \
  -F "files=@doc3.pdf" \
  http://localhost:5001/api/predict/batch
```

Python:
```python
import requests

files = [
    ('files', open('doc1.pdf', 'rb')),
    ('files', open('doc2.pdf', 'rb')),
    ('files', open('doc3.pdf', 'rb')),
]

response = requests.post('http://localhost:5001/api/predict/batch', files=files)
result = response.json()

for prediction in result['data']['predictions']:
    print(f"{prediction['filename']}: {prediction['predicted_label']}")

if result['data']['errors']:
    print(f"Errors: {result['data']['errors']}")
```

---

## Information Endpoints

### 5. API Information

**Endpoint:** `GET /api/info`

**Response (200):**
```json
{
  "success": true,
  "service": "AI Document Classifier ML Service",
  "version": "1.0.0",
  "description": "Flask-based ML inference API for document classification",
  "endpoints": {
    "health": {
      "method": "GET",
      "path": "/health",
      "description": "Health check"
    },
    "health_detailed": {
      "method": "GET",
      "path": "/health/detailed",
      "description": "Detailed health check"
    },
    "predict": {
      "method": "POST",
      "path": "/api/predict",
      "description": "Predict document label from PDF",
      "content_type": "multipart/form-data",
      "parameters": {
        "file": "PDF file (required)"
      }
    },
    "batch_predict": {
      "method": "POST",
      "path": "/api/predict/batch",
      "description": "Batch predict multiple PDFs",
      "content_type": "multipart/form-data",
      "parameters": {
        "files": "Multiple PDF files (required)"
      }
    }
  },
  "models": {
    "embedding_model": "BAAI/bge-large-en-v1.5",
    "stack_model": "stack_model.pkl",
    "label_encoder": "label_encoder.pkl"
  },
  "features": {
    "pdf_text_extraction": true,
    "batch_processing": true,
    "cors_enabled": true,
    "model_singleton": true
  },
  "configuration": {
    "max_file_size_mb": 10.0,
    "max_pdf_pages": 100,
    "min_text_length": 10,
    "environment": "development",
    "debug": false
  }
}
```

**Example:**
```bash
curl http://localhost:5001/api/info
```

---

## Model Pipeline Explanation

### How Document Classification Works

```
1. Upload PDF
   ↓
2. Extract Text (PyPDF2)
   ↓
3. Generate Embedding (BAAI/bge-large-en-v1.5)
   ↓
4. Predict with Stack Model (stack_model.pkl)
   ↓
5. Decode Label (label_encoder.pkl)
   ↓
6. Return Predicted Label + Confidence
```

### Models Used

1. **BAAI/bge-large-en-v1.5**
   - Sentence-BERT embedding model
   - Generates 1024-dimensional vectors
   - Pre-trained on large text corpus
   - Captures semantic meaning

2. **stack_model.pkl**
   - Ensemble classifier (Random Forest, SVM, etc.)
   - Trained on embeddings
   - Outputs class predictions
   - Size: ~100MB typical

3. **label_encoder.pkl**
   - Converts numeric predictions to label names
   - Example: 0 → "Invoice", 1 → "Report", etc.
   - Essential for human-readable output

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| No file provided | Missing form parameter | Include PDF in `file` field |
| Only PDF files allowed | Wrong file type | Upload PDF file only |
| File too large | Exceeds 10MB | Use smaller PDF |
| PDF file has no pages | Empty PDF | Use valid PDF |
| No readable text found | PDF extraction failed | Check PDF content |
| ML model not ready | Service initializing | Wait for startup |
| Error making prediction | Model inference failed | Check logs |
| Internal server error | Unexpected error | Check server logs |

### Error Response Format

```json
{
  "success": false,
  "message": "Error description"
}
```

---

## Performance Metrics

### Typical Performance

- Single prediction: 2-5 seconds (CPU)
- Single prediction: 0.5-1 second (GPU)
- Text extraction: 0.1-0.5 seconds
- Embedding generation: 1-2 seconds
- Model prediction: 0.1-0.3 seconds

### Batch Performance

- 10 files: 20-50 seconds (CPU)
- 10 files: 5-10 seconds (GPU)

### Resource Usage

- Memory: ~2GB (embedding model)
- GPU VRAM: ~2GB (if CUDA enabled)
- Disk: ~500MB (models + dependencies)

---

## CORS Configuration

CORS is enabled for all origins by default:

```
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, OPTIONS
Access-Control-Allow-Headers: Content-Type
```

For production, restrict origins:
- Edit `app.py` CORS configuration
- Whitelist specific domains

---

## Rate Limiting

Currently no rate limiting implemented. For production:
- Add Flask-Limiter: `pip install flask-limiter`
- Implement per-IP rate limits
- Consider queue system for high load

---

## Authentication

Currently no authentication required. For production:
- Add API key authentication
- Implement JWT tokens
- Add role-based access control

---

## Security Considerations

1. **File Upload Security**
   - Validates PDF format
   - Limits file size
   - Uses secure filename handling
   - Deletes temp files

2. **Input Validation**
   - Validates all parameters
   - Checks file MIME type
   - Sanitizes error messages

3. **Error Handling**
   - No sensitive info in errors
   - Logs errors securely
   - Returns generic error messages

---

## Deployment Considerations

### Production Checklist

- [ ] SSL/HTTPS enabled
- [ ] CORS restricted to known domains
- [ ] Rate limiting implemented
- [ ] Monitoring & alerts configured
- [ ] Logging to persistent storage
- [ ] Model files secured
- [ ] Database backups
- [ ] Error tracking (Sentry)
- [ ] Health checks configured
- [ ] Load testing completed

### Scaling Strategies

1. **Horizontal Scaling**
   - Multiple ML service instances
   - Load balancer (nginx, Kubernetes)
   - Shared model cache

2. **Vertical Scaling**
   - Increase server resources
   - GPU acceleration
   - Memory optimization

3. **Caching**
   - Redis for embedding cache
   - Reduce redundant computations

---

## Testing

### Unit Tests

```python
import requests

def test_health():
    response = requests.get('http://localhost:5001/health')
    assert response.status_code == 200
    assert response.json()['success'] == True

def test_predict():
    with open('test.pdf', 'rb') as f:
        files = {'file': f}
        response = requests.post('http://localhost:5001/api/predict', files=files)
        assert response.status_code == 200
        assert response.json()['success'] == True
```

### Load Testing

Using Apache Bench:
```bash
ab -n 100 -c 10 http://localhost:5001/health
```

Using Locust:
```bash
pip install locust
locust -f locustfile.py --host=http://localhost:5001
```

---

## API Version History

### v1.0.0 (Current)
- Initial release
- Single file prediction
- Batch prediction
- Health checks
- Comprehensive error handling

---

Last Updated: May 13, 2024
