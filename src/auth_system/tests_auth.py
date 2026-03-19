"""
Comprehensive test suite for the user authentication system
Tests edge cases for get_user function and all authentication flows
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from src.auth_system.user_manager import UserManager
from src.auth_system.models import CustomUser, PasswordResetToken, EmailVerificationToken

User = get_user_model()


class AuthSystemComprehensiveTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_manager = UserManager()
        
        # Create test users
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'securepassword123',
            'role': 'user'
        }
        
        self.admin_data = {
            'username': 'adminuser',
            'email': 'admin@example.com',
            'password': 'adminpassword123',
            'role': 'admin'
        }
        
        self.user = User.objects.create_user(**self.user_data)
        self.admin = User.objects.create_user(**self.admin_data)
        
        # Create a token for testing
        self.token = 'testtoken1234567890abcdef'
        
    def test_get_user_exists(self):
        """Test getting an existing user by ID"""
        user = self.user_manager.get_user(self.user.id)
        self.assertEqual(user, self.user)
        
    def test_get_user_not_exists(self):
        """Test getting a non-existing user by ID"""
        user = self.user_manager.get_user(999)
        self.assertIsNone(user)
        
    def test_get_user_by_email_exists(self):
        """Test getting an existing user by email"""
        user = self.user_manager.get_user_by_email('test@example.com')
        self.assertEqual(user, self.user)
        
    def test_get_user_by_email_not_exists(self):
        """Test getting a non-existing user by email"""
        user = self.user_manager.get_user_by_email('nonexistent@example.com')
        self.assertIsNone(user)
        
    def test_get_all_users(self):
        """Test getting all users"""
        users = self.user_manager.get_all_users()
        self.assertEqual(users.count(), 2)
        
    def test_get_users_by_role(self):
        """Test getting users by role"""
        users = self.user_manager.get_users_by_role('user')
        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first(), self.user)
        
        users = self.user_manager.get_users_by_role('admin')
        self.assertEqual(users.count(), 1)
        self.assertEqual(users.first(), self.admin)
        
    def test_user_creation(self):
        """Test that a user can be created"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        
    def test_user_registration(self):
        """Test user registration endpoint"""
        response = self.client.post('/api/auth/register/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['email'], self.user_data['email'])
        
    def test_user_login_success(self):
        """Test successful user login"""
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
    def test_user_login_invalid_credentials(self):
        """Test user login with invalid credentials"""
        login_data = {
            'email': self.user_data['email'],
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_user_login_nonexistent_user(self):
        """Test user login with non-existent user"""
        login_data = {
            'email': 'nonexistent@example.com',
            'password': 'any_password'
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_user_login_account_locked(self):
        """Test user login with locked account due to too many failed attempts"""
        # Simulate multiple failed login attempts
        for i in range(5):
            login_data = {
                'email': self.user_data['email'],
                'password': 'wrongpassword'
            }
            response = self.client.post('/api/auth/login/', login_data)
            
        # Try one more time - should be locked out
        login_data = {
            'email': self.user_data['email'],
            'password': 'wrongpassword'
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_password_reset_request_valid_email(self):
        """Test password reset request with valid email"""
        response = self.client.post('/api/auth/password-reset/', {'email': self.user_data['email']})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
    def test_password_reset_request_invalid_email(self):
        """Test password reset request with invalid email"""
        response = self.client.post('/api/auth/password-reset/', {'email': 'nonexistent@example.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_password_reset_confirm_valid_token(self):
        """Test password reset confirmation with valid token"""
        # Create a reset token
        reset_token = PasswordResetToken.objects.create(
            user=self.user,
            token=self.token,
            expires_at=timezone.now() + timedelta(hours=1)
        )
        
        # Reset password
        reset_data = {
            'token': self.token,
            'password': 'newsecurepassword456'
        }
        response = self.client.post('/api/auth/password-reset/confirm/', reset_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # Verify password was changed
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newsecurepassword456'))
        
    def test_password_reset_confirm_expired_token(self):
        """Test password reset confirmation with expired token"""
        # Create an expired reset token
        expired_token = PasswordResetToken.objects.create(
            user=self.user,
            token=self.token,
            expires_at=timezone.now() - timedelta(hours=1)
        )
        
        # Try to reset password with expired token
        reset_data = {
            'token': self.token,
            'password': 'newsecurepassword456'
        }
        response = self.client.post('/api/auth/password-reset/confirm/', reset_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_password_reset_confirm_invalid_token(self):
        """Test password reset confirmation with invalid token"""
        reset_data = {
            'token': 'invalidtoken',
            'password': 'newsecurepassword456'
        }
        response = self.client.post('/api/auth/password-reset/confirm/', reset_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_email_verification_valid_token(self):
        """Test email verification with valid token"""
        # Create a verification token
        verification_token = EmailVerificationToken.objects.create(
            user=self.user,
            token=self.token,
            expires_at=timezone.now() + timedelta(hours=24)
        )
        
        # Verify email
        response = self.client.get(f'/api/auth/verify-email/?token={self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
        # Verify user is now verified
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified)
        
    def test_email_verification_expired_token(self):
        """Test email verification with expired token"""
        # Create an expired verification token
        expired_token = EmailVerificationToken.objects.create(
            user=self.user,
            token=self.token,
            expires_at=timezone.now() - timedelta(hours=1)
        )
        
        # Try to verify with expired token
        response = self.client.get(f'/api/auth/verify-email/?token={self.token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_email_verification_invalid_token(self):
        """Test email verification with invalid token"""
        response = self.client.get('/api/auth/verify-email/?token=invalidtoken')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_user_profile_access(self):
        """Test user profile access with valid authentication"""
        # First login to get tokens
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Get access token from response
        access_token = response.data['access']
        
        # Access profile with authentication
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])
        
    def test_user_profile_access_unauthenticated(self):
        """Test user profile access without authentication"""
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_user_profile_update(self):
        """Test user profile update with valid authentication"""
        # First login to get tokens
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Get access token from response
        access_token = response.data['access']
        
        # Update profile
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        update_data = {
            'username': 'updateduser',
            'email': 'updated@example.com'
        }
        response = self.client.put('/api/auth/profile/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'updateduser')
        
    def test_user_list_access_admin(self):
        """Test user list access for admin user"""
        # First login as admin to get tokens
        login_data = {
            'email': self.admin_data['email'],
            'password': self.admin_data['password']
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Get access token from response
        access_token = response.data['access']
        
        # Access user list with admin authentication
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/auth/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_user_list_access_regular_user(self):
        """Test user list access for regular user (should be forbidden)"""
        # First login as regular user to get tokens
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Get access token from response
        access_token = response.data['access']
        
        # Access user list with regular user authentication
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get('/api/auth/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_logout_with_valid_token(self):
        """Test logout with valid refresh token"""
        # First login to get tokens
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post('/api/auth/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Get refresh token from response
        refresh_token = response.data['refresh']
        
        # Logout
        logout_data = {
            'refresh': refresh_token
        }
        response = self.client.post('/api/auth/logout/', logout_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        
    def test_logout_with_invalid_token(self):
        """Test logout with invalid refresh token"""
        logout_data = {
            'refresh': 'invalidtoken123'
        }
        response = self.client.post('/api/auth/logout/', logout_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_get_user_with_invalid_id(self):
        """Test get_user with invalid ID (negative number)"""
        user = self.user_manager.get_user(-1)
        self.assertIsNone(user)
        
    def test_get_user_with_zero_id(self):
        """Test get_user with zero ID"""
        user = self.user_manager.get_user(0)
        self.assertIsNone(user)
        
    def test_get_user_with_string_id(self):
        """Test get_user with string ID (should return None)"""
        user = self.user_manager.get_user("invalid")
        self.assertIsNone(user)
        
    def test_get_user_by_email_with_special_characters(self):
        """Test get_user_by_email with special characters"""
        # Create a user with special characters in email
        special_user = User.objects.create_user(
            username='specialuser',
            email='special+test@example.com',
            password='testpass123',
            role='user'
        )
        
        user = self.user_manager.get_user_by_email('special+test@example.com')
        self.assertEqual(user, special_user)
        
    def test_get_user_by_email_case_sensitivity(self):
        """Test get_user_by_email case sensitivity"""
        user = self.user_manager.get_user_by_email('TEST@EXAMPLE.COM')
        self.assertIsNone(user)  # Should be case sensitive
        
        user = self.user_manager.get_user_by_email('test@example.com')
        self.assertEqual(user, self.user)