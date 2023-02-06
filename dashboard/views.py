from django.shortcuts import render
from .models import DashboardData
from .forms import DashboardDataForm, SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.db.models import Avg
from django.shortcuts import redirect 

@login_required
def index(request):
	dashboardInfo = DashboardData.objects.filter(author = request.user)
	avgGlucose = round(DashboardData.objects.filter(author = request.user).aggregate(Avg('glucose')).get('glucose__avg'),2)
	avgWeight = round(DashboardData.objects.filter(author = request.user).aggregate(Avg('weight')).get('weight__avg'), 2)
	avgSystolic = round(DashboardData.objects.filter(author = request.user).aggregate(Avg('systolic_bp')).get('systolic_bp__avg'),2)
	avgDiastolic = round(DashboardData.objects.filter(author = request.user).aggregate(Avg('diastolic_bp')).get('diastolic_bp__avg'),2)
	context = {
		'dashboardInfo':dashboardInfo,
		'avgGlucose':avgGlucose,
		'avgWeight':avgWeight,
		'avgSystolic':avgSystolic,
		'avgDiastolic':avgDiastolic
	}

	return render(request, 'dashboard/index.html', context)


@login_required
def addDashboard(request):
	dashboardInfo = DashboardData.objects.all()

	if request.method == 'POST':
		form = DashboardDataForm(request.POST)
		if form.is_valid():
		
			instance = form.save(commit=False) 
			instance.author = request.user

			# Save our form
			instance.save()
			return redirect('dashboard-index')
	else:
		form = DashboardDataForm()

	context = {
		'form':form,
		'dashboardInfo':dashboardInfo
	}
	return render(request, 'dashboard/diabetestracker.html', context)


def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			print(form)
			return redirect('dashboard-index')

	else:
		form = SignUpForm()


	context = {
		'form':form,
	}

	return render(request, 'dashboard/sign_up.html', context)

def logout_view(request):
	logout(request)
	return render(request, 'dashboard/logout.html')

def history(request):
	countryInfo = CountryData.objects.all()
	context = {
		'countryInfo':countryInfo
	}
	return render(request, 'dashboard/history.html', context)