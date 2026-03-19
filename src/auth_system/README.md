# Django Authentication System

A comprehensive authentication system for Django applications with the following features:

## Features

1. **Custom User Model** - Uses email as the username field
2. **JWT-based Authentication** - With refresh tokens support
3. **Password Reset Functionality** - Secure password reset with token expiration
4. **Email Verification System** - Email verification with token expiration
5. **Role-based Access Control** - Support for different user roles (user, admin, moderator, premium)
6. **Rate Limiting for Login Attempts** - Account lockout after failed attempts
7. **Secure Password Hashing** - Uses Django's built-in password validation

## Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### JWT Tokens
- `POST /api/auth/token/` - Get access and refresh tokens
- `POST /api/auth/token/refresh/` - Refresh access token

### Password Management
- `POST /api/auth/password-reset/` - Request password reset
- `POST /api/auth/password-reset/confirm/` - Confirm password reset

### Email Verification
- `GET /api/auth/verify-email/` - Verify user email

### User Management
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/` - Update user profile
- `GET /api/auth/users/` - List users (admin only)

## Installation

1. Add `auth_system` to your `INSTALLED_APPS` in `settings.py`
2. Configure the authentication settings
3. Run migrations: `python manage.py migrate`

## Configuration

Add to your Django settings:

```python
# Settings for authentication
AUTH_USER_MODEL = 'auth_system.CustomUser'

# JWT Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Email settings (configure for your environment)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
DEFAULT_FROM_EMAIL = 'noreply@example.com'
```

## Usage

### Register a new user
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### Password Reset
```bash
curl -X POST http://localhost:8000/api/auth/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com"
  }'
```

### Verify Email
Visit: `http://localhost:8000/api/auth/verify-email/?token=your_token_here`

## Security Features

- Passwords are securely hashed using Django's built-in methods
- Rate limiting for login attempts (5 failed attempts = 30 minute lockout)
- Token-based authentication with expiration
- Secure password reset tokens
- Email verification tokens with expiration
- Role-based access control for different endpoints