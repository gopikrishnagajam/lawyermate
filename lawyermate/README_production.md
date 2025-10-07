# LawyerMate - Production-Ready Authentication System

A Django application featuring **secure HTTP-Only Cookie JWT authentication** with comprehensive debugging capabilities, designed for production environments.

## 🚀 Production-Ready Features

### 🔐 Secure HTTP-Only Cookie Authentication
- **XSS Protection**: JWT tokens stored in HTTP-Only cookies, invisible to JavaScript
- **CSRF Protection**: SameSite=Lax prevents cross-site request forgery
- **Auto HTTPS**: Secure flag automatically enabled in production
- **Token Rotation**: Refresh tokens are rotated and blacklisted for maximum security
- **Real-time Debugging**: Comprehensive logging for development and troubleshooting

### 🛡️ Security-First Architecture
```
Browser Request → Django → CookieJWTAuthentication → Validate Token → User Access
     ↑                                ↓
HTTP-Only Cookie ←←← Set Secure Cookies ←←← JWT Token Generation
```

## 🏗️ Quick Start

1. **Install Dependencies**:
```bash
pip install -r requirements.txt
```

2. **Database Setup**:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

3. **Run Development Server**:
```bash
python manage.py runserver
```

4. **Test Production Authentication**:
   - Visit: http://127.0.0.1:8000/production-demo/
   - Login with your superuser credentials
   - Watch real-time debug console for authentication events

## 🎯 Production API Endpoints

### Core Authentication (HTTP-Only Cookies)
- `POST /api/auth/cookie/login/` - Secure login with HTTP-Only cookies
- `POST /api/auth/cookie/logout/` - Logout and clear all cookies
- `GET /api/auth/cookie/profile/` - Get user profile (auto-authenticated)
- `POST /api/auth/cookie/refresh/` - Refresh tokens automatically

### Web Interface
- `/` - Home page with authentication demo links
- `/production-demo/` - **⭐ Main production authentication demo**
- `/signup/` - User registration
- `/login/` - Traditional login (session-based)

## 🔍 Debug Console Features

The production demo includes a real-time debug console showing:

```
🔐 JWT DEBUG: 12:34:56 - 🔍 Authentication attempt for request to: /api/auth/cookie/profile/
🔐 JWT DEBUG: 12:34:56 - 📋 Available cookies: ['access_token', 'refresh_token', 'is_authenticated']
🔐 JWT DEBUG: 12:34:56 - ✅ JWT token found in cookie
🔐 JWT DEBUG: 12:34:56 - 👤 User authenticated: john_doe (ID: 1)
🔐 JWT DEBUG: 12:34:56 - ✅ Profile data prepared and returned successfully
```

## 🔧 Production Configuration

### settings.py - JWT Configuration
```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),    # 1 hour
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),       # 7 days
    'ROTATE_REFRESH_TOKENS': True,                     # Security: rotate on use
    'BLACKLIST_AFTER_ROTATION': True,                  # Security: blacklist old tokens
    'AUTH_COOKIE_SECURE': not DEBUG,                   # HTTPS only in production
    'AUTH_COOKIE_HTTP_ONLY': True,                     # XSS protection
    'AUTH_COOKIE_SAMESITE': 'Lax',                     # CSRF protection
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'core.authentication.CookieJWTAuthentication',  # Production-ready only
    ),
}
```

### Custom Authentication Class
```python
class CookieJWTAuthentication(JWTAuthentication):
    """
    Production-Ready JWT Authentication via HTTP-Only cookies
    Features: XSS protection, debug logging, token validation tracking
    """
```

## 🚦 Security Comparison

| Method | XSS Safe | Auto-Sent | Production Ready | CSRF Safe |
|--------|----------|-----------|------------------|-----------|
| **HTTP-Only Cookies** ✅ | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| localStorage | ❌ No | ❌ Manual | ❌ No | ❌ No |
| Auth Headers | ❌ No | ❌ Manual | ⚠️ Maybe | ❌ No |

## 🐛 Development Debugging

Enable comprehensive debugging in development:

```python
# Automatic debug logging when DEBUG=True
if DEBUG:
    LOGGING = {
        'loggers': {
            'core.authentication': {
                'handlers': ['jwt_console'],
                'level': 'DEBUG',
            },
            'core.api_views': {
                'handlers': ['jwt_console'],  
                'level': 'DEBUG',
            },
        },
    }
```

## 📦 Dependencies

```txt
Django==5.1.2
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.0
django-cors-headers==4.3.1
user-agents==2.2.0
```

## 🎯 Why This Approach?

1. **Maximum Security**: HTTP-Only cookies prevent XSS attacks completely
2. **Zero JavaScript**: No need to manage tokens in frontend code
3. **Auto HTTPS**: Production security enabled automatically
4. **Debug Friendly**: Comprehensive logging for development
5. **Production Ready**: Designed for real-world deployment

## 📈 Performance & Monitoring

The debug console provides insights into:
- Token generation time
- Authentication success/failure rates  
- Cookie security settings validation
- User authentication patterns
- Token expiration handling

## 🤝 Contributing

1. Focus on production security
2. Maintain comprehensive debugging
3. Follow HTTP-Only cookie best practices
4. Test with the production demo

---

**⭐ Start with the Production Demo**: Visit `/production-demo/` to see secure authentication in action!