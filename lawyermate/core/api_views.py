import logging
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.conf import settings
from django.utils import timezone
import json

# Set up logger for API debugging
logger = logging.getLogger(__name__)

# =============================================================================
# JWT TOKEN API VIEWS (for mobile apps, SPAs, etc.)
# =============================================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def jwt_signup_api(request):
    """
    JWT-based signup API endpoint
    
    Expected JSON:
    {
        "username": "john_doe",
        "email": "john@example.com", 
        "password": "securepass123",
        "confirm_password": "securepass123"
    }
    """
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        
        # Validation
        if not username or not email or not password:
            return Response({
                'error': 'Username, email, and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if password != confirm_password:
            return Response({
                'error': 'Passwords do not match'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if len(password) < 8:
            return Response({
                'error': 'Password must be at least 8 characters long'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return Response({
                'error': 'Invalid email format'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects.filter(email=email).exists():
            return Response({
                'error': 'Email already registered'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        return Response({
            'message': 'Account created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'date_joined': user.date_joined.isoformat()
            },
            'tokens': {
                'access': str(access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_201_CREATED)
        
    except json.JSONDecodeError:
        return Response({
            'error': 'Invalid JSON format'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': f'Server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def jwt_login_api(request):
    """
    JWT-based login API endpoint
    
    Expected JSON:
    {
        "username": "john_doe",
        "password": "securepass123"
    }
    """
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return Response({
                'error': 'Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Authenticate user
        user = authenticate(username=username, password=password)
        if not user:
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'date_joined': user.date_joined.isoformat()
            },
            'tokens': {
                'access': str(access_token),
                'refresh': str(refresh),
            }
        }, status=status.HTTP_200_OK)
        
    except json.JSONDecodeError:
        return Response({
            'error': 'Invalid JSON format'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': f'Server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def jwt_logout_api(request):
    """
    JWT logout - blacklists the refresh token
    
    Expected JSON:
    {
        "refresh_token": "your_refresh_token_here"
    }
    """
    try:
        data = json.loads(request.body)
        refresh_token = data.get('refresh_token')
        
        if not refresh_token:
            return Response({
                'error': 'Refresh token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Blacklist the refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response({
            'message': 'Logged out successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Logout failed: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def jwt_profile_api(request):
    """
    Get user profile data (JWT protected)
    """
    user = request.user
    return Response({
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'is_staff': user.is_staff,
        }
    }, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def jwt_refresh_api(request):
    """
    Refresh JWT access token using refresh token
    
    Expected JSON:
    {
        "refresh": "your_refresh_token_here"
    }
    """
    try:
        data = json.loads(request.body)
        refresh_token = data.get('refresh')
        
        if not refresh_token:
            return Response({
                'error': 'Refresh token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Generate new access token
        refresh = RefreshToken(refresh_token)
        access_token = refresh.access_token
        
        return Response({
            'access': str(access_token)
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Token refresh failed: {str(e)}'
        }, status=status.HTTP_401_UNAUTHORIZED)


# =============================================================================
# HTTP-ONLY COOKIE API VIEWS (most secure)
# =============================================================================

def set_jwt_cookies(response, tokens):
    """
    Production-Ready Helper function to set JWT tokens as HTTP-Only cookies
    
    Security Features:
    - HTTP-Only access tokens (XSS protection)
    - Secure cookies in production (HTTPS)
    - SameSite protection (CSRF protection)
    - Appropriate expiration times
    - Debug logging for development
    """
    logger.debug("🍪 Setting JWT cookies with security configurations...")
    
    # Cookie security settings
    is_secure = not settings.DEBUG
    logger.debug(f"🔒 Cookie security settings: secure={is_secure}, httponly=True, samesite=Lax")
    
    # Access token cookie (short-lived)
    logger.debug("🔑 Setting access_token cookie (1 hour expiry)")
    response.set_cookie(
        'access_token',
        tokens['access'],
        max_age=3600,  # 1 hour
        httponly=True,  # Cannot be accessed by JavaScript - XSS Protection
        secure=is_secure,  # HTTPS only in production
        samesite='Lax',  # CSRF protection
        path='/',
    )
    
    # Refresh token cookie (long-lived)  
    logger.debug("🔄 Setting refresh_token cookie (7 days expiry)")
    response.set_cookie(
        'refresh_token',
        tokens['refresh'],
        max_age=7*24*3600,  # 7 days
        httponly=True,  # HTTP-Only for security
        secure=is_secure,
        samesite='Lax',
        path='/',
    )
    
    # Non-HTTP-Only cookie for JavaScript to check auth status
    logger.debug("✅ Setting is_authenticated cookie (JS readable)")
    response.set_cookie(
        'is_authenticated',
        'true',
        max_age=3600,  # 1 hour
        httponly=False,  # JavaScript can read this for UI updates
        secure=is_secure,
        samesite='Lax',
        path='/',
    )
    
    logger.debug("✅ All JWT cookies set successfully with production security settings")
    
    return response

def clear_jwt_cookies(response):
    """
    Helper function to clear JWT cookies on logout
    """
    response.delete_cookie('access_token', path='/')
    response.delete_cookie('refresh_token', path='/')
    response.delete_cookie('is_authenticated', path='/')
    return response

@api_view(['POST'])
@permission_classes([AllowAny])
def cookie_login_api(request):
    """
    Production-Ready Login endpoint that sets JWT tokens as HTTP-Only cookies
    
    Features:
    - Secure HTTP-Only cookie storage
    - Comprehensive debug logging
    - Token generation tracking
    - User authentication monitoring
    """
    logger.debug("🔐 Cookie Login API: Starting login process")
    
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        logger.debug(f"📋 Login attempt for username: '{username}'")
        
        if not username or not password:
            logger.debug("❌ Missing username or password")
            return Response({
                'error': 'Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Authenticate user
        logger.debug(f"🔍 Authenticating user: {username}")
        user = authenticate(username=username, password=password)
        
        if not user:
            logger.debug(f"❌ Authentication failed for user: {username}")
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        logger.debug(f"✅ User authenticated successfully: {user.username} (ID: {user.id})")
        
        # Generate JWT tokens
        logger.debug("🎫 Generating JWT tokens...")
        refresh = RefreshToken.for_user(user)
        
        tokens = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
        
        logger.debug(f"✅ JWT tokens generated successfully")
        logger.debug(f"🔑 Access token length: {len(tokens['access'])} characters")
        logger.debug(f"🔄 Refresh token length: {len(tokens['refresh'])} characters")
        logger.debug(f"📋 Access token payload preview: user_id={refresh.access_token.get('user_id')}")
        
        response_data = {
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'date_joined': user.date_joined.isoformat()
            },
            'authenticated': True,
            'expires_in': 3600,
            'debug_info': {
                'token_generated': True,
                'access_token_length': len(tokens['access']),
                'user_id': user.id,
            } if settings.DEBUG else {}
        }
        
        response = Response(response_data, status=status.HTTP_200_OK)
        logger.debug("🍪 Setting JWT tokens as HTTP-Only cookies...")
        response = set_jwt_cookies(response, tokens)
        logger.debug("✅ Login process completed successfully")
        
        return response
        
    except json.JSONDecodeError:
        return Response({
            'error': 'Invalid JSON format'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': f'Server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def cookie_signup_api(request):
    """
    Signup endpoint that automatically logs in with HTTP-Only cookies
    """
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        
        # Validation (same as JWT signup)
        if not username or not email or not password:
            return Response({
                'error': 'Username, email, and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if password != confirm_password:
            return Response({
                'error': 'Passwords do not match'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if len(password) < 8:
            return Response({
                'error': 'Password must be at least 8 characters long'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            validate_email(email)
        except ValidationError:
            return Response({
                'error': 'Invalid email format'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects.filter(username=username).exists():
            return Response({
                'error': 'Username already exists'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        if User.objects.filter(email=email).exists():
            return Response({
                'error': 'Email already registered'
            }, status=status.HTTP_400_BAD_REQUEST)
            
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Generate JWT tokens for immediate login
        refresh = RefreshToken.for_user(user)
        tokens = {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }
        
        response_data = {
            'message': 'Account created and logged in successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'date_joined': user.date_joined.isoformat()
            },
            'authenticated': True,
        }
        
        response = Response(response_data, status=status.HTTP_201_CREATED)
        response = set_jwt_cookies(response, tokens)
        
        return response
        
    except Exception as e:
        return Response({
            'error': f'Server error: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cookie_logout_api(request):
    """
    Logout endpoint that clears HTTP-Only cookies
    """
    try:
        # Get refresh token from cookie to blacklist it
        refresh_token = request.COOKIES.get('refresh_token')
        
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception:
                pass  # Token might already be invalid
        
        response_data = {
            'message': 'Logged out successfully'
        }
        
        response = Response(response_data, status=status.HTTP_200_OK)
        response = clear_jwt_cookies(response)
        
        return response
        
    except Exception as e:
        return Response({
            'error': f'Logout failed: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cookie_profile_api(request):
    """
    Production-Ready: Get user profile (authentication via HTTP-Only cookie)
    
    This endpoint demonstrates successful JWT authentication via HTTP-Only cookies.
    The request must include a valid JWT token in the 'access_token' cookie.
    """
    logger.debug("👤 Profile API: Processing authenticated request")
    
    user = request.user
    logger.debug(f"✅ User profile requested: {user.username} (ID: {user.id})")
    
    # Debug: Check authentication method
    auth_header = request.META.get('HTTP_AUTHORIZATION', 'None')
    cookies_present = list(request.COOKIES.keys())
    logger.debug(f"🔍 Auth method: HTTP-Only Cookie (no auth header needed)")
    logger.debug(f"🍪 Cookies present: {cookies_present}")
    logger.debug(f"🔐 Authentication successful via CookieJWTAuthentication")
    
    profile_data = {
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined.isoformat(),
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'is_staff': user.is_staff,
        },
        'authenticated': True,
        'auth_method': 'HTTP-Only Cookie JWT',
        'debug_info': {
            'cookies_available': cookies_present,
            'authentication_class': 'CookieJWTAuthentication',
            'timestamp': timezone.now().isoformat(),
        } if settings.DEBUG else {}
    }
    
    logger.debug("✅ Profile data prepared and returned successfully")
    return Response(profile_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def cookie_refresh_api(request):
    """
    Production-Ready: Refresh access token using refresh token from HTTP-Only cookie
    
    This endpoint handles automatic token refresh when access tokens expire.
    Called when access_token cookie is missing but refresh_token is still valid.
    """
    logger.debug("🔄 Token Refresh API: Starting refresh process")
    logger.debug(f"📋 Available cookies: {list(request.COOKIES.keys())}")
    
    try:
        refresh_token = request.COOKIES.get('refresh_token')
        
        if not refresh_token:
            logger.debug("❌ No refresh token found in cookies")
            return Response({
                'error': 'Refresh token not found'
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        logger.debug("✅ Refresh token found in cookies")
        logger.debug("🔄 Generating new access token...")
            
        # Generate new access token
        refresh = RefreshToken(refresh_token)
        new_access_token = str(refresh.access_token)
        
        logger.debug(f"✅ New access token generated successfully")
        logger.debug(f"🔑 New access token length: {len(new_access_token)} characters")
        logger.debug(f"👤 Token generated for user_id: {refresh.access_token.get('user_id')}")
        
        response_data = {
            'message': 'Token refreshed successfully',
            'authenticated': True,
            'expires_in': 3600,
            'debug_info': {
                'new_token_length': len(new_access_token),
                'user_id': refresh.access_token.get('user_id'),
                'refresh_timestamp': timezone.now().isoformat(),
            } if settings.DEBUG else {}
        }
        
        response = Response(response_data, status=status.HTTP_200_OK)
        
        logger.debug("🍪 Setting new access token as HTTP-Only cookie...")
        
        # Set new access token cookie
        response.set_cookie(
            'access_token',
            new_access_token,
            max_age=3600,
            httponly=True,
            secure=not settings.DEBUG,
            samesite='Lax',
            path='/',
        )
        
        # Update is_authenticated cookie
        response.set_cookie(
            'is_authenticated',
            'true',
            max_age=3600,
            httponly=False,
            secure=not settings.DEBUG,
            samesite='Lax',
            path='/',
        )
        
        logger.debug("✅ Token refresh completed successfully")
        return response
        
    except Exception as e:
        return Response({
            'error': f'Token refresh failed: {str(e)}'
        }, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes([AllowAny])
def check_auth_status(request):
    """
    Check if user is authenticated (for JavaScript to know auth status)
    """
    is_authenticated = hasattr(request, 'user') and request.user.is_authenticated
    
    if is_authenticated:
        return Response({
            'authenticated': True,
            'user': {
                'id': request.user.id,
                'username': request.user.username,
                'email': request.user.email,
            }
        })
    else:
        return Response({
            'authenticated': False
        })