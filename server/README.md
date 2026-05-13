# AI Document Classifier - Backend Server

A production-ready Node.js + Express backend for the AI document classification system with JWT authentication, MongoDB, and integration with Python ML service.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Running the Server](#running-the-server)
- [Error Handling](#error-handling)
- [Production Deployment](#production-deployment)

## 🎯 Features

- ✅ User authentication with JWT
- ✅ Password hashing with bcrypt
- ✅ MongoDB integration with Mongoose
- ✅ PDF file upload with Multer
- ✅ Integration with Python ML service
- ✅ Upload history tracking
- ✅ MVC architecture
- ✅ Complete error handling
- ✅ CORS support
- ✅ Environment configuration
- ✅ Production-ready code

## 🛠️ Tech Stack

- **Node.js** - Runtime
- **Express.js** - Web framework
- **MongoDB** - Database
- **Mongoose** - ODM
- **JWT** - Authentication
- **bcryptjs** - Password hashing
- **Multer** - File upload
- **Axios** - HTTP client
- **CORS** - Cross-Origin Resource Sharing
- **dotenv** - Environment variables
- **Nodemon** - Development server

## 📦 Installation

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Install MongoDB** (if not already installed)
   - Download from: https://www.mongodb.com/try/download/community
   - Or use MongoDB Atlas (cloud): https://www.mongodb.com/cloud/atlas

3. **Verify Installation**
   ```bash
   npm list
   ```

## ⚙️ Configuration

1. **Copy Environment File**
   ```bash
   # .env file is already created with default values
   # Edit as needed for your environment
   ```

2. **Edit `.env` File**
   ```env
   # MongoDB Configuration
   MONGODB_URI=mongodb://localhost:27017/ai-document-classifier

   # JWT Configuration
   JWT_SECRET=your_secure_jwt_secret_key_here
   JWT_EXPIRE=7d

   # Server Configuration
   PORT=5000
   NODE_ENV=development

   # Python ML Service Configuration
   ML_SERVICE_URL=http://localhost:5001/classify

   # File Upload Configuration
   MAX_FILE_SIZE=10485760
   UPLOAD_TEMP_DIR=./uploads/temp
   ```

3. **MongoDB Setup**
   - Ensure MongoDB is running on `localhost:27017`
   - Or update `MONGODB_URI` with your connection string

## 📁 Project Structure

```
server/
├── config/
│   └── database.js                 # MongoDB connection
├── controllers/
│   ├── authController.js           # Authentication logic
│   └── uploadController.js         # File upload logic
├── middleware/
│   ├── authMiddleware.js           # JWT verification
│   └── errorHandler.js             # Error handling
├── models/
│   ├── User.js                     # User model
│   └── Upload.js                   # Upload model
├── routes/
│   ├── authRoutes.js               # Auth routes
│   └── uploadRoutes.js             # Upload routes
├── utils/
│   ├── jwt.js                      # JWT utilities
│   └── validators.js               # Input validators
├── uploads/
│   └── temp/                       # Temporary upload directory
├── .env                            # Environment variables
├── .env.example                    # Environment template
├── server.js                       # Main server file
└── package.json                    # Dependencies
```

## 📡 API Documentation

### Authentication Routes

#### Register User
```
POST /api/auth/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}

Response (201):
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "...",
      "name": "John Doe",
      "email": "john@example.com"
    },
    "token": "eyJhbGc..."
  }
}
```

#### Login User
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "john@example.com",
  "password": "password123"
}

Response (200):
{
  "success": true,
  "message": "Logged in successfully",
  "data": {
    "user": {
      "id": "...",
      "name": "John Doe",
      "email": "john@example.com"
    },
    "token": "eyJhbGc..."
  }
}
```

#### Get Current User
```
GET /api/auth/me
Authorization: Bearer {token}

Response (200):
{
  "success": true,
  "data": {
    "user": {
      "id": "...",
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
}
```

### Upload Routes

#### Upload PDF File
```
POST /api/uploads
Authorization: Bearer {token}
Content-Type: multipart/form-data

Form Data:
- file: <PDF file>

Response (201):
{
  "success": true,
  "message": "File uploaded and classified successfully",
  "data": {
    "upload": {
      "id": "...",
      "fileName": "document.pdf",
      "label": "Invoice",
      "confidence": 95.5,
      "uploadedAt": "2024-05-13T..."
    }
  }
}
```

#### Get Upload History
```
GET /api/uploads/history?page=1&limit=10&sort=-createdAt
Authorization: Bearer {token}

Response (200):
{
  "success": true,
  "message": "Upload history retrieved successfully",
  "data": {
    "uploads": [
      {
        "id": "...",
        "fileName": "document.pdf",
        "label": "Invoice",
        "confidence": 95.5,
        "status": "completed",
        "uploadedAt": "2024-05-13T..."
      }
    ],
    "pagination": {
      "currentPage": 1,
      "totalPages": 5,
      "totalCount": 42,
      "limit": 10
    }
  }
}
```

#### Get Single Upload
```
GET /api/uploads/:id
Authorization: Bearer {token}

Response (200):
{
  "success": true,
  "data": {
    "upload": {
      "id": "...",
      "fileName": "document.pdf",
      "label": "Invoice",
      "confidence": 95.5,
      "status": "completed",
      "uploadedAt": "2024-05-13T..."
    }
  }
}
```

#### Delete Upload
```
DELETE /api/uploads/:id
Authorization: Bearer {token}

Response (200):
{
  "success": true,
  "message": "Upload deleted successfully"
}
```

## 🚀 Running the Server

### Development Mode
```bash
npm run dev
```
Server runs with auto-reload on file changes using Nodemon.

### Production Mode
```bash
npm start
```

### Expected Output
```
╔════════════════════════════════════════╗
║  🚀 Server running on port 5000        ║
║  🌍 Environment: development           ║
║  📡 MongoDB: Connected                 ║
╚════════════════════════════════════════╝
```

## ⚠️ Error Handling

The API returns consistent error responses:

```json
{
  "success": false,
  "message": "Error description"
}
```

### Common Error Codes

| Status | Error | Solution |
|--------|-------|----------|
| 400 | Bad Request | Check request format and required fields |
| 401 | Unauthorized | Missing or invalid JWT token |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Check server logs |

## 🔐 Security Features

- JWT token-based authentication
- Password hashing with bcrypt (10 salt rounds)
- Input validation on all routes
- CORS protection
- File type validation (PDF only)
- File size limits
- MongoDB injection prevention
- XSS protection via JSON parsing

## 📊 Database Models

### User Model
```javascript
{
  name: String (required, 2-50 chars),
  email: String (required, unique, valid email),
  password: String (required, hashed, 6+ chars),
  createdAt: Date,
  updatedAt: Date
}
```

### Upload Model
```javascript
{
  userId: ObjectId (ref: User),
  originalFileName: String,
  predictedLabel: String,
  confidence: Number (0-100),
  filePath: String,
  fileSize: Number,
  status: String (uploaded|processing|completed|failed),
  error: String,
  createdAt: Date,
  updatedAt: Date
}
```

## 🌐 CORS Configuration

The server accepts requests from:
- Development: `http://localhost:3000`
- Production: URL from `CLIENT_URL` environment variable

To modify, edit the CORS configuration in `server.js`.

## 🐛 Troubleshooting

### MongoDB Connection Error
```
✗ Error connecting to MongoDB: connect ECONNREFUSED
```
**Solution:** Ensure MongoDB is running and `MONGODB_URI` is correct.

### JWT Secret Not Defined
```
JWT_SECRET is not defined in environment variables
```
**Solution:** Add `JWT_SECRET` to `.env` file.

### Port Already in Use
```
Error: listen EADDRINUSE: address already in use :::5000
```
**Solution:** Change `PORT` in `.env` or kill process using port 5000.

### ML Service Connection Error
```
Error: connect ECONNREFUSED from ML service
```
**Solution:** Ensure Python Flask service is running on `ML_SERVICE_URL`.

## 📝 Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017/ai-document-classifier` |
| `JWT_SECRET` | Secret key for JWT signing | (required) |
| `JWT_EXPIRE` | JWT expiration time | `7d` |
| `PORT` | Server port | `5000` |
| `NODE_ENV` | Environment mode | `development` |
| `ML_SERVICE_URL` | Python ML service endpoint | `http://localhost:5001/classify` |
| `MAX_FILE_SIZE` | Max upload size in bytes | `10485760` (10MB) |
| `UPLOAD_TEMP_DIR` | Temporary upload directory | `./uploads/temp` |

## 📈 Performance Optimization

- Database indexes on `userId` and `createdAt` for faster queries
- Lean queries for upload history to reduce memory usage
- Pagination support for large datasets
- Temporary file cleanup after processing
- Connection pooling via Mongoose

## 🚀 Production Deployment

1. **Update Environment Variables**
   ```env
   NODE_ENV=production
   JWT_SECRET=<strong-secret-key>
   MONGODB_URI=<production-mongodb-url>
   ML_SERVICE_URL=<production-ml-service>
   CLIENT_URL=<production-client-url>
   ```

2. **Install Production Dependencies**
   ```bash
   npm install --production
   ```

3. **Start Server**
   ```bash
   npm start
   ```

4. **Monitor Logs**
   ```bash
   pm2 start server.js --name "ai-classifier"
   pm2 logs ai-classifier
   ```

## 📄 License

ISC

## 🤝 Support

For issues or questions, check:
- MongoDB docs: https://docs.mongodb.com/
- Express docs: https://expressjs.com/
- JWT docs: https://jwt.io/
- Mongoose docs: https://mongoosejs.com/

---

**Happy Coding! 🎉**
