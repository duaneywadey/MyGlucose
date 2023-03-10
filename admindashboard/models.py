from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


class DoctorModel(models.Model):

	CHOICES = (
		('Male', 'Male'),
		('Female', 'Female'),

	)

	# One user from django admin is equal to one profile (One to one)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctorprofile')
	avatar = models.ImageField(upload_to='profile', default='doctor.png', validators=[
		FileExtensionValidator(['png', 'jpg'])])
	profileAge = models.IntegerField(null=True, blank=True)
	sex = models.CharField(max_length=100, choices = CHOICES, default='')
	firstName = models.CharField(max_length=200, default='')
	lastName = models.CharField(max_length=200, default='')
	address = models.CharField(max_length=200, default='')
	phoneNum = models.CharField(max_length=50, default='')
	shortDesc = models.CharField(max_length=200, default='')



	def __str__(self):
		return f'{self.user.username}'




