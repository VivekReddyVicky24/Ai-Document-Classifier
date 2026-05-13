# Troubleshooting Guide - Backend Server

Common issues and solutions for the AI Document Classifier backend.

## MongoDB Connection Issues

### Problem: "connect ECONNREFUSED"
```
Error: MongoNetworkError: connect ECONNREFUSED 127.0.0.1:27017
```

**Solutions:**
1. Check MongoDB is running:
   ```bash
   mongosh
   ```
   If fails, start MongoDB:
   ```bash
   mongod
   ```

2. Verify MONGODB_URI in `.env`:
   ```env
   MONGODB_URI=mongodb://localhost:27017/ai-document-classifier
   ```

3. For MongoDB Atlas, check connection string:
   ```env
   MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/ai-document-classifier
   ```

4. Check firewall rules (if remote):
   ```bash
   # MongoDB default port
   telnet localhost 27017
   ```

---

## JWT Authentication Issues

### Problem: "JWT_SECRET is not defined"
```
Error: JWT_SECRET is not defined in environment variables
```

**Solution:**
1. Add JWT_SECRET to `.env`:
   ```env
   JWT_SECRET=your_secure_secret_key_here_min_32_chars
   ```

2. Restart server:
   ```bash
   npm run dev
   ```

### Problem: "Invalid token"
```
Error: Not authorized to access this route
```

**Solutions:**
1. Check token in Authorization header:
   ```bash
   # Correct format:
   Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
   
   # Incorrect:
   Authorization: eyJhbGciOiJIUzI1NiIs... (missing "Bearer ")
   ```

2. Token may be expired - login again:
   ```bash
   curl -X POST http://localhost:5000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"user@example.com","password":"password"}'
   ```

3. Check JWT_SECRET matches between registration and verification

### Problem: "Token verification failed"
```
Error: jwt malformed
```

**Solution:**
- Token is corrupted or incomplete
- Re-login to get new token
- Check token is fully copied (no truncation)

---

## Port Issues

### Problem: "Port already in use"
```
Error: listen EADDRINUSE: address already in use :::5000
```

**Solutions:**
1. Change PORT in `.env`:
   ```env
   PORT=5001
   ```

2. Or kill process using port:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   
   # Linux/Mac
   lsof -i :5000
   kill -9 <PID>
   ```

3. Or stop other Node processes:
   ```bash
   ps aux | grep node
   ```

---

## File Upload Issues

### Problem: "Only PDF files are allowed"
```
Error: Only PDF files are allowed
```

**Solutions:**
1. Ensure file is PDF format:
   - Check file extension: `.pdf`
   - Check MIME type: `application/pdf`

2. Use valid PDF file:
   ```bash
   curl -X POST http://localhost:5000/api/uploads \
     -H "Authorization: Bearer TOKEN" \
     -F "file=@document.pdf"  # Must be .pdf
   ```

### Problem: "File too large"
```
Error: File exceeds maximum size
```

**Solutions:**
1. Check file size:
   ```bash
   ls -lh document.pdf  # Show size
   ```

2. Increase limit in `.env`:
   ```env
   MAX_FILE_SIZE=52428800  # 50MB
   ```

3. Or upload smaller file

### Problem: "No file uploaded"
```
Error: Please upload a PDF file
```

**Solution:**
Check file parameter in request:
```bash
# Correct
curl -X POST http://localhost:5000/api/uploads \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@document.pdf"  # Parameter name: "file"

# Incorrect (parameter name wrong)
curl -X POST http://localhost:5000/api/uploads \
  -H "Authorization: Bearer TOKEN" \
  -F "document=@document.pdf"  # Should be "file"
```

---

## ML Service Integration Issues

### Problem: "Error processing file"
```
Error: Error processing file: connect ECONNREFUSED
```

**Solutions:**
1. Check Python ML service is running:
   ```bash
   curl http://localhost:5001/classify
   ```

2. Verify ML_SERVICE_URL in `.env`:
   ```env
   ML_SERVICE_URL=http://localhost:5001/classify
   ```

3. Check ML service is accessible:
   ```bash
   # Test connection
   curl -X POST http://localhost:5001/classify \
     -F "file=@test.pdf"
   ```

4. Check firewall allows port 5001

5. Verify Flask service response format:
   ```json
   {
     "label": "Invoice",
     "confidence": 95.5
   }
   ```

### Problem: ML service returns error
```
Error: Invalid response from ML service
```

**Solutions:**
1. Check response contains `label` field
2. Verify response format is JSON
3. Check ML service logs for errors
4. Test ML service independently

---

## CORS Issues

### Problem: "CORS policy: Cross-Origin Request Blocked"
```
Access to XMLHttpRequest at 'http://localhost:5000/api/...' 
from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solutions:**
1. Check CORS is enabled in `server.js` (should be default)

2. Verify Client URL in CORS config:
   ```javascript
   // In server.js - already configured
   cors({
     origin: process.env.NODE_ENV === 'production'
       ? process.env.CLIENT_URL || 'http://localhost:3000'
       : 'http://localhost:3000',
     credentials: true,
   })
   ```

3. For production, set CLIENT_URL:
   ```env
   CLIENT_URL=https://yourdomain.com
   ```

---

## Database Model Issues

### Problem: "Duplicate key error"
```
Error: E11000 duplicate key error collection
```

**Solution:**
Email already exists. Register with different email:
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name":"John",
    "email":"newemail@example.com",
    "password":"password123"
  }'
