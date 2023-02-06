from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class DashboardData(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	glucose = models.IntegerField()
	weight = models.IntegerField()
	systolic_bp = models.IntegerField()
	diastolic_bp = models.IntegerField()	
	dateNow = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.author}-{self.dateNow}'

class ProfileModel(models.Model):
	# One user from django admin is equal to one profile (One to one)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to='profile', default='avatar.jpg', validators=[
		FileExtensionValidator(['png', 'jpg'])])

	def __str__(self):
		return f'{self.user.username}'