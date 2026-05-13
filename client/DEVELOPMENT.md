# Development Tips & Best Practices

## Local Development Setup

### Initial Setup
```bash
# Clone and install
git clone <repo-url>
cd client
npm install

# Copy environment file
cp .env.example .env

# Start development server
npm run dev
```

### Development Server
- Runs on `http://localhost:3000`
- Hot Module Replacement (HMR) enabled
- API proxy to `http://localhost:5000`
- Browser opens automatically

## Backend Requirements

Ensure backend API is running with these endpoints:

```
POST   /api/auth/login           # { email, password } → { token, user }
POST   /api/auth/register        # { firstName, lastName, email, password } → { token, user }
GET    /api/auth/verify          # Verify JWT token validity
POST   /api/documents/upload     # Upload PDF files (multipart/form-data)
GET    /api/documents/history    # Get documents with pagination
DELETE /api/documents/:id        # Delete a document
```

## Debugging

### Browser DevTools

**Console Tab**
```javascript
// Check authentication
localStorage.getItem('token')
localStorage.getItem('user')

// Check API responses
console.log(response)

// Clear storage
localStorage.clear()
```

**Network Tab**
- Monitor API calls
- Check request/response headers
- Verify Authorization header: `Bearer <token>`
- Check response status codes

**Application Tab**
- View localStorage contents
- Clear cache if needed
- Check Cookies

### React DevTools
- Install React DevTools browser extension
- Inspect component tree
- Check props and state
- Monitor re-renders

### Vite DevTools
- Check for module boundaries
- Verify HMR connectivity
- Monitor build performance

## Common Debugging Scenarios

### Login Not Working
```javascript
// 1. Check if backend is running
curl http://localhost:5000/api/auth/login -X POST

// 2. Check request payload
// In Network tab, verify body is correct JSON

// 3. Check response
// Should return { token: "...", user: {...} }

// 4. Verify token storage
localStorage.getItem('token') // Should exist after login
```

### Upload Fails
```javascript
// 1. Check file type
// Only PDFs allowed - verify in FileUpload.jsx validation

// 2. Check backend endpoint
curl -X POST http://localhost:5000/api/documents/upload \
  -F "files=@test.pdf" \
  -H "Authorization: Bearer <token>"

// 3. Check file size
console.log(file.size) // in bytes

// 4. Check Content-Type
// Should be multipart/form-data (Axios handles this)
```

### History Not Loading
```javascript
// 1. Check backend response
// Network tab → GET /api/documents/history → Response

// 2. Verify token is sent
// Headers should include: Authorization: Bearer <token>

// 3. Check pagination params
// URL should have: ?page=1&limit=10
```

## Code Style Guidelines

### Component Structure
```jsx
// Good component structure
import React, { useState, useEffect } from 'react';
import '../styles/component.css';

const MyComponent = ({ prop1, prop2, onEvent }) => {
  const [state, setState] = useState(null);

  useEffect(() => {
    // Side effects
  }, []);

  const handleClick = () => {
    // Event handler
  };

  return (
    <div className="my-component">
      {/* JSX */}
    </div>
  );
};

export default MyComponent;
```

### CSS Naming Convention
```css
/* Component container */
.component-name {
  /* styles */
}

/* Child elements */
.component-name__child {
  /* styles */
}

/* Modifier states */
.component-name--active {
  /* styles */
}

.component-name--disabled {
  /* styles */
}

/* Nested modifiers */
.component-name__child--error {
  /* styles */
}
```

### Error Handling
```javascript
// Always wrap API calls in try-catch
try {
  const result = await apiCall();
  // Handle success
} catch (error) {
  const message = error.response?.data?.message || 'Something went wrong';
  console.error('Operation failed:', message);
  // Show error to user
}
```

### Props Validation
```javascript
// Use descriptive prop names
const MyComponent = ({
  isLoading,      // boolean - indicates loading state
  errorMessage,   // string - error to display
  onSubmit,       // function - called when form submitted
  items,          // array - list of items to display
}) => {
  // Component code
};
```

## Performance Tips

### Avoid Re-renders
```javascript
// Bad - creates new function on each render
<button onClick={() => handleClick(id)}>Click</button>

// Good - use useCallback for complex handlers
const handleClick = useCallback((id) => {
  // Handle click
}, []);
<button onClick={() => handleClick(id)}>Click</button>
```

### Optimize Dependencies
```javascript
// Bad - useEffect runs on every render
useEffect(() => {
  fetchData();
}, []); // Missing dependencies

// Good - only run when needed
useEffect(() => {
  fetchData();
}, [userId]); // Explicit dependencies
```

