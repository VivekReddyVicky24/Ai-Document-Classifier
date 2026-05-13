# Project Structure & File Overview

## Complete Directory Structure

```
ai-document-classifier/client/
│
├── public/                              # Static assets
│   └── (favicon and other static files)
│
├── src/
│   ├── components/                      # Reusable React Components
│   │   ├── FileUpload.jsx              # Drag-and-drop PDF upload component
│   │   ├── Navbar.jsx                   # Navigation bar with user info
│   │   ├── ProtectedRoute.jsx          # Route protection HOC
│   │   └── UploadHistory.jsx           # Upload history table component
│   │
│   ├── context/                         # React Context & Hooks
│   │   └── AuthContext.jsx              # Authentication state management
│   │
│   ├── pages/                           # Page Components
│   │   ├── Dashboard.jsx                # Main dashboard with upload & history
│   │   ├── Login.jsx                    # User login page
│   │   └── Register.jsx                 # User registration page
│   │
│   ├── styles/                          # Component-Specific CSS
│   │   ├── auth.css                     # Login/Register page styles
│   │   ├── dashboard.css                # Dashboard page styles
│   │   ├── fileUpload.css              # File upload component styles
│   │   ├── index.css                    # Global styles & CSS variables
│   │   ├── navbar.css                   # Navigation bar styles
│   │   └── uploadHistory.css           # Upload history table styles
│   │
│   ├── utils/                           # Utility Functions
│   │   ├── api.js                       # Axios HTTP client configuration
│   │   └── authService.js              # Authentication helper functions
│   │
│   ├── App.css                          # Main app container styles
│   ├── App.jsx                          # Main app component with routing
│   ├── index.css                        # Global CSS setup
│   └── main.jsx                         # React DOM entry point
│
├── .env                                 # Environment variables (local)
├── .env.example                         # Example environment variables
├── .gitignore                          # Git ignore rules
├── eslint.config.js                    # ESLint configuration
├── index.html                          # HTML entry point
├── package-lock.json                   # Dependency lock file
├── package.json                        # Project dependencies & scripts
├── QUICK_START.md                      # Quick start guide
├── README.md                           # Original README
├── README_FRONTEND.md                  # Frontend documentation
├── vite.config.js                      # Vite configuration
└── STRUCTURE.md                        # This file
```

## File-by-File Breakdown

### Configuration Files

#### `.env`
Environment variables for development:
```env
VITE_API_BASE_URL=http://localhost:5000
VITE_API_TIMEOUT=30000
```

#### `.env.example`
Template for environment variables - copy to `.env`

#### `vite.config.js`
Vite build configuration including:
- React plugin setup
- Development server settings
- API proxy configuration
- Production build optimization
- Code splitting for vendor libraries

#### `package.json`
Project metadata and dependencies:
- React 19, React DOM 19
- React Router DOM 7
- Axios 1.7
- Dev dependencies for Vite and ESLint

#### `index.html`
HTML entry point for the SPA:
- Root div for React mounting
- Main script entry point
- Meta tags for viewport and SEO

#### `eslint.config.js`
ESLint rules for code quality

### Source Code Files

#### Main Entry Point

**`src/main.jsx`**
- React DOM root rendering
- Mounts App component to #root element
- Enables React StrictMode for development

**`src/App.jsx`**
- Main application component
- React Router setup with BrowserRouter
- AuthProvider wrapper
- Route definitions:
  - `/login` - Login page
  - `/register` - Registration page
  - `/dashboard` - Protected dashboard
  - Catch-all redirect to dashboard

**`src/App.css`**
- Main app container styles
- Flexbox layout for Navbar + Main content
- Full viewport height setup

#### Styling

**`src/index.css`**
- Global CSS variables (colors, spacing, shadows)
- Base element styles (body, h1-h4, forms, buttons)
- Utility classes (loading spinner, messages)
- Responsive design utilities
- Animation keyframes

**`src/styles/index.css` (in styles folder)**
- Duplicate of component-level global styles
- CSS variables definitions
- Consistent theming

**Component-Specific CSS Files:**
- `src/styles/navbar.css` - Navigation styling
- `src/styles/auth.css` - Login/Register page styles
- `src/styles/fileUpload.css` - File upload component
- `src/styles/uploadHistory.css` - History table styling
- `src/styles/dashboard.css` - Dashboard layout and styling

#### Context & State Management

**`src/context/AuthContext.jsx`**
Provides authentication state and methods:
- `user` - Current user object
- `loading` - Loading state
- `error` - Error messages
- `login()` - Login function
- `register()` - Register function
- `logout()` - Logout function
- `isAuthenticated` - Boolean flag
- `useAuth()` - Custom hook for context consumption

#### Utility Functions

**`src/utils/api.js`**
Axios HTTP client with:
- Base URL from environment variables
- Request interceptor for JWT token injection
- Response interceptor for 401 error handling
- Auth API methods:
  - `login()` - POST /api/auth/login
  - `register()` - POST /api/auth/register
  - `verifyToken()` - GET /api/auth/verify
- Document API methods:
  - `uploadFiles()` - POST /api/documents/upload
  - `getHistory()` - GET /api/documents/history
  - `getDocument()` - GET /api/documents/:id
  - `deleteDocument()` - DELETE /api/documents/:id

**`src/utils/authService.js`**
Authentication helper functions:
- `login()` - Handle login and token storage
- `register()` - Handle registration and token storage
- `logout()` - Clear auth from localStorage
- `getToken()` - Retrieve stored token
- `getUser()` - Retrieve stored user data
- `isAuthenticated()` - Check auth status

