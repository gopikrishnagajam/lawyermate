from django.urls import path
from . import views, api_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# URL patterns for authentication and core app functionality
urlpatterns = [
    # Traditional session-based URLs (for web interface)
    path("", views.home, name="home"),                    # http://127.0.0.1:8000/
    path("signup/", views.signup_view, name="signup"),    # http://127.0.0.1:8000/signup/
    path("login/", views.login_view, name="login"),       # http://127.0.0.1:8000/login/
    path("logout/", views.logout_view, name="logout"),    # http://127.0.0.1:8000/logout/
    path("profile/", views.profile_view, name="profile"), # http://127.0.0.1:8000/profile/
    
    # JWT Token API endpoints (for mobile apps, SPAs)
    path("api/jwt/signup/", api_views.jwt_signup_api, name="jwt_signup"),
    path("api/jwt/login/", api_views.jwt_login_api, name="jwt_login"),
    path("api/jwt/logout/", api_views.jwt_logout_api, name="jwt_logout"),
    path("api/jwt/profile/", api_views.jwt_profile_api, name="jwt_profile"),
    path("api/jwt/refresh/", api_views.jwt_refresh_api, name="jwt_refresh"),
    
    # HTTP-Only Cookie API endpoints (most secure)
    path("api/cookie/login/", api_views.cookie_login_api, name="cookie_login"),
    path("api/cookie/signup/", api_views.cookie_signup_api, name="cookie_signup"),
    path("api/cookie/logout/", api_views.cookie_logout_api, name="cookie_logout"),
    path("api/cookie/profile/", api_views.cookie_profile_api, name="cookie_profile"),
    path("api/cookie/refresh/", api_views.cookie_refresh_api, name="cookie_refresh"),
    path("api/cookie/auth-status/", api_views.check_auth_status, name="cookie_auth_status"),
    
    # Built-in JWT endpoints (alternative)
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    
    # Electronic Diary URLs for Indian Lawyers
    path("diary/", views.diary_dashboard, name="diary_dashboard"),
    
    # Case Management
    path("diary/cases/", views.case_list, name="case_list"),
    path("diary/cases/create/", views.case_create, name="case_create"),
    path("diary/cases/<int:case_id>/", views.case_detail, name="case_detail"),
    
    # Client Management
    path("diary/clients/", views.client_list, name="client_list"),
    path("diary/clients/create/", views.client_create, name="client_create"),
    
    # Hearing Management
    path("diary/hearings/", views.hearing_list, name="hearing_list"),
    
    # Task Management
    path("diary/tasks/", views.task_list, name="task_list"),
    path("diary/tasks/<int:task_id>/complete/", views.task_complete, name="task_complete"),
    
    # Court Directory
    path("diary/courts/", views.court_list, name="court_list"),
]