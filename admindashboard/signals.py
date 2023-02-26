from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import DoctorModel
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and instance.groups.filter(name='doctors').exists():
        DoctorModel.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'doctorprofile'):
        instance.doctorprofile.save()