#### Components

**`src/components/ProtectedRoute.jsx`**
Route protection component:
- Checks authentication status
- Shows loading spinner while checking
- Redirects to login if not authenticated
- Renders children if authenticated

**`src/components/Navbar.jsx`**
Navigation component with:
- Brand logo and name
- Conditional rendering for auth state
- User name display when logged in
- Logout button
- Login/Register links when not authenticated
- Responsive design
- Sticky positioning

**`src/components/FileUpload.jsx`**
File upload component with:
- Drag-and-drop support
- File picker input
- PDF validation
- Multiple file selection
- File list with removal
- Upload button with loading state
- Error handling and display
- File size information

**`src/components/UploadHistory.jsx`**
History table component with:
- Paginated document list
- File name, label, and upload time
- Delete button for each document
- Label color coding by category
- Loading states
- Error handling
- Empty state message
- Pagination controls
- Refresh button

#### Pages

**`src/pages/Login.jsx`**
Login page with:
- Email and password fields
- Form validation
- Error display
- Loading state
- Link to registration page
- Authentication error handling

**`src/pages/Register.jsx`**
Registration page with:
- First name, last name, email, password fields
- Confirm password field
- Form validation
- Password strength checking
- Error display
- Loading state
- Link to login page

**`src/pages/Dashboard.jsx`**
Main dashboard with:
- FileUpload component integration
- UploadHistory component integration
- Success/error message display
- Refresh trigger for upload history
- Message auto-dismiss functionality

### Documentation Files

**`README_FRONTEND.md`**
Comprehensive frontend documentation:
- Features overview
- Project structure explanation
- Setup instructions
- Development guidelines
- API endpoint details
- Authentication flow
- Styling information
- Troubleshooting guide
- Production deployment

**`QUICK_START.md`**
Quick reference guide:
- 5-minute setup
- Key files overview
- Command reference
- API integration examples
- Debugging tips
- Common issues and solutions

**`STRUCTURE.md`** (this file)
Complete file structure and overview

## Data Flow

### Authentication Flow
```
User Input
    ↓
Login/Register Page
    ↓
AuthContext.login() or .register()
    ↓
authService handles API call
    ↓
API response with JWT token
    ↓
Token stored in localStorage
    ↓
User object stored in localStorage
    ↓
AuthContext state updates
    ↓
Redirect to Dashboard
    ↓
ProtectedRoute allows access
```

### File Upload Flow
```
User selects/drags PDF files
    ↓
FileUpload component validates
    ↓
Files shown in preview list
    ↓
User clicks upload
    ↓
FormData created with files
    ↓
documentAPI.uploadFiles() called
    ↓
Axios adds JWT token via interceptor
    ↓
Backend API processes upload
    ↓
Response with classification results
    ↓
Dashboard shows success message
    ↓
UploadHistory component refreshes
    ↓
New document appears in history table
```

### API Interceptor Flow
```
API Request Made
    ↓
Request Interceptor
    ↓
Retrieve token from localStorage
    ↓
Add "Authorization: Bearer {token}" header
    ↓
Send request to backend
    ↓
Receive response
    ↓
Response Interceptor
    ↓
Check status code
    ↓
If 401 → Redirect to login
    ↓
Otherwise → Return response data
    ↓
Component receives data
```

## Environment Variables

| Variable | Type | Default | Purpose |
|----------|------|---------|---------|
| `VITE_API_BASE_URL` | string | http://localhost:5000 | Backend API endpoint |
| `VITE_API_TIMEOUT` | number | 30000 | Request timeout in ms |

## CSS Architecture

### Global CSS Variables
- Colors (primary, secondary, danger, gray palette)
- Spacing scale (2px to 16px units)
- Border radius values
- Box shadows
- Typography settings
- Animation durations

### Responsive Design Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

### CSS Naming Convention
- BEM-like structure: `.component-name__element--modifier`
- Utility classes for common patterns
- Component-specific files for isolation
- Global utilities in index.css

## Component Dependencies

```
App
├── Navbar
├── Router
│   ├── Login (public)
│   ├── Register (public)
│   └── ProtectedRoute
│       └── Dashboard
│           ├── FileUpload
│           │   └── documentAPI
│           └── UploadHistory
│               └── documentAPI
└── AuthProvider
    └── AuthContext
        ├── authService
        ├── api
        └── localStorage
```

## Technology Stack

| Technology | Version | Purpose |
|-----------|---------|---------|
| React | 19.2.5 | UI library |
| React DOM | 19.2.5 | DOM rendering |
| React Router | 7.15.0 | Routing |
| Axios | 1.16.0 | HTTP client |
| Vite | 8.0.10 | Build tool |
| ESLint | 10.2.1 | Code quality |

## Build Process

1. **Development**: `npm run dev` starts Vite dev server on port 3000
2. **Build**: `npm run build` creates optimized production bundle
3. **Optimization**:
   - Code splitting with vendor chunk
   - Minification and tree-shaking
   - CSS optimization
   - Asset optimization

## Performance Metrics

- Lighthouse Performance Score target: 90+
- Initial load time target: < 2s
- Bundle size target: < 250KB (gzipped)
- First Contentful Paint: < 1s

## Security Considerations

- JWT tokens stored in localStorage (production: consider httpOnly cookies)
- Secure password transmission with HTTPS
- CORS properly configured on backend
- Input validation on both client and server
- Protected routes with authentication checks
- Automatic logout on 401 errors