### Use Lazy Loading
```javascript
// Lazy load heavy components if needed
const Dashboard = lazy(() => import('./pages/Dashboard'));
```

### Monitor Performance
```bash
# Build analysis
npm run build -- --mode analyze

# Check bundle size
npm run build && npm run preview
```

## Testing Tips

### Test Authentication
1. Register new account
2. Login with credentials
3. Verify token in localStorage
4. Refresh page - should stay logged in
5. Logout - should clear storage and redirect

### Test File Upload
1. Try uploading non-PDF - should show error
2. Upload valid PDF - should succeed
3. Verify file appears in history
4. Delete file - should remove from list

### Test Error Handling
1. Disconnect from internet - should show error
2. Kill backend - API calls should fail gracefully
3. Expire token - should redirect to login
4. Try accessing dashboard without login - should redirect

## Browser Compatibility

Test in multiple browsers:
- Chrome/Edge (Chromium-based)
- Firefox
- Safari
- Mobile browsers (iPhone, Android)

Use BrowserStack or similar for extensive testing.

## Accessibility Checklist

- ✅ Semantic HTML elements
- ✅ Proper heading hierarchy
- ✅ Alt text for images
- ✅ Form labels associated with inputs
- ✅ Keyboard navigation support
- ✅ Color contrast ratios
- ✅ Focus indicators visible
- ✅ ARIA labels where needed

## Production Deployment

### Pre-deployment Checklist
- [ ] All tests passing
- [ ] No console errors
- [ ] No console warnings (except third-party)
- [ ] Environment variables configured
- [ ] API endpoints verified
- [ ] CORS properly configured
- [ ] Authentication flow tested
- [ ] File upload tested
- [ ] Responsive design verified
- [ ] Performance optimized

### Environment Variables (Production)
```env
VITE_API_BASE_URL=https://api.yourdomain.com
VITE_API_TIMEOUT=30000
```

### Build and Deploy
```bash
# Build
npm run build

# Output is in dist/ folder

# Deploy dist/ folder to:
# - Vercel
# - Netlify
# - AWS S3 + CloudFront
# - Any static hosting
```

### SPA Configuration
Ensure web server redirects all routes to index.html:

**Nginx**
```nginx
location / {
  try_files $uri /index.html;
}
```

**Apache**
```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

## Version Management

### Update Dependencies
```bash
# Check outdated packages
npm outdated

# Update specific package
npm update package-name

# Update all packages
npm update
```

### Lock File Management
```bash
# Always commit package-lock.json
# Install exact versions from lock file
npm ci  # Instead of npm install in CI/CD
```

## Git Workflow

```bash
# Create feature branch
git checkout -b feature/feature-name

# Make changes and commit
git add .
git commit -m "feat: add feature"

# Push to remote
git push origin feature/feature-name

# Create Pull Request
# Get code reviewed
# Merge to main

# Pull latest
git checkout main
git pull origin main
```

## Common Commands Reference

```bash
# Development
npm run dev              # Start dev server
npm run build            # Build for production
npm run preview          # Preview production build
npm run lint             # Run ESLint

# Debugging
npm run dev -- --debug   # Debug mode

# Cleaning
rm -rf node_modules      # Remove dependencies
rm package-lock.json     # Remove lock file
npm install              # Reinstall from scratch
```

## Resources

- [React Documentation](https://react.dev)
- [React Router Documentation](https://reactrouter.com)
- [Vite Documentation](https://vitejs.dev)
- [Axios Documentation](https://axios-http.com)
- [MDN Web Docs](https://developer.mozilla.org)
- [Web Accessibility](https://www.w3.org/WAI/)

## Support & Help

- Check error messages in browser console
- Review network tab for API issues
- Verify backend is running
- Check .env configuration
- Review component props
- Check localStorage in DevTools

## Useful VSCode Extensions

- ES7+ React/Redux/React-Native snippets
- Prettier - Code formatter
- ESLint
- Thunder Client (API testing)
- React DevTools
- Vite

## Quick Fixes

### Port already in use
```bash
# Kill process on port 3000
# macOS/Linux
lsof -i :3000 | grep LISTEN | awk '{print $2}' | xargs kill

# Windows
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Clear cache
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and reinstall
rm -rf node_modules && npm install
```

### CORS Issues
- Verify backend has CORS enabled
- Check API_BASE_URL in .env
- Test with curl command

### Token Not Persisting
- Check if localStorage is enabled
- Verify token is being set: `localStorage.setItem('token', token)`
- Clear localStorage and login again
