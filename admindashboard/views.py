from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect 
from .forms import SignUpForm, CommentForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import logout
from dashboard.models import DashboardData, PredictionData, ProfileModel
from dashboard.models import MessagePanel, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .decorators import admin_only
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.db.models import Avg


class AdminDashboardLoginView(LoginView):
    template_name = 'admindashboard/login.html'

@login_required(login_url='admindashboard-login')
@admin_only
def index(request):
	User = get_user_model()
	users = User.objects.filter(groups__name='patients')

	context = {
		'users': users
	}
	return render(request, 'admindashboard/index.html', context)

@login_required(login_url='admindashboard-login')
@admin_only
def patientInfo(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	dashboard_data = DashboardData.objects.filter(author=user)
	prediction_data = PredictionData.objects.filter(author=user)
	profile_data = ProfileModel.objects.filter(user=user)
	avgGlucose = DashboardData.objects.filter(author=user).aggregate(Avg('glucose')).get('glucose__avg')
	avgWeight = DashboardData.objects.filter(author=user).aggregate(Avg('weight')).get('weight__avg')
	avgSystolic = DashboardData.objects.filter(author=user).aggregate(Avg('systolic_bp')).get('systolic_bp__avg')
	avgDiastolic = DashboardData.objects.filter(author=user).aggregate(Avg('diastolic_bp')).get('diastolic_bp__avg')
	message_panel = MessagePanel.objects.get(user=user)
	comments = message_panel.comments.all()

	if request.method == 'POST':
		c_form = CommentForm(request.POST)
		if c_form.is_valid():
			instance = c_form.save(commit=False)
			instance.author = request.user
			instance.message_panel = message_panel
			instance.save()
			return redirect('admindashboard-patientInfo', user.id)
	else:
		c_form = CommentForm()

	context = {
		'user': user,
		'dashboard_data': dashboard_data,
		'prediction_data': prediction_data,
		'profile_data' : profile_data,
		'avgGlucose':avgGlucose,
		'avgWeight':avgWeight,
		'avgSystolic':avgSystolic,
		'avgDiastolic':avgDiastolic,
		'comments':comments,
		'c_form':c_form
	}
	return render(request, 'admindashboard/info.html', context)

@login_required(login_url='dashboard-login')
@admin_only
def editProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('admindashboard-editProfile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'admindashboard/edit-profile.html', context)




def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)

		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			user_group = Group.objects.get(name='doctors')
			user.groups.add(user_group)
			return redirect('admindashboard-index')

	else:
		form = SignUpForm()


	context = {
		'form':form,
	}

	return render(request, 'admindashboard/sign_up.html', context)


@admin_only
def logout_view(request):
	logout(request)
	return render(request, 'admindashboard/logout.html')

def error(request):
	return render(request, 'admindashboard/error.html')
