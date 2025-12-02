import secrets
from django.conf import settings
from django.db import models
from django.utils import timezone
from datetime import timedelta


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    employee_code = models.CharField(max_length=30, blank=True)
    job_title = models.CharField(max_length=100, blank=True)
    location = models.CharField(max_length=100, blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    marital_status = models.CharField(max_length=20, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    permanent_address = models.TextField(blank=True)
    emergency_number = models.CharField(max_length=20, blank=True)
    blood_group = models.CharField(max_length=10, blank=True)
    # Account info
    aadhar_number = models.CharField(max_length=30, blank=True)
    pan_number = models.CharField(max_length=20, blank=True)
    esi_number = models.CharField(max_length=30, blank=True)
    pf_number = models.CharField(max_length=30, blank=True)
    uan_number = models.CharField(max_length=30, blank=True)
    communication_address = models.TextField(blank=True)
    # Account status fields
    must_change_password = models.BooleanField(
        default=False,
        help_text='Force user to change password on next login'
    )
    account_verified = models.BooleanField(
        default=False,
        help_text='Whether the employee has verified their account'
    )
    verification_token = models.CharField(
        max_length=64,
        blank=True,
        null=True,
        unique=True,
        help_text='Token for account verification'
    )
    verification_token_expires = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Expiration time for verification token'
    )

    def __str__(self):
        return f'{self.user.username} Profile'

    def generate_verification_token(self):
        """Generate a secure verification token."""
        token = secrets.token_urlsafe(32)
        self.verification_token = token
        self.verification_token_expires = timezone.now() + timedelta(days=7)  # Token valid for 7 days
        self.save()
        return token

    def is_verification_token_valid(self):
        """Check if verification token is valid and not expired."""
        if not self.verification_token:
            return False
        if self.verification_token_expires and timezone.now() > self.verification_token_expires:
            return False
        return True