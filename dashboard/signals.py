from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


from .models import ProfileModel, MessagePanel

def patients_profile(sender, instance, created, **kwargs):
	if created:
		ProfileModel.objects.create(
			user=instance)
		MessagePanel.objects.create(
			user=instance)
		print('Profile created!')

post_save.connect(patients_profile, sender=User)