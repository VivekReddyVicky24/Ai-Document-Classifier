# API Documentation - AI Document Classifier

Complete API reference for the backend server.

## Base URL
```
http://localhost:5000/api
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_token>
```

## Response Format

All responses follow this format:

```json
{
  "success": true/false,
  "message": "Description",
  "data": {} // Optional
}
```

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Server Error |

---

## Authentication Endpoints

### 1. Register User

**Endpoint:** `POST /auth/register`

**Authentication:** ❌ Not required

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "password123"
}
```

**Validation Rules:**
- `name`: 2-50 characters, required
- `email`: valid email format, unique, required
- `password`: minimum 6 characters, required

**Response (201):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "507f1f77bcf86cd799439011",
      "name": "John Doe",
      "email": "john@example.com"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Responses:**
- 400: Missing fields, invalid email, email already exists, password too short
- 500: Server error

**Example:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "password123"
  }'
```

---

### 2. Login User

**Endpoint:** `POST /auth/login`

**Authentication:** ❌ Not required

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

**Validation Rules:**
- `email`: required, must be valid email format
- `password`: required

**Response (200):**
```json
{
  "success": true,
  "message": "Logged in successfully",
  "data": {
    "user": {
      "id": "507f1f77bcf86cd799439011",
      "name": "John Doe",
      "email": "john@example.com"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

**Error Responses:**
- 400: Missing email or password
- 401: Invalid credentials
- 500: Server error

**Example:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "password123"
  }'
```

---

### 3. Get Current User

**Endpoint:** `GET /auth/me`

**Authentication:** ✅ Required

**Request Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "507f1f77bcf86cd799439011",
      "name": "John Doe",
      "email": "john@example.com"
    }
  }
}
```

**Error Responses:**
- 401: Missing or invalid token
- 404: User not found
- 500: Server error

**Example:**
```bash
curl http://localhost:5000/api/auth/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

## Upload Endpoints

### 4. Upload PDF File

**Endpoint:** `POST /uploads`

**Authentication:** ✅ Required

**Request Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body:**
- `file`: PDF file (multipart form data)

**File Constraints:**
- Must be PDF format
- Maximum size: 10MB (configurable)
- Content-Type: application/pdf

**Response (201):**
```json
{
  "success": true,
  "message": "File uploaded and classified successfully",
  "data": {
    "upload": {
      "id": "507f1f77bcf86cd799439012",
      "fileName": "document.pdf",
      "label": "Invoice",
      "confidence": 95.5,
      "uploadedAt": "2024-05-13T10:30:00.000Z"
    }
  }
}
```

**Error Responses:**
- 400: No file uploaded, invalid file type
- 401: Missing or invalid token
- 500: ML service error, file processing error

**Example:**
```bash
curl -X POST http://localhost:5000/api/uploads \
  -H "Authorization: Bearer <token>" \
  -F "file=@document.pdf"
```

---

### 5. Get Upload History

**Endpoint:** `GET /uploads/history`

**Authentication:** ✅ Required

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `limit` (optional): Items per page (default: 10, max: 100)
- `sort` (optional): Sort field with order (default: -createdAt)

**Request Example:**
```
GET /uploads/history?page=1&limit=10&sort=-createdAt
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Upload history retrieved successfully",
  "data": {
    "uploads": [
      {
        "id": "507f1f77bcf86cd799439012",
        "fileName": "document.pdf",
        "label": "Invoice",
        "confidence": 95.5,
        "status": "completed",
        "uploadedAt": "2024-05-13T10:30:00.000Z"
      },
      {
        "id": "507f1f77bcf86cd799439013",
        "fileName": "report.pdf",
        "label": "Report",
        "confidence": 88.3,
        "status": "completed",
        "uploadedAt": "2024-05-13T09:15:00.000Z"
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

**Error Responses:**
- 401: Missing or invalid token
- 500: Server error

**Example:**
```bash
curl "http://localhost:5000/api/uploads/history?page=1&limit=10" \
  -H "Authorization: Bearer <token>"
```

---

### 6. Get Single Upload

**Endpoint:** `GET /uploads/:id`

**Authentication:** ✅ Required

**URL Parameters:**
- `id`: Upload document ID (MongoDB ObjectId)

**Request Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "upload": {
      "id": "507f1f77bcf86cd799439012",
      "fileName": "document.pdf",
      "label": "Invoice",
      "confidence": 95.5,
      "status": "completed",
      "uploadedAt": "2024-05-13T10:30:00.000Z"
    }
  }
}
```

**Error Responses:**
- 401: Missing or invalid token
- 404: Upload not found
- 500: Server error

**Example:**
```bash
curl http://localhost:5000/api/uploads/507f1f77bcf86cd799439012 \
  -H "Authorization: Bearer <token>"
```

---

### 7. Delete Upload

**Endpoint:** `DELETE /uploads/:id`

**Authentication:** ✅ Required

**URL Parameters:**
- `id`: Upload document ID (MongoDB ObjectId)

**Request Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "message": "Upload deleted successfully"
}
```

**Error Responses:**
- 401: Missing or invalid token
- 404: Upload not found
- 500: Server error

**Example:**
```bash
curl -X DELETE http://localhost:5000/api/uploads/507f1f77bcf86cd799439012 \
  -H "Authorization: Bearer <token>"
```

---

## Data Models

### User

```javascript
{
  _id: ObjectId,
  name: String,           // 2-50 characters
  email: String,          // Unique email
  password: String,       // Hashed with bcrypt
  createdAt: Date,
  updatedAt: Date
}
```

### Upload

```javascript
{
  _id: ObjectId,
  userId: ObjectId,       // Reference to User
  originalFileName: String,
  predictedLabel: String,
  confidence: Number,     // 0-100
  filePath: String,       // Path to uploaded file
  fileSize: Number,       // File size in bytes
  status: String,         // "uploaded", "processing", "completed", "failed"
  error: String,          // Error message if failed
  createdAt: Date,
  updatedAt: Date
}
```

---

## Error Examples

### Invalid Email Format
```json
{
  "success": false,
  "message": "Please provide a valid email"
}
```

### Email Already Exists
```json
{
  "success": false,
  "message": "User with this email already exists"
}
```

### Invalid Token
```json
{
  "success": false,
  "message": "Not authorized to access this route"
}
```

### File Upload Error
```json
{
  "success": false,
  "message": "Only PDF files are allowed"
}
```

### ML Service Error
```json
{
  "success": false,
  "message": "Error processing file"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider adding:
- Express-rate-limit for DDoS protection
- Request throttling per user
- File upload rate limiting

---

## CORS Configuration

The API accepts requests from:
- Development: `http://localhost:3000`
- Production: URL from `CLIENT_URL` environment variable

---

## Postman Collection

To import into Postman:
1. Copy the base URL: `http://localhost:5000/api`
2. Create requests for each endpoint
3. Use the examples above as request bodies
4. Include Authorization header for protected routes

---

## Common Integration Issues

### Issue: CORS Error
**Solution:** Ensure Client URL is configured in `CLIENT_URL` env variable

### Issue: 401 Unauthorized
**Solution:** Token may be expired. Re-login to get new token.

### Issue: 500 ML Service Error
**Solution:** Ensure Flask service is running on `ML_SERVICE_URL`

### Issue: File Upload Fails
**Solution:** Check file is PDF, size < 10MB, and token is valid

---

## Performance Tips

- Pagination limit: Use reasonable limits (10-50 items)
- Upload: Large files may take time, consider async processing
- Queries: Use filtering to reduce data transfer
- Cache: Implement client-side caching for upload history

---

Last Updated: May 13, 2024
