# AI Document Classifier - Frontend

A modern React + Vite frontend application for the AI Document Classification System. Features JWT authentication, drag-and-drop PDF uploads, and real-time document classification with display of upload history from MongoDB.

## Features

✨ **Modern & Clean UI**
- Built with React 19 and Vite for blazing-fast development and builds
- Plain CSS with a professional, modern design (no Tailwind)
- Fully responsive and mobile-friendly
- Smooth animations and transitions

🔐 **Authentication & Security**
- JWT-based authentication
- Secure token storage in localStorage
- Protected routes
- Automatic token refresh on 401 errors
- User registration and login pages

📄 **Document Management**
- Drag-and-drop PDF upload support
- Multiple file selection
- Real-time file preview before upload
- Upload history with pagination
- Document deletion capability

🚀 **API Integration**
- Axios HTTP client with interceptors
- Environment-based API configuration
- Comprehensive error handling
- Loading states for all operations

## Project Structure

```
src/
├── components/              # Reusable React components
│   ├── Navbar.jsx          # Navigation bar with user info
│   ├── FileUpload.jsx      # Drag-and-drop file upload
│   ├── UploadHistory.jsx   # Document history table
│   └── ProtectedRoute.jsx  # Route protection wrapper
├── context/                # React Context for state management
│   └── AuthContext.jsx     # Authentication context and hooks
├── pages/                  # Page components
│   ├── Login.jsx           # Login page
│   ├── Register.jsx        # Registration page
│   └── Dashboard.jsx       # Main dashboard with upload and history
├── styles/                 # Component-specific CSS
│   ├── index.css           # Global styles and CSS variables
│   ├── navbar.css          # Navbar styles
│   ├── fileUpload.css      # File upload component styles
│   ├── uploadHistory.css   # Upload history styles
│   ├── auth.css            # Authentication pages styles
│   └── dashboard.css       # Dashboard styles
├── utils/                  # Utility functions and API client
│   ├── api.js              # Axios API client with interceptors
│   └── authService.js      # Authentication service
├── App.jsx                 # Main app component with routing
├── App.css                 # App-level styles
├── main.jsx                # React DOM entry point
└── index.css               # Base CSS configuration

public/                     # Static assets
.env                        # Environment variables
.env.example                # Example environment variables
```

## Setup Instructions

### Prerequisites

- Node.js (v16 or higher)
- npm or yarn package manager
- Backend API running at `http://localhost:5000` (configurable)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd client
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment variables**
```bash
# Copy the example file
cp .env.example .env

# Update .env with your backend API URL
VITE_API_BASE_URL=http://localhost:5000
VITE_API_TIMEOUT=30000
```

### Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

This creates an optimized production build in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## API Endpoints

The application expects the following backend API endpoints:

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/auth/verify` - Token verification

### Documents
- `POST /api/documents/upload` - Upload PDF files
- `GET /api/documents/history` - Get upload history
- `GET /api/documents/:id` - Get document details
- `DELETE /api/documents/:id` - Delete a document

## Authentication Flow

1. **Register** → User creates new account with email and password
2. **Login** → User logs in and receives JWT token
3. **Token Storage** → Token is saved in localStorage
4. **Auto-Redirect** → On 401 error, user is redirected to login
5. **Protected Routes** → Only authenticated users can access dashboard
6. **Logout** → Token and user data are cleared from localStorage

## Key Features Implementation

### Protected Routes
The `ProtectedRoute` component wraps pages that require authentication. If the user is not authenticated, they are redirected to the login page.

```jsx
<Route
  path="/dashboard"
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  }
/>
```

### API Interceptors
- **Request Interceptor**: Automatically adds JWT token to Authorization header
- **Response Interceptor**: Handles 401 errors and redirects to login

### File Upload
- Accepts only PDF files
- Supports drag-and-drop and file picker
- Shows file list with size information
- Real-time upload progress indication

### Upload History
- Displays all uploaded documents in a table
- Shows file name, predicted label, and upload time
- Supports pagination
- Delete functionality for documents
- Color-coded labels by category

## Styling & Design

### Color Scheme
- **Primary**: Blue (#3b82f6)
- **Secondary**: Green (#10b981)
- **Danger**: Red (#ef4444)
- **Neutral**: Gray palette

### CSS Organization
- Global styles in `styles/index.css`
- CSS variables for consistent theming
- Component-specific styles in dedicated files
- Responsive design with mobile-first approach

### Design Principles
- Clean and minimal interface
- Consistent spacing and typography
- Intuitive user interactions
- Loading states for all async operations
- Clear error messages and feedback

## Error Handling

The application provides comprehensive error handling:

1. **Form Validation**: Client-side validation on all forms
2. **API Errors**: User-friendly error messages from backend
3. **Network Errors**: Automatic retry and error notifications
4. **Authentication Errors**: Auto-redirect on token expiration

## Performance Optimizations

- Code splitting with Vite
- Vendor chunk separation (React, Router, Axios)
- Efficient re-renders with React hooks
- CSS minification in production
- Lazy component loading with React Router

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend API base URL | http://localhost:5000 |
| `VITE_API_TIMEOUT` | Request timeout in milliseconds | 30000 |

## Development Guidelines

### Code Style
- Use ES6+ JavaScript
- Functional components with React hooks
- Consistent naming conventions
- Proper error handling

### Component Structure
- Single responsibility principle
- Props validation
- Default props where applicable
- Descriptive prop names

### CSS Standards
- BEM naming convention
- CSS variables for theming
- Mobile-first responsive design
- Accessibility considerations

## Troubleshooting

### Application won't start
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### API requests are failing
1. Check if backend API is running on the configured URL
2. Verify `VITE_API_BASE_URL` in `.env` file
3. Check browser console for error messages

### Login issues
1. Ensure backend authentication endpoint is working
2. Check token is being stored in localStorage
3. Verify JWT token format

### CSS not loading
1. Ensure all CSS files are imported in their respective components
2. Check browser DevTools for CSS errors
3. Clear browser cache and rebuild

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## Technologies Used

- **React 19** - UI library
- **Vite 8** - Build tool and dev server
- **React Router 7** - Routing
- **Axios 1.7** - HTTP client
- **Plain CSS** - Styling (no frameworks)

## Contributing

When contributing to this project:

1. Follow the existing code style
2. Create descriptive commit messages
3. Test changes before submitting
4. Update documentation as needed

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
1. Check existing documentation
2. Review error messages in browser console
3. Verify backend API is running correctly
4. Check network tab in DevTools

## Production Deployment

### Vercel/Netlify
1. Connect GitHub repository
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Add environment variables in platform settings

### Self-hosted
1. Run `npm run build`
2. Deploy `dist/` folder to your web server
3. Configure web server to serve `index.html` for all routes (SPA)
4. Update API base URL for production backend

## Version History

- **v1.0.0** - Initial release
  - Authentication system
  - Document upload
  - Upload history
  - Protected routes
