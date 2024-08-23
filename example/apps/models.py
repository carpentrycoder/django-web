# example/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_type = models.CharField(max_length=20, choices=[
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    ])
