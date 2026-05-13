# Troubleshooting Guide - ML Service

Common issues and solutions for the Flask ML inference API.

## Installation Issues

### Problem: "No module named 'torch'"
```
ModuleNotFoundError: No module named 'torch'
```

**Solution:**
Install PyTorch first:
```bash
# CPU version
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# GPU version (CUDA 11.8)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Problem: "No module named 'flask'"
```
ModuleNotFoundError: No module named 'flask'
```

**Solution:**
Install all requirements:
```bash
pip install -r requirements.txt
```

### Problem: "No module named 'sentence_transformers'"
```
ModuleNotFoundError: No module named 'sentence_transformers'
```

**Solution:**
```bash
pip install sentence-transformers
```

---

## Startup Issues

### Problem: "Model files not found"
```
FileNotFoundError: Stack model not found at ./models/stack_model.pkl
FileNotFoundError: Label encoder not found at ./models/label_encoder.pkl
```

**Solution:**
1. Create models directory:
   ```bash
   mkdir -p models
   ```

2. Place trained models:
   ```bash
   models/
   ├── stack_model.pkl
   └── label_encoder.pkl
   ```

3. Check file paths:
   ```bash
   ls -lh models/
   ```

### Problem: "Cannot start server - ML model failed to initialize"
```
Error: Cannot start server - ML model failed to initialize
Error: stack_model.pkl is corrupted or invalid format
```

**Solution:**
1. Verify pickle files are valid:
   ```python
   import pickle
   pickle.load(open('models/stack_model.pkl', 'rb'))
   pickle.load(open('models/label_encoder.pkl', 'rb'))
   ```

2. Regenerate models if corrupted
3. Check file encoding (binary, not text)

### Problem: "CUDA out of memory"
```
RuntimeError: CUDA out of memory
```

**Solution:**
Use CPU instead:
```env
DEVICE=cpu
```

Or reduce batch size in code.

### Problem: Port already in use
```
OSError: [Errno 48] Address already in use
```

**Solution:**
1. Change PORT in `.env`:
   ```env
   PORT=5002
   ```

2. Or kill process using port:
   ```bash
   # Linux/Mac
   lsof -i :5001 | tail -1 | awk '{print $2}' | xargs kill -9
   
   # Windows
   netstat -ano | findstr :5001
   taskkill /PID <PID> /F
   ```

---

## Model Loading Issues

### Problem: "Embedding model download failure"
```
Error: Failed to download embedding model BAAI/bge-large-en-v1.5
```

**Solution:**
1. Check internet connection
2. Download manually:
   ```python
   from sentence_transformers import SentenceTransformer
   model = SentenceTransformer('BAAI/bge-large-en-v1.5')
   # Wait for download to complete
   ```

3. Use offline mode:
   - Pre-download model
   - Set cache directory
   ```env
   HF_HOME=./cache
   ```

### Problem: "Model not ready - 503 error"
```
Error: ML model not ready. Please try again later.
```

**Solution:**
1. Wait for initialization (first startup takes time)
2. Check logs for errors:
   ```bash
   tail -f logs/ml_service.log
   ```

3. Verify all model files exist
4. Check system resources (RAM, disk)

### Problem: "pickle.UnpicklingError"
```
pickle.UnpicklingError: invalid load key, '<'
```

**Solution:**
File is corrupted or wrong format:
1. Regenerate model files
2. Verify they're binary pickle format
3. Use correct Python version (pickle compatibility)

---

## PDF Processing Issues

### Problem: "No readable text found in PDF"
```
Error: No readable text found in PDF
```

**Solution:**
1. Check PDF has text content (not image-only)
2. Try OCR processing (requires additional setup)
3. Use different PDF

### Problem: "PDF file has no pages"
```
Error: PDF file has no pages
```

**Solution:**
1. Verify PDF file is valid
2. Test with different PDF reader
3. Check file corruption

### Problem: "Error extracting text from PDF"
```
Error: Failed to extract text from PDF
```

**Solution:**
1. Check PDF format (must be standard PDF)
2. Test PDF with PyPDF2 directly:
   ```python
   from PyPDF2 import PdfReader
   reader = PdfReader('file.pdf')
   print(len(reader.pages))
   ```

3. Try converting PDF format

---

## File Upload Issues

### Problem: "No file provided"
```
Error: No file provided
```

**Solution:**
Check request format:
```bash
# Correct
curl -X POST -F "file=@document.pdf" http://localhost:5001/api/predict

