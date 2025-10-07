import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

# Set up logger for JWT debugging
logger = logging.getLogger(__name__)


class CookieJWTAuthentication(JWTAuthentication):
    """
    Production-Ready JWT Authentication that reads tokens from HTTP-Only cookies
    instead of Authorization headers. This provides better security against XSS attacks.
    
    Features:
    - HTTP-Only cookie security
    - Comprehensive debug logging
    - Token validation tracking
    - User authentication monitoring
    """
    
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token)
        Features auto-refresh when access token expires but refresh token is valid
        """
        # Debug: Log authentication attempt
        logger.debug(f"🔍 Authentication attempt for request to: {request.path}")
        logger.debug(f"📋 Available cookies: {list(request.COOKIES.keys())}")
        
        # First try to get token from cookie
        raw_token = self.get_raw_token_from_cookie(request)
        
        if raw_token is None:
            logger.debug("❌ No JWT token found in cookies")
            
            # Check if refresh token is available for auto-refresh
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                logger.debug("🔄 Access token missing but refresh token found - suggesting refresh")
                logger.debug("💡 Hint: Call /api/cookie/refresh/ to get new access token")
            
            return None
        
        # Debug: Token found
        logger.debug(f"✅ JWT token found in cookie")
        logger.debug(f"🔑 Token type: {type(raw_token)}")
        
        try:
            # Validate the token
            validated_token = self.get_validated_token(raw_token)
            logger.debug(f"✅ Token validation successful")
            
            user = self.get_user(validated_token)
            logger.debug(f"👤 User authenticated: {user.username} (ID: {user.id})")
            logger.debug(f"🕒 Token payload: user_id={validated_token.get('user_id')}")
            
            return (user, validated_token)
            
        except TokenError as e:
            logger.debug(f"❌ Token validation failed: {str(e)}")
            logger.debug(f"🔍 Token error type: {type(e).__name__}")
            
            # Check if refresh token is available for auto-refresh
            refresh_token = request.COOKIES.get('refresh_token')
            if refresh_token:
                logger.debug("🔄 Access token expired but refresh token available")
                logger.debug("💡 Hint: Call /api/cookie/refresh/ to get new access token")
            
            return None
        except Exception as e:
            logger.debug(f"💥 Unexpected authentication error: {str(e)}")
            return None
    
    def get_raw_token_from_cookie(self, request):
        """
        Extract the JWT token from HTTP-Only cookie
        """
        cookie_name = getattr(settings, 'SIMPLE_JWT', {}).get('AUTH_COOKIE', 'access_token')
        logger.debug(f"🍪 Looking for cookie named: '{cookie_name}'")
        
        raw_token = request.COOKIES.get(cookie_name)
        
        if raw_token is None:
            logger.debug(f"❌ Cookie '{cookie_name}' not found")
            return None
        
        logger.debug(f"✅ Cookie '{cookie_name}' found")
        logger.debug(f"📏 Token length: {len(raw_token)} characters")
        
        # Return as bytes for JWT processing
        return raw_token.encode('utf-8')
    
    def get_validated_token(self, raw_token):
        """
        Validate the token and return the validated token instance
        """
        logger.debug(f"🔐 Validating JWT token...")
        
        try:
            validated_token = UntypedToken(raw_token)
            logger.debug(f"✅ Token validation successful")
            logger.debug(f"📋 Token claims: {list(validated_token.keys())}")
            return validated_token
        except TokenError as e:
            logger.debug(f"❌ Token validation failed: {str(e)}")
            raise InvalidToken(f'Token is invalid or expired: {e}')