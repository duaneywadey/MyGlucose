from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DoctorModel
from dashboard.models import MessagePanel, Comment


class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']
# -----------------DELETING HELP TEXT---------------
	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		for fieldname in ['username', 'email', 'password1', 'password2']:
			self.fields[fieldname].help_text = None

class CommentForm(forms.ModelForm):
	content = forms.CharField(label='', widget=forms.TextInput(attrs={
			'placeholder':"What's on your mind?",
			'rows':5}))
	class Meta:
		model = Comment
		fields = ('content',)

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
		model = DoctorModel
		fields = ['profileAge', 'sex', 'firstName', 'lastName', 'address', 'phoneNum']