# Incorrect - missing -F
curl -X POST http://localhost:5001/api/predict document.pdf
```

### Problem: "Only PDF files are allowed"
```
Error: Only PDF files are allowed
```

**Solution:**
1. Ensure file is PDF format
2. Check file extension: `.pdf`
3. Verify MIME type: `application/pdf`

### Problem: "File too large"
```
Error: File too large. Maximum size: 10.0MB
```

**Solution:**
1. Use smaller PDF or split file
2. Increase limit in `.env`:
   ```env
   MAX_FILE_SIZE=52428800  # 50MB
   ```

3. Compress PDF file

### Problem: "File is empty"
```
Error: File is empty
```

**Solution:**
1. Ensure file has content
2. Check file size: `ls -lh document.pdf`
3. Verify file uploaded correctly

---

## Prediction Issues

### Problem: "Error making prediction"
```
Error: Error making prediction
```

**Solution:**
1. Check logs for detailed error:
   ```bash
   tail logs/ml_service.log
   ```

2. Verify model files are valid
3. Check extracted text length (minimum 10 chars)
4. Check system resources

### Problem: "Prediction returns wrong label"
```
{
  "predicted_label": "Unknown",
  "confidence": 0.2
}
```

**Solution:**
1. Model may need retraining
2. Check label encoder has all classes
3. Verify training data quality
4. Consider low confidence predictions

### Problem: "Very low confidence score"
```
{
  "confidence": 0.15
}
```

**Solution:**
1. Document may not match training data
2. Model may need more training
3. Consider ensemble of models
4. Check if label is uncommon

### Problem: "Timeout during prediction"
```
Error: Prediction timeout (>60 seconds)
```

**Solution:**
1. Check system resources (CPU/GPU)
2. Reduce document size
3. Use GPU: `DEVICE=cuda`
4. Increase timeout in settings

---

## Batch Prediction Issues

### Problem: "Batch size too large"
```
Error: Too many files. Maximum: 10
```

**Solution:**
1. Send fewer files (max 10)
2. Or increase limit in code
3. Split into multiple batch requests

### Problem: "Partial failures in batch"
```
{
  "errors": [
    {"file": "doc.txt", "error": "Invalid file type"}
  ]
}
```

**Solution:**
1. Check error message for each file
2. Retry with valid files only
3. Fix file format issue

---

## CORS Issues

### Problem: "CORS policy violation"
```
Access to XMLHttpRequest at 'http://localhost:5001/api/predict'
from origin 'http://localhost:3000' blocked by CORS policy
```

**Solution:**
1. CORS should be enabled by default
2. Check if request origin is allowed:
   ```python
   # In app.py
   CORS(app, resources={
       r"/api/*": {
           "origins": "*",  # Allow all origins for dev
       }
   })
   ```

3. For production, whitelist specific origins

---

## Logging & Debugging

### Problem: "Cannot find logs"
```
FileNotFoundError: logs/ml_service.log
```

**Solution:**
1. Create logs directory:
   ```bash
   mkdir -p logs
   ```

2. Check permissions:
   ```bash
   chmod 755 logs
   ```

### Problem: "Need more detailed logs"
**Solution:**
Change log level in `.env`:
```env
LOG_LEVEL=DEBUG
```

View logs:
```bash
tail -f logs/ml_service.log
```

---

## Performance Issues

### Problem: Slow predictions
**Solution:**
1. Use GPU if available:
   ```env
   DEVICE=cuda
   ```

2. Check system resources:
   ```bash
   # Linux
   top
   nvidia-smi  # For GPU
   
   # Mac
   top
   
   # Windows
   taskmgr
   ```

3. Reduce document size
4. Cache embeddings with Redis

### Problem: High memory usage
**Solution:**
1. Check model size:
   ```bash
   du -h models/
   ```

2. Monitor memory:
   ```bash
   ps aux | grep python
   ```

3. Reduce batch size
4. Restart service

### Problem: API response times > 5 seconds
**Solution:**
1. Check PDF extraction time
2. Profile embedding generation:
   ```python
   import time
   start = time.time()
   embedding = model.encode(text)
   print(f"Time: {time.time() - start}s")
   ```

3. Check network latency
4. Use caching layer

---

## Integration Issues

### Problem: Backend cannot connect to ML service
```
Error: connect ECONNREFUSED (from Node.js backend)
```

**Solution:**
1. Check ML service is running:
   ```bash
   curl http://localhost:5001/health
   ```

2. Verify port is correct (5001)
3. Check firewall allows connection
4. Verify ML_SERVICE_URL in backend `.env`

### Problem: Response format mismatch
```
Backend error: Cannot read property 'predicted_label' of undefined
```

**Solution:**
1. Check API response format
2. Verify response includes 'data' key
3. Test endpoint directly:
   ```bash
   curl -X POST -F "file=@test.pdf" http://localhost:5001/api/predict
   ```

---

## Production Issues

### Problem: Cannot start with gunicorn
```
Error: Failed to find application object: 'app'
```

**Solution:**
```bash
gunicorn -w 4 -b 0.0.0.0:5001 app:app
```

Ensure `app` variable is exported in app.py

### Problem: SSL certificate error
```
Error: CERTIFICATE_VERIFY_FAILED
```

**Solution:**
```bash
# Disable SSL verification (dev only!)
export PYTHONHTTPSVERIFY=0

