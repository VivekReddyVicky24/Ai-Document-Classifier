# ML Service - Quick Start Guide

Get the AI Document Classifier ML service running in 5 minutes.

## Prerequisites

- Python 3.8+
- pip
- PyTorch (CPU or GPU)

## Quick Setup

### 1. Install PyTorch

**CPU:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```

**GPU (CUDA 11.8):**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 2. Install Dependencies
```bash
cd ml_service
pip install -r requirements.txt
```

### 3. Place Model Files

Copy your trained models to the `models/` directory:
```
models/
├── stack_model.pkl
└── label_encoder.pkl
```

### 4. Start ML Service
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

## 5. Test the API

### Check Health
```bash
curl http://localhost:5001/health
```

### Get API Info
```bash
curl http://localhost:5001/api/info
```

### Make Prediction
```bash
curl -X POST \
  -F "file=@document.pdf" \
  http://localhost:5001/api/predict
```

Response:
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

## Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | Health check |
| GET | `/api/info` | API information |
| POST | `/api/predict` | Predict single PDF |
| POST | `/api/predict/batch` | Predict multiple PDFs |

## Configuration

Edit `.env` to customize:

```env
FLASK_ENV=development
DEBUG=False
HOST=0.0.0.0
PORT=5001
DEVICE=cpu  # Change to 'cuda' for GPU
```

## Next Steps

1. Start backend server: `cd ../server && npm run dev`
2. Start frontend: `cd ../client && npm run dev`
3. Connect all services together
4. Test end-to-end workflow

## Troubleshooting

### ImportError: No module named 'torch'
- Install PyTorch first (see step 1)

### FileNotFoundError: models/stack_model.pkl
- Place trained model files in `models/` directory
- See [README.md](README.md) for training instructions

### Port 5001 already in use
- Change PORT in `.env`
- Or kill process: `lsof -i :5001 | kill -9 <PID>`

### Slow predictions
- Switch to GPU if available: `DEVICE=cuda`
- Check document size
- Monitor RAM usage

---

See [README.md](README.md) for complete documentation.
See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details.
