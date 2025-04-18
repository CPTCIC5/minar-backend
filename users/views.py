from django.shortcuts import render
from rest_framework import status, permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, login, logout, authenticate, update_session_auth_hash
from django.utils import timezone
from datetime import timedelta
import uuid
import random
import string
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserLoginSerializer,
    EmailVerificationSerializer,
    DeviceTokenUpdateSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    PasswordChangeSerializer
)

User = get_user_model()

def generate_otp(length=6):
    """Generate a numeric OTP of specified length"""
    return ''.join(random.choices(string.digits, k=length))

class RegisterUserView(APIView):
    """Register a new user with email, phone, and other details"""
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            # Send verification email with OTP
            self.send_verification_email(user)
            
            return Response({
                "detail": "User registered successfully. Please check your email for verification OTP.",
                "user": UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def send_verification_email(self, user):
        """Send verification email with OTP to the user"""
        # Generate 6-digit OTP
        otp = generate_otp()
        
        # Save OTP to user
        user.email_verification_token = otp
        user.save()
        
        subject = "Verify Your Email"
        message = f"""
        Hi {user.first_name},
        
        Thank you for registering with us. Please use the following verification code:
        
        {otp}
        
        This code will expire in 24 hours.
        
        If you did not register for an account, please ignore this email.
        """
        
        try:
            print('aaya idhr')
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't fail the registration
            print(f"Failed to send verification email: {str(e)}")

class VerifyEmailView(APIView):
    """Verify user's email with OTP"""
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['token']
            
            try:
                user = User.objects.get(email_verification_token=otp, email_verified=False)
            except User.DoesNotExist:
                return Response(
                    {"detail": "Invalid or expired verification code"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Mark email as verified and remove token
            user.email_verified = True
            user.email_verification_token = None
            user.save()
            
            return Response({"detail": "Email successfully verified"})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """Email and password based login"""
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(request, username=email, password=password)
            
            if user is None:
                return Response(
                    {"detail": "Invalid email or password"}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            if not user.email_verified:
                # Resend verification email
                self.resend_verification_email(user)
                return Response(
                    {"detail": "Email not verified. Verification code has been resent to your email."},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            login(request, user)
            
            return Response({
                "detail": "Login successful",
                "user": UserSerializer(user).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def resend_verification_email(self, user):
        """Resend verification email with OTP to the user"""
        # Generate new OTP
        otp = generate_otp()
        user.email_verification_token = otp
        user.save()
        
        subject = "Verify Your Email"
        message = f"""
        Hi {user.first_name},
        
        Please use the following code to verify your email:
        
        {otp}
        
        This code will expire in 24 hours.
        
        If you did not register for an account, please ignore this email.
        """
        
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            # Log the error but don't fail the request
            print(f"Failed to send verification email: {str(e)}")

class LogoutView(APIView):
    """Log out the currently authenticated user"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({"detail": "Successfully logged out"})

class PasswordResetRequestView(APIView):
    """Request password reset via email"""
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Don't reveal that the user doesn't exist
                return Response({"detail": "Password reset code sent if account exists"})
            
            # Generate OTP
            otp = generate_otp()
            user.password_reset_token = otp
            user.save()
            
            subject = "Reset Your Password"
            message = f"""
            Hi {user.first_name},
            
            We received a request to reset your password. Use the following code to reset it:
            
            {otp}
            
            This code will expire in 24 hours.
            
            If you did not request a password reset, please ignore this email.
            """
            
            try:
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log the error but don't reveal it to the user
                print(f"Failed to send password reset email: {str(e)}")
            
            return Response({"detail": "Password reset code sent if account exists"})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    """Reset password using OTP"""
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            
            try:
                user = User.objects.get(password_reset_token=otp)
            except User.DoesNotExist:
                return Response(
                    {"detail": "Invalid or expired code"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password and remove token
            user.set_password(new_password)
            user.password_reset_token = None
            user.save()
            
            return Response({"detail": "Password reset successful"})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeView(APIView):
    """Change password when user is logged in"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            
            # Check current password
            if not user.check_password(serializer.validated_data['current_password']):
                return Response(
                    {"detail": "Current password is incorrect"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Update session to prevent logout
            update_session_auth_hash(request, user)
            
            return Response({"detail": "Password changed successfully"})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and updating user information"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user information"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_device_token(self, request):
        """Update device token for push notifications"""
        serializer = DeviceTokenUpdateSerializer(data=request.data)
        if serializer.is_valid():
            request.user.device_token = serializer.validated_data['device_token']
            request.user.save()
            return Response({"detail": "Device token updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)