# Or fix certificate
pip install --upgrade certifi
```

### Problem: Model files not found in production
**Solution:**
1. Ensure models/ directory is copied to production
2. Use absolute paths in config
3. Mount volume if using Docker

---

## Common Error Codes

| Code | Issue | Fix |
|------|-------|-----|
| 400 | Bad request | Check parameters |
| 404 | Not found | Check endpoint path |
| 405 | Method not allowed | Use correct HTTP method |
| 413 | File too large | Upload smaller file |
| 500 | Server error | Check logs |
| 503 | Service unavailable | Wait for startup |

---

## Diagnostic Script

```bash
#!/bin/bash
echo "=== ML Service Diagnostics ==="
echo ""
echo "Python version:"
python --version
echo ""
echo "Packages installed:"
python -c "import torch, flask, PyPDF2, sentence_transformers; print('✓ All packages OK')"
echo ""
echo "Model files:"
ls -lh models/
echo ""
echo ".env file:"
[ -f .env ] && echo "✓ .env exists" || echo "✗ .env missing"
echo ""
echo "Starting service..."
python app.py
```

---

## Quick Fixes

1. **Service won't start?**
   - Check all dependencies: `pip install -r requirements.txt`
   - Check model files exist: `ls models/`
   - Check port is free: `lsof -i :5001`

2. **Predictions failing?**
   - Verify PDF is valid
   - Check models are not corrupted
   - Look at logs: `tail logs/ml_service.log`

3. **Slow performance?**
   - Use GPU: `DEVICE=cuda`
   - Check system resources
   - Reduce batch size

4. **Integration issues?**
   - Test endpoint: `curl http://localhost:5001/health`
   - Check CORS: Use browser dev tools
   - Verify request format

---

## Getting Help

1. **Check Logs First**
   ```bash
   tail -f logs/ml_service.log
   ```

2. **Test Endpoint**
   ```bash
   curl http://localhost:5001/api/info
   ```

3. **Verify Setup**
   - Models exist
   - Dependencies installed
   - Environment configured

4. **Review Documentation**
   - README.md - Setup
   - API_DOCUMENTATION.md - API details
   - QUICK_START.md - Fast setup

---

**Still stuck?** Check the logs carefully - they usually contain the root cause! 🔍
