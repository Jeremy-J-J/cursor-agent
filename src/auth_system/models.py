from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
import uuid


class CustomUser(AbstractUser):
    """
    Custom user model with email as username field
    """
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=255, blank=True, null=True)
    verification_token_expires = models.DateTimeField(blank=True, null=True)
    password_reset_token = models.CharField(max_length=255, blank=True, null=True)
    password_reset_token_expires = models.DateTimeField(blank=True, null=True)
    last_login_attempt = models.DateTimeField(blank=True, null=True)
    failed_login_attempts = models.IntegerField(default=0)
    max_failed_login_attempts = models.IntegerField(default=5)
    locked_out_until = models.DateTimeField(blank=True, null=True)
    
    # Role-based access control
    ROLES = [
        ('user', 'User'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('premium', 'Premium User'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLES, default='user')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def is_account_locked(self):
        """Check if account is locked due to too many failed login attempts"""
        if self.locked_out_until and self.locked_out_until > timezone.now():
            return True
        return False

    def unlock_account(self):
        """Unlock the account"""
        self.failed_login_attempts = 0
        self.locked_out_until = None
        self.save()

    def increment_failed_login_attempts(self):
        """Increment failed login attempts and lock account if needed"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= self.max_failed_login_attempts:
            self.locked_out_until = timezone.now() + timezone.timedelta(minutes=30)
        self.save()

    def reset_failed_login_attempts(self):
        """Reset failed login attempts"""
        self.failed_login_attempts = 0
        self.locked_out_until = None
        self.save()


class PasswordResetToken(models.Model):
    """
    Model to store password reset tokens
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at


class EmailVerificationToken(models.Model):
    """
    Model to store email verification tokens
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expires_at