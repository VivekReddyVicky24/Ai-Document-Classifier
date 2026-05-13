# Backend Quick Start Guide

Get the AI Document Classifier backend running in 5 minutes.

## Prerequisites

- Node.js (v14+)
- MongoDB (local or MongoDB Atlas)
- npm or yarn

## Quick Setup

### 1. Start MongoDB
```bash
# If MongoDB is installed locally:
mongod

# Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas
# Update MONGODB_URI in .env with your connection string
```

### 2. Start Backend Server
```bash
# Development mode (with auto-reload)
npm run dev

# Production mode
npm start
```

Expected output:
```
╔════════════════════════════════════════╗
║  🚀 Server running on port 5000        ║
║  🌍 Environment: development           ║
║  📡 MongoDB: Connected                 ║
╚════════════════════════════════════════╝
```

## 3. Test the API

### Register a User
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

Save the returned `token` for protected routes.

### Get Current User
```bash
curl http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Upload PDF File
```bash
curl -X POST http://localhost:5000/api/uploads \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf"
```

### Get Upload History
```bash
curl http://localhost:5000/api/uploads/history \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Key Endpoints

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | `/api/auth/register` | ❌ | Register new user |
| POST | `/api/auth/login` | ❌ | Login user |
| GET | `/api/auth/me` | ✅ | Get current user |
| POST | `/api/uploads` | ✅ | Upload PDF |
| GET | `/api/uploads/history` | ✅ | Get upload history |
| GET | `/api/uploads/:id` | ✅ | Get upload details |
| DELETE | `/api/uploads/:id` | ✅ | Delete upload |

## Configuration

Edit `.env` file:
```env
MONGODB_URI=mongodb://localhost:27017/ai-document-classifier
JWT_SECRET=your_secret_key
PORT=5000
ML_SERVICE_URL=http://localhost:5001/classify
```

## Troubleshooting

**MongoDB won't connect:**
- Check MongoDB is running: `mongosh`
- Update `MONGODB_URI` if using remote

**JWT errors:**
- Add JWT_SECRET to `.env`

**ML Service errors:**
- Ensure Python Flask service is running on port 5001

**Port 5000 in use:**
- Change PORT in `.env` or kill process: `lsof -i :5000`

## Next Steps

1. Start the frontend: `cd ../client && npm run dev`
2. Set up Python ML service (Flask)
3. Test API endpoints with Postman
4. Deploy to production

---

See [README.md](./README.md) for complete documentation.
