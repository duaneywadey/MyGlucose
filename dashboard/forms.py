from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DashboardData, PredictionData

class DashboardDataForm(forms.ModelForm):
	class Meta:
		model = DashboardData
		fields = ['glucose', 'weight', 'systolic_bp', 'diastolic_bp']

class PredictionDataForm(forms.ModelForm):
	parentAgeDiabetes = forms.CharField(label="Is your mother/father diabetic? How old was he/she when diagnosed with diabetes? Leave blank if your guradian doesn't have the disease.", required=False)
	class Meta:
		model = PredictionData
		fields = ['height', 'weight', 'parentAgeDiabetes', 'age']


class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']


# -----------------DELETING HELP TEXT---------------
	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		for fieldname in ['username', 'email', 'password1', 'password2']:
			self.fields[fieldname].help_text = None




