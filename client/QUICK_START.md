# AI Document Classifier Frontend - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### 1. Install Dependencies
```bash
npm install
```

### 2. Configure Environment
Create or update `.env` file:
```env
VITE_API_BASE_URL=http://localhost:5000
VITE_API_TIMEOUT=30000
```

### 3. Start Development Server
```bash
npm run dev
```

Access the app at: **http://localhost:3000**

## 📋 What's Included

### Pages
- ✅ **Login** - Authenticate with email/password
- ✅ **Register** - Create new account
- ✅ **Dashboard** - Upload PDFs and view history

### Components
- ✅ **Navbar** - Navigation and user menu
- ✅ **FileUpload** - Drag-and-drop PDF upload
- ✅ **UploadHistory** - Document history table
- ✅ **ProtectedRoute** - Route authentication guard

### Features
- ✅ JWT authentication
- ✅ Token storage in localStorage
- ✅ Drag-and-drop file upload
- ✅ Multiple file selection
- ✅ Upload history with pagination
- ✅ Error handling & loading states
- ✅ Responsive mobile design
- ✅ Modern clean UI

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `src/App.jsx` | Main app component with routing |
| `src/context/AuthContext.jsx` | Authentication state management |
| `src/utils/api.js` | Axios API client |
| `src/pages/` | Page components |
| `src/components/` | Reusable components |
| `src/styles/` | Component CSS files |
| `.env` | Environment configuration |

## 🛠️ Available Commands

```bash
# Development
npm run dev           # Start dev server

# Build
npm run build         # Build for production
npm run preview       # Preview production build

# Lint
npm run lint          # Run ESLint
```

## 📱 Responsive Breakpoints

- Desktop: 1024px and above
- Tablet: 768px to 1023px
- Mobile: Below 768px

## 🎨 Styling

The app uses **plain CSS only** (no Tailwind):
- Global variables in `src/styles/index.css`
- Component-specific styles in dedicated CSS files
- Consistent color scheme and spacing
- Smooth animations and transitions

## 🔐 Authentication

```javascript
// Login
await authContext.login(email, password);

// Register
await authContext.register(firstName, lastName, email, password);

// Logout
authContext.logout();

// Check auth status
authContext.isAuthenticated
```

## 📤 File Upload

```javascript
// Upload handler
const handleUploadSuccess = (response) => {
  console.log('Files uploaded:', response.data);
  // Refresh upload history
};

const handleUploadError = (error) => {
  console.log('Upload failed:', error);
};
```

## 📊 API Integration

All API calls go through the `api.js` client with:
- Automatic JWT token injection
- Error handling and redirects
- Timeout configuration
- Request/response interceptors

### Upload Files
```javascript
const formData = new FormData();
formData.append('files', file1);
formData.append('files', file2);
const response = await documentAPI.uploadFiles(formData);
```

### Get History
```javascript
const response = await documentAPI.getHistory({ page: 1, limit: 10 });
```

## 🚨 Debugging

### Check Browser Console
- View error messages
- Check network requests in DevTools
- Verify token in localStorage

### Network Issues
1. Ensure backend API is running
2. Check `VITE_API_BASE_URL` configuration
3. Verify CORS settings on backend

### Auth Issues
1. Check token in localStorage: `localStorage.getItem('token')`
2. Verify token format: `Bearer <token>`
3. Check user data: `localStorage.getItem('user')`

## 📦 Production Build

```bash
# Create optimized build
npm run build

# Test production build
npm run preview

# Deploy dist/ folder to your hosting
```

## 🎯 Next Steps

1. ✅ Backend API should be running at `http://localhost:5000`
2. ✅ Test authentication (register/login)
3. ✅ Test file upload (dashboard page)
4. ✅ Test upload history retrieval
5. ✅ Verify all API endpoints working

## 📝 API Endpoints Expected

Backend should provide these endpoints:

```
POST   /api/auth/login         # Login user
POST   /api/auth/register      # Register user
GET    /api/auth/verify        # Verify token
POST   /api/documents/upload   # Upload files
GET    /api/documents/history  # Get history
DELETE /api/documents/:id      # Delete document
```

## 💡 Tips

- Use React DevTools for component debugging
- Check Network tab for API issues
- Use browser DevTools Lighthouse for performance
- Enable source maps in development for easier debugging

## 🆘 Common Issues

**Port 3000 already in use?**
```bash
# Change port in vite.config.js
npm run dev -- --port 3001
```

**Token expiration?**
- App automatically redirects to login on 401
- Clear localStorage and login again

**API not found?**
- Verify backend running on `http://localhost:5000`
- Check CORS is enabled on backend
- Update `VITE_API_BASE_URL` if needed

## 📚 Resources

- React Documentation: https://react.dev
- Vite Documentation: https://vitejs.dev
- React Router: https://reactrouter.com
- Axios: https://axios-http.com

---

Happy coding! 🎉
