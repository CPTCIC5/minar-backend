from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import random
import uuid
from datetime import date

class User(AbstractUser):
    # Basic user information
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField(null=True)
    is_newsletter_interested = models.BooleanField(default=False)
    
    # Fields for OTP verification
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    otp_attempts = models.IntegerField(default=0)
    is_phone_verified = models.BooleanField(default=False)
    
    # Push notification token for mobile
    device_token = models.CharField(max_length=255, null=True, blank=True)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'username', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} ({self.phone_number})"
    
    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None

    def generate_otp(self):
        """Generate a random 6-digit OTP"""
        return str(random.randint(100000, 999999))

class PhoneToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, related_name='phone_tokens', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=0)
    used = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Phone Token"
        verbose_name_plural = "Phone Tokens"
        
    def __str__(self):
        return f"{self.phone_number}: {self.otp}"
