from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DashboardData, PredictionData, ProfileModel, Comment

class DashboardDataForm(forms.ModelForm):
	class Meta:
		model = DashboardData
		fields = ['glucose', 'weight', 'systolic_bp', 'diastolic_bp']

class PredictionDataForm(forms.ModelForm):
	dpf = forms.CharField(label="DPF (Put zero if neither your mother nor father have the disease)", required=False)
	class Meta:
		model = PredictionData
		fields = ['height', 'weight', 'dpf', 'age']

class EditDashboardDataForm(forms.ModelForm):
	class Meta:
		model = DashboardData
		fields = ['glucose', 'weight', 'systolic_bp', 'diastolic_bp']

class EditPredictionDataForm(forms.ModelForm):
	dpf = forms.CharField(label="DPF (Put zero if neither your mother nor father have the disease)", required=False)
	class Meta:
		model = PredictionData
		fields = ['height', 'weight', 'age', 'dpf']


class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
# -----------------DELETING HELP TEXT---------------
	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		for fieldname in ['username', 'email', 'password1', 'password2']:
			self.fields[fieldname].help_text = None

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    # DELETING HELP TEXT
    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields["username"].disabled = True
        self.fields["email"].disabled = True


        for fieldname in ['username', 'email']:
            self.fields[fieldname].help_text = None


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = ProfileModel
		fields = ['profileAge', 'sex', 'firstName', 'lastName', 'address', 'phoneNum']


class CommentForm(forms.ModelForm):
	content = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':4, 'placeholder':"Talk to a doctor!"}))
	class Meta:
		model = Comment
		fields = ('content',)






