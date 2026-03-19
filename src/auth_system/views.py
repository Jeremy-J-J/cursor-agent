from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import secrets
import string
from .models import CustomUser, PasswordResetToken, EmailVerificationToken
from .serializers import (
    RegisterSerializer, LoginSerializer, 
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer,
    EmailVerificationSerializer, UserProfileSerializer, 
    CustomTokenObtainPairSerializer
)
from .permissions import IsOwnerOrAdmin


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for JWT token generation
    """
    serializer_class = CustomTokenObtainPairSerializer


class RegisterView(APIView):
    """
    View for user registration
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Generate verification token
            token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
            verification_token = EmailVerificationToken.objects.create(
                user=user,
                token=token,
                expires_at=timezone.now() + timezone.timedelta(hours=24)
            )
            
            # Send verification email
            self.send_verification_email(user, token)
            
            return Response({
                'message': 'User registered successfully. Please check your email for verification.',
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_verification_email(self, user, token):
        """
        Send email verification to user
        """
        subject = 'Verify your email address'
        message = f'Please click the link below to verify your email:\n\n'
        message += f'http://localhost:8000/api/auth/verify-email/?token={token}\n\n'
        message += 'If you did not create an account, please ignore this email.'
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )


class LoginView(APIView):
    """
    View for user login
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Reset failed login attempts
            user.reset_failed_login_attempts()
            
            # Generate tokens
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    View for user logout
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(APIView):
    """
    View for requesting password reset
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
                
                # Generate reset token
                token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
                reset_token, created = PasswordResetToken.objects.update_or_create(
                    user=user,
                    defaults={
                        'token': token,
                        'expires_at': timezone.now() + timezone.timedelta(hours=1)
                    }
                )
                
                # Send reset email
                self.send_reset_email(user, token)
                
                return Response({
                    'message': 'Password reset email sent successfully'
                }, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({
                    'error': 'User with this email does not exist'
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_reset_email(self, user, token):
        """
        Send password reset email to user
        """
        subject = 'Password Reset Request'
        message = f'Please click the link below to reset your password:\n\n'
        message += f'http://localhost:8000/api/auth/reset-password/?token={token}\n\n'
        message += 'If you did not request a password reset, please ignore this email.'
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )


class PasswordResetConfirmView(APIView):
    """
    View for confirming password reset
    """
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']
            
            try:
                reset_token = PasswordResetToken.objects.get(token=token)
                if reset_token.is_expired():
                    return Response({
                        'error': 'Password reset token has expired'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                user = reset_token.user
                user.set_password(password)
                user.save()
                
                # Delete the used token
                reset_token.delete()
                
                return Response({
                    'message': 'Password reset successfully'
                }, status=status.HTTP_200_OK)
            except PasswordResetToken.DoesNotExist:
                return Response({
                    'error': 'Invalid password reset token'
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationView(APIView):
    """
    View for email verification
    """
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        serializer = EmailVerificationSerializer(data=request.query_params)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            
            try:
                verification_token = EmailVerificationToken.objects.get(token=token)
                if verification_token.is_expired():
                    return Response({
                        'error': 'Verification token has expired'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                user = verification_token.user
                user.is_verified = True
                user.save()
                
                # Delete the used token
                verification_token.delete()
                
                return Response({
                    'message': 'Email verified successfully'
                }, status=status.HTTP_200_OK)
            except EmailVerificationToken.DoesNotExist:
                return Response({
                    'error': 'Invalid verification token'
                }, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    View for user profile management
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    
    def get_object(self):
        return self.request.user


class UserListView(generics.ListAPIView):
    """
    View for listing all users (admin only)
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return CustomUser.objects.all()
        elif user.role == 'moderator':
            return CustomUser.objects.filter(role__in=['user', 'premium'])
        else:
            return CustomUser.objects.none()