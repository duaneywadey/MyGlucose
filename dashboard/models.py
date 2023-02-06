from django.db import models
from django.contrib.auth.models import User
from sklearn.ensemble import RandomForestClassifier
from django.core.validators import FileExtensionValidator
import joblib

class DashboardData(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	glucose = models.IntegerField()
	weight = models.IntegerField()
	systolic_bp = models.IntegerField()
	diastolic_bp = models.IntegerField()	
	dateNow = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.author}-{self.dateNow}'

class PredictionData(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	bmi = models.FloatField(null=True)
	dpf = models.FloatField(null=True)
	age = models.PositiveIntegerField(null=True)
	date = models.DateTimeField(auto_now_add=True)

	predictions = models.PositiveIntegerField(blank=True)

	def save(self, *args, **kwargs):
		model = joblib.load('model/updated_ml_model_diabetes')
		self.predictions = model.predict_proba([[self.bmi, self.dpf, self.age]])[:, 1]	
		self.predictions = self.predictions*100
		return super().save(*args, *kwargs)

	class Meta:
		ordering = ['-date']

	def __str__(self):
		return str(self.date)


class ProfileModel(models.Model):
	# One user from django admin is equal to one profile (One to one)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.ImageField(upload_to='profile', default='avatar.jpg', validators=[
		FileExtensionValidator(['png', 'jpg'])])

	def __str__(self):
		return f'{self.user.username}'