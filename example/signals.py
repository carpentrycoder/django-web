from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, DoctorProfile, PatientProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'doctor':
            DoctorProfile.objects.create(user=instance)
        elif instance.user_type == 'patient':
            PatientProfile.objects.create(user=instance)
