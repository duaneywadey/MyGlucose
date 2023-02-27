from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import DoctorModel

def doctor_profile(sender, instance, created, **kwargs):
	if created:
		DoctorModel.objects.create(
			user=instance)
		print('Profile created!')

post_save.connect(doctor_profile, sender=User)