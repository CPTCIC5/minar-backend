from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import PhoneToken
import re

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 
            'phone_number', 'date_of_birth', 'age', 
            'is_newsletter_interested', 'is_active', 'is_phone_verified'
        ]
        read_only_fields = ['is_active', 'is_phone_verified']

class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    
    def validate_phone_number(self, value):
        # Basic validation for phone numbers - can be enhanced based on your requirements
        if not re.match(r'^\+?[0-9]{10,15}$', value):
            raise serializers.ValidationError("Enter a valid phone number")
        return value

class OTPVerificationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'last_name', 'email', 
            'phone_number', 'date_of_birth', 'is_newsletter_interested'
        ]
    
    def validate_phone_number(self, value):
        # Basic validation for phone numbers
        if not re.match(r'^\+?[0-9]{10,15}$', value):
            raise serializers.ValidationError("Enter a valid phone number")
        
        # Check if phone number is already in use
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already in use")
        return value
    
    def validate_date_of_birth(self, value):
        if value and value > timezone.now().date():
            raise serializers.ValidationError("Date of birth cannot be in the future")
        return value

class DeviceTokenUpdateSerializer(serializers.Serializer):
    device_token = serializers.CharField(max_length=255)
