# example/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # User type field with choices for Patient and Doctor
    USER_TYPE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ]
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    def is_patient(self):
        return self.user_type == 'patient'

    def is_doctor(self):
        return self.user_type == 'doctor'

class PatientProfile(models.Model):
    # One-to-one relationship with User for patient profiles
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    address_line1 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='profile_pics/')

    def __str__(self):
        return f"{self.user.username} - Patient Profile"

class DoctorProfile(models.Model):
    # One-to-one relationship with User for doctor profiles
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/')

    def __str__(self):
        return f"{self.user.username} - Doctor Profile"

class BlogPost(models.Model):
    # Category choices for blog posts
    CATEGORY_CHOICES = [
        ('Mental Health', 'Mental Health'),
        ('Heart Disease', 'Heart Disease'),
        ('Covid19', 'Covid19'),
        ('Immunization', 'Immunization'),
    ]

    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='blog_images/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    summary = models.TextField()
    content = models.TextField()
    is_draft = models.BooleanField(default=True)
    # Foreign key to DoctorProfile, only doctors can author blog posts
    author = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def truncated_summary(self):
        # Method to truncate summary to 15 words and append '...' if necessary
        words = self.summary.split()
        if len(words) > 15:
            return ' '.join(words[:15]) + '...'
        return self.summary
