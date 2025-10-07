w# LawyerMate - Login/Signup System

This Django application provides a simple and secure authentication system for the LawyerMate platform.

## Features

### ✅ Implemented Features
- **User Registration (Sign Up)**
  - Username validation
  - Email validation  
  - Password confirmation
  - Duplicate user checking

- **Triple Authentication System**
  - **Traditional Sessions** - Classic web authentication
  - **JWT Tokens** - Modern stateless authentication for APIs/SPAs
  - **HTTP-Only Cookies** - Maximum security JWT storage

- **User Profile**
  - View user information
  - Account statistics display
  - Profile management interface

- **Security Features**
  - CSRF protection
  - Password hashing (Django built-in)
  - Login required decorators
  - Form validation
  - XSS protection (HTTP-Only cookies)
  - Token blacklisting
  - Automatic token refresh

## How to Use

### 1. Start the Server
```bash
cd c:\Users\gopik\Documents\lawgbt\code\lawyermate
python manage.py runserver
```

### 2. Access the Application

#### Traditional Web Interface:
- **Home Page**: http://127.0.0.1:8000/
- **Sign Up**: http://127.0.0.1:8000/signup/
- **Login**: http://127.0.0.1:8000/login/
- **Profile**: http://127.0.0.1:8000/profile/ (requires login)
- **Logout**: http://127.0.0.1:8000/logout/

####  API Endpoints:

**JWT Token APIs:** sd
- POST `/api/jwt/signup/` - Register with JWT tokens
- POST `/api/jwt/login/` - Login and get JWT tokens  
- GET `/api/jwt/profile/` - Get profile (requires Bearer token)
- POST `/api/jwt/refresh/` - Refresh access token
- POST `/api/jwt/logout/` - Blacklist refresh token

**HTTP-Only Cookie APIs:**
- POST `/api/cookie/login/` - Login with secure cookies
- GET `/api/cookie/profile/` - Get profile (automatic auth)
- POST `/api/cookie/refresh/` - Refresh token via cookies
- POST `/api/cookie/logout/` - Clear secure cookies

### 3. User Flow
1. **New Users**: Visit signup page → Create account → Login
2. **Existing Users**: Visit login page → Enter credentials → Access dashboard
3. **Logged-in Users**: View profile, logout, or access protected areas

## File Structure

```
core/
├── views.py          # Authentication logic and view functions
├── urls.py           # URL routing for auth pages  
├── models.py         # Database models (uses Django's User model)
├── templates/core/
│   ├── base.html     # Base template with navigation
│   ├── home.html     # Home page (different content for auth/non-auth users)
│   ├── signup.html   # User registration form
│   ├── login.html    # User login form
│   └── profile.html  # User profile page
```

## Key Functions in views.py

- **`home(request)`**: Displays home page with different content for authenticated/non-authenticated users
- **`signup_view(request)`**: Handles user registration with validation
- **`login_view(request)`**: Manages user authentication and login
- **`logout_view(request)`**: Logs out users and redirects to home
- **`profile_view(request)`**: Shows user profile (login required)

## Form Validation

### Signup Form
- Username: Required, unique, max 30 characters
- Email: Required, valid email format, unique
- Password: Required, minimum 8 characters
- Confirm Password: Must match password

### Login Form
- Username: Required
- Password: Required

## Security Notes

- All forms include CSRF tokens for security
- Passwords are automatically hashed by Django
- Login required decorator protects sensitive pages
- Messages framework provides user feedback
- Bootstrap styling for professional appearance

## Future Enhancements (Placeholders Ready)

- Password reset functionality
- Email verification
- Profile editing
- Password change feature
- Case management integration
- Document upload functionality

## Dependencies

- Django 5.1.2+
- Bootstrap 5.1.3 (CDN)
- No additional packages required for basic functionality

## Testing

### 🧪 Test Authentication System:

#### Traditional Session Authentication
1. Visit http://127.0.0.1:8000/signup/
2. Create a new account
3. Login at http://127.0.0.1:8000/login/
4. View profile and test logout

### 📱 Mobile/SPA Integration Testing
```javascript
// For React, Vue, React Native, etc.
const response = await fetch('/api/jwt/login/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: 'test', password: 'test123' })
});

const data = await response.json();
const { access, refresh } = data.tokens;

// Store tokens and use for API calls
localStorage.setItem('access_token', access);
```

## 🛡️ Security Comparison

| Feature | Sessions | JWT Tokens | HTTP-Only Cookies |
|---------|----------|------------|-------------------|
| **XSS Protection** | ✅ | ❌ | ✅ |
| **CSRF Protection** | ✅ | ✅ | ✅ |
| **Mobile Ready** | ❌ | ✅ | ✅ |
| **Stateless** | ❌ | ✅ | ✅ |
| **Auto-sent** | ✅ | ❌ | ✅ |
| **JS Access** | ❌ | ✅ | ❌ |
| **Dev Tools Visible** | ❌ | ✅ | ❌ |

**Recommendation**: Use HTTP-Only cookies for maximum security! 🍪🔒

## 🚀 Production Checklist

### Security Settings (settings.py)
```python
# For production
DEBUG = False
SIMPLE_JWT['AUTH_COOKIE_SECURE'] = True  # HTTPS only
SIMPLE_JWT['AUTH_COOKIE_SAMESITE'] = 'Strict'  # CSRF protection
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Dependencies
```bash
pip install djangorestframework==3.15.2
pip install djangorestframework-simplejwt==5.3.0
pip install django-cors-headers==4.3.1
pip install user-agents==2.2.0
```

## 🎯 When to Use Which Authentication

### Use **HTTP-Only Cookies** When:
- Building web applications (maximum security)
- Need XSS protection
- Want automatic token management
- **RECOMMENDED for LawyerMate! 🏆**

### Use **JWT Tokens** When:
- Building mobile applications
- Creating SPAs (React, Vue, Angular)
- Need cross-domain authentication
- Building public APIs

### Use **Sessions** When:
- Building simple internal tools
- Working with legacy systems
- Need server-side state management

## Notes for Developers

- The system uses Django's built-in User model with JWT extensions
- All templates extend from `base.html` with Bootstrap styling
- Messages framework configured for user feedback
- Custom authentication classes for cookie-based JWT
- Token blacklisting for secure logout
- CORS enabled for cross-origin API requests

Your LawyerMate platform now has **enterprise-grade authentication**:

**🏆 FEATURES IMPLEMENTED:**
- ✅ Traditional Session Authentication  
- ✅ JWT Token Authentication
- ✅ HTTP-Only Cookie Authentication (Most Secure)
- ✅ Token Blacklisting & Refresh
- ✅ XSS & CSRF Protection
- ✅ Mobile & SPA Ready
- ✅ Production Security Settings

**Ready for: Mobile Apps 📱 | SPAs 💻 | APIs 🔗 | Enterprise 🏢**