from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
from datetime import date

from .managers import CustomUserManager

class User(AbstractUser):
    username= None
    # Basic user information
    email = models.EmailField(('email address'), unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_newsletter_interested = models.BooleanField(default=False)
    
    # Email verification fields
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, null=True, blank=True)
    
    # Password reset field
    password_reset_token = models.UUIDField(null=True, blank=True)
    
    # Push notification token for mobile
    device_token = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    #cUSERNAME_FIELD = 'email'
    objects = CustomUserManager()
    
    def __str__(self):
        return f"{self.first_name} ({self.email})"
    
    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return None