```

### Problem: "Validation error"
```
Error: Validation failed: email: Email is required
```

**Solutions:**
1. Check all required fields are provided:
   - name (2-50 characters)
   - email (valid email format)
   - password (6+ characters)

2. Example valid request:
   ```bash
   curl -X POST http://localhost:5000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{
       "name":"John Doe",
       "email":"john@example.com",
       "password":"password123"
     }'
   ```

---

## Environment Variables Issues

### Problem: "Variable not defined"
```
Error: MONGODB_URI is not defined in environment variables
```

**Solutions:**
1. Create `.env` file if not exists:
   ```bash
   # Copy from template
   cp .env.example .env
   ```

2. Check `.env` file exists:
   ```bash
   ls -la .env
   ```

3. Verify variable is spelled correctly (case-sensitive)

4. Restart server after changing `.env`:
   ```bash
   npm run dev
   ```

5. Don't use spaces in values:
   ```env
   # Correct
   JWT_SECRET=abc123def456
   
   # Incorrect
   JWT_SECRET = abc123def456  # Extra spaces
   ```

---

## Validation Issues

### Problem: "Please provide a valid email"
```
Error: Please provide a valid email
```

**Solution:**
Email must be valid format:
```
Correct: john@example.com
Incorrect: john@invalid
Incorrect: @example.com
Incorrect: john
```

### Problem: "Password must be at least 6 characters"
```
Error: Password must be at least 6 characters
```

**Solution:**
Use password with 6+ characters:
```
✓ password123
✓ 123456
✗ 12345
✗ pass
```

### Problem: "Name must be between 2 and 50 characters"
```
Error: Name must be between 2 and 50 characters
```

**Solution:**
Name must be 2-50 characters:
```
✓ John Doe
✓ Jo  (minimum 2)
✓ A very long name (up to 50 characters)
✗ J  (only 1 character)
✗ Very long name exceeding fifty characters total length...  (too long)
```

---

## Server Startup Issues

### Problem: "Cannot find module"
```
Error: Cannot find module 'express'
```

**Solution:**
Install dependencies:
```bash
npm install
```

### Problem: "SyntaxError: Unexpected token"
```
SyntaxError: Unexpected token u in JSON at position 0
```

**Solutions:**
1. Check `.env` syntax (should be simple key=value)
2. Fix JSON in request body (if using JSON)
3. Check for invalid characters in `.env`

### Problem: Server starts but won't accept connections
```
Server listening but: Connection refused
```

**Solutions:**
1. Check PORT in `.env` matches request URL
2. Check firewall allows the port
3. Verify address is correct (localhost vs 0.0.0.0)
4. Check for error logs above

---

## Database Query Issues

### Problem: "Upload not found"
```
Error: Upload not found
```

**Solutions:**
1. Verify upload ID is correct (MongoDB ObjectId format)
2. Check upload belongs to logged-in user
3. List user's uploads:
   ```bash
   curl http://localhost:5000/api/uploads/history \
     -H "Authorization: Bearer TOKEN"
   ```

### Problem: Empty upload history
```
"uploads": []
```

**Solutions:**
1. Check user is logged in (correct token)
2. Verify uploads were created successfully
3. Check database directly:
   ```bash
   mongosh
   > db.uploads.find()
   ```

---

## Performance Issues

### Problem: Slow file uploads
**Solutions:**
1. Check file size (large files take time)
2. Increase timeout in client
3. Check network connection
4. Verify ML service performance

### Problem: High memory usage
**Solution:**
```bash
# Restart server
npm run dev

# Or increase memory limit
node --max-old-space-size=4096 server.js
```

### Problem: Database queries slow
**Solutions:**
1. Add indexes (already configured)
2. Use pagination:
   ```bash
   ?page=1&limit=10
   ```
3. Check MongoDB performance

---

## Development Issues

### Problem: Changes not reflected after editing
**Solution:**
Restart development server:
```bash
# Stop: Ctrl+C
# Start again:
npm run dev
```

(Nodemon should auto-reload, if not, restart manually)

### Problem: "Unhandled promise rejection"
```
Error: Unhandled Rejection: ...
```

**Solution:**
Check server logs for error details. Error is caught and logged.

---

## Production Issues

### Problem: "Cannot find .env in production"
**Solution:**
Set environment variables directly:
```bash
# Heroku
heroku config:set JWT_SECRET=value

# Docker
-e JWT_SECRET=value

# VPS
export JWT_SECRET=value
```

### Problem: Database connection timeout in production
**Solutions:**
1. Check VPN/firewall rules
2. Verify connection string is correct
3. Check database credentials
4. Increase timeout settings
5. Use connection pooling

---

## Getting Help

If issue not listed:

1. **Check logs:**
   ```bash
   npm run dev  # Shows all output
   ```

2. **Test endpoints:**
   ```bash
   curl http://localhost:5000/health
   ```

3. **Check environment:**
   ```bash
   # Verify .env is loaded
   node -e "require('dotenv').config(); console.log(process.env.JWT_SECRET)"
   ```

4. **Review documentation:**
   - README.md - General info
   - API_DOCUMENTATION.md - Endpoint details
   - DEPLOYMENT.md - Production issues

5. **Check dependencies:**
   ```bash
   npm list
   npm audit
   ```

---

## Quick Diagnostic Script

```bash
#!/bin/bash
echo "=== Diagnostics ==="
echo "Node version:"
node -v
echo ""
echo "NPM version:"
npm -v
echo ""
echo "Dependencies:"
npm list --depth=0
echo ""
echo "MongoDB check:"
mongosh --eval "db.version()" 2>/dev/null || echo "MongoDB not running"
echo ""
echo ".env check:"
[ -f .env ] && echo ".env file exists" || echo ".env file missing"
echo ""
echo "Server test:"
npm run dev &
sleep 2
curl http://localhost:5000/health 2>/dev/null || echo "Server not responding"
```

---

**Still stuck?** Check server logs carefully - they usually contain the root cause! 🔍
