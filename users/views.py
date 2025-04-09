from django.shortcuts import render
from rest_framework import status, permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model, login, logout
from django.utils import timezone
from datetime import timedelta
import random

from .models import PhoneToken
from .serializers import (
    UserSerializer, 
    PhoneNumberSerializer, 
    OTPVerificationSerializer,
    UserRegistrationSerializer,
    DeviceTokenUpdateSerializer
)

User = get_user_model()

class SendOTPView(APIView):
    """Send OTP to the provided phone number for login verification"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                return Response(
                    {"detail": "User with this phone number does not exist"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            
            # Save OTP
            phone_token = PhoneToken.objects.create(
                user=user,
                phone_number=phone_number,
                otp=otp
            )
            
            # TODO: Integrate with SMS service to send OTP
            # For development, returning OTP in response
            return Response({
                "detail": "OTP sent successfully",
                "otp": otp  # Remove this in production
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    """OTP-based login view"""
    permission_classes = [AllowAny]
    authentication_classes = [SessionAuthentication]
    
    def post(self, request):
        serializer = OTPVerificationSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            otp = serializer.validated_data['otp']
            
            try:
                phone_token = PhoneToken.objects.filter(
                    phone_number=phone_number,
                    used=False
                ).latest('timestamp')
            except PhoneToken.DoesNotExist:
                return Response(
                    {"detail": "No valid OTP found"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if timezone.now() > phone_token.timestamp + timedelta(minutes=10):
                return Response(
                    {"detail": "OTP has expired"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if otp != phone_token.otp:
                phone_token.attempts += 1
                phone_token.save()
                if phone_token.attempts >= 3:
                    phone_token.used = True
                    phone_token.save()
                    return Response(
                        {"detail": "Too many failed attempts. Request new OTP"}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    {"detail": "Invalid OTP"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            phone_token.used = True
            phone_token.save()
            
            user = phone_token.user
            if not user.is_phone_verified:
                user.is_phone_verified = True
                user.save()
                
            login(request, user)
            
            return Response({
                "detail": "Login successful",
                "user": UserSerializer(user).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterUserView(APIView):
    """Register a new user with required information"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            # Create user with unusable password since we're using OTP
            user = User.objects.create_user(
                **serializer.validated_data,
                password=None  # No password needed
            )
            user.set_unusable_password()
            
            # Generate OTP for phone verification
            otp = str(random.randint(100000, 999999))
            
            # Save OTP
            phone_token = PhoneToken.objects.create(
                user=user,
                phone_number=user.phone_number,
                otp=otp
            )
            
            # TODO: Integrate with SMS service to send OTP
            return Response({
                "detail": "User registered successfully. Verify your phone number with the OTP.",
                "user": UserSerializer(user).data,
                "otp": otp  # Remove in production
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    """Log out the currently authenticated user"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        logout(request)
        return Response({"detail": "Successfully logged out"})

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

