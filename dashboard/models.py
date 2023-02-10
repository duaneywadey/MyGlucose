from django.db import models
from django.contrib.auth.models import User
from sklearn.ensemble import RandomForestClassifier
from django.core.validators import FileExtensionValidator
import joblib

class DashboardData(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	glucose = models.IntegerField(null=True)
	weight = models.IntegerField(null=True)
	systolic_bp = models.IntegerField(null=True)
	diastolic_bp = models.IntegerField(null=True)	
	dateNow = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.author}-{self.dateNow}'

class PredictionData(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	height = models.FloatField(null=True)
	weight = models.PositiveIntegerField(null=True)
	age = models.PositiveIntegerField(null=True)
	date = models.DateTimeField(auto_now_add=True)
	dpf = models.FloatField(default=0)

	# Blank fields
	bmi = models.FloatField(blank=True)
	predictions = models.PositiveIntegerField(blank=True)


	def save(self, *args, **kwargs):
		model = joblib.load('model/updated_ml_model_diabetes')
		self.bmi = round(self.weight / ((self.height)**2),1)	
		self.predictions = model.predict_proba([[self.bmi, self.dpf, self.age]])[:, 1]	
		self.predictions = self.predictions*100		
		return super().save(*args, *kwargs)


	def __str__(self):
		return str(self.date)


class ProfileModel(models.Model):
	# One user from django admin is equal to one profile (One to one)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to='profile', default='avatar.jpg', validators=[
		FileExtensionValidator(['png', 'jpg'])])

	def __str__(self):
		return f'{self.user.username}'