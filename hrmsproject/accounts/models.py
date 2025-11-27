from django.conf import settings
from django.db import models

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

    def __str__(self):
        return f'{self.user.username} Profile'