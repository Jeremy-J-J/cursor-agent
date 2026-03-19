"""
Example usage of the Django Authentication System

This file demonstrates how to integrate and use the auth_system in a Django project.
"""

# 1. Add to your Django settings.py:
"""
INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
    'auth_system',
]

AUTH_USER_MODEL = 'auth_system.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Email settings (configure for your environment)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'noreply@example.com'
"""

# 2. Add to your main urls.py:
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('auth_system.urls')),
    # ... other URLs
]
"""

# 3. Example API calls:

# Register a new user
"""
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "role": "user"
  }'
"""

# Login
"""
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
"""

# Get user profile (requires authentication)
"""
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer <access_token>"
"""

# Password reset request
"""
curl -X POST http://localhost:8000/api/auth/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com"
  }'
"""

# Password reset confirmation
"""
curl -X POST http://localhost:8000/api/auth/password-reset/confirm/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "reset_token_here",
    "password": "newpassword123",
    "password_confirm": "newpassword123"
  }'
"""

# Verify email (click the link from verification email)
"""
http://localhost:8000/api/auth/verify-email/?token=verification_token_here
"""

# Admin-only endpoint to list users
"""
curl -X GET http://localhost:8000/api/auth/users/ \
  -H "Authorization: Bearer <admin_access_token>"
"""

# 4. Using in views with permissions:
"""
from rest_framework.permissions import IsAuthenticated
from auth_system.permissions import IsAdmin, IsModerator

class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def get(self, request):
        # Only admins can access this
        pass

class ModeratorOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsModerator]
    
    def get(self, request):
        # Admins and moderators can access this
        pass
"""