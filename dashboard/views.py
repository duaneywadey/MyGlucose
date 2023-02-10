from django.shortcuts import render
from .models import DashboardData, PredictionData
from .forms import DashboardDataForm, SignUpForm, PredictionDataForm, EditDashboardDataForm, EditPredictionDataForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.db.models import Avg
from django.shortcuts import redirect 



@login_required
def index(request):
	dashboardInfo = DashboardData.objects.filter(author = request.user)
	avgGlucose = round(DashboardData.objects.filter(author = request.user).aggregate(Avg('glucose')).get('glucose__avg'),2)
	avgWeight = round(DashboardData.objects.filter(author = request.user).aggregate(Avg('weight')).get('weight__avg'), 2)
	avgSystolic = round(DashboardData.objects.filter(author = request.user).aggregate(Avg('systolic_bp')).get('systolic_bp__avg'))
	avgDiastolic = round(DashboardData.objects.filter(author = request.user).aggregate(Avg('diastolic_bp')).get('diastolic_bp__avg'))
	context = {
		'dashboardInfo':dashboardInfo,
		'avgGlucose':avgGlucose,
		'avgWeight':avgWeight,
		'avgSystolic':avgSystolic,
		'avgDiastolic':avgDiastolic,
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


@login_required
def addAndPredictDiabetes(request):
	predicted_values = PredictionData.objects.filter(author = request.user)

	if request.method == 'POST':
		form = PredictionDataForm(request.POST)
		if form.is_valid():
			instance = form.save(commit=False) 
			instance.author = request.user

			# Save our form
			instance.save()
			return redirect('dashboard-addAndPredictDiabetes')
	else:
		form = PredictionDataForm()
	context	= {
		'form':form,
		'predicted_values':predicted_values
	}

	return render(request, 'dashboard/predictdiabetes.html', context)

@login_required
def history(request):
	dashboardInfo = DashboardData.objects.filter(author = request.user)
	predictionInfo = PredictionData.objects.filter(author = request.user)

	context = {
		'dashboardInfo': dashboardInfo,
		'predictionInfo':predictionInfo
	}

	return render(request, 'dashboard/history.html', context)

@login_required
def historyEdit(request, pk):
	dashboardSingleInfo = DashboardData.objects.get(id=pk)
	if request.method == 'POST':
		form = DashboardDataForm(request.POST, instance=dashboardSingleInfo)
		if form.is_valid():
			form.save()
			return redirect('dashboard-history')
	else:
		form = DashboardDataForm(instance=dashboardSingleInfo)
	context = {
		'dashboardSingleInfo': dashboardSingleInfo,
		'form': form,
	}
	return render(request, 'dashboard/edit-dashboard-history.html', context)

@login_required
def predictionEdit(request, pk):
	predictionSingleInfo = PredictionData.objects.get(id=pk)
	if request.method == 'POST':
		form_prediction = EditPredictionDataForm(request.POST, instance=predictionSingleInfo)
		if form_prediction.is_valid():
			form_prediction.save()
			return redirect('dashboard-history')
	else:
		form_prediction = EditPredictionDataForm(instance=predictionSingleInfo)
	context = {
		'predictionSingleInfo': predictionSingleInfo,
		'form_prediction': form_prediction,
	}
	return render(request, 'dashboard/edit-prediction-history.html', context)
	
	

def historyDelete(request,pk):
	dashboardSingleInfo = DashboardData.objects.get(id=pk)

	if request.method == 'POST':
		dashboardSingleInfo.delete()
		return redirect('dashboard-history')

	context = {
		dashboardSingleInfo: 'dashboardSingleInfo'
	}

	return render(request, 'dashboard/delete-dashboard-history.html', context)


def predictionDelete(request,pk):
	predictionSingleInfo = PredictionData.objects.get(id=pk)

	if request.method == 'POST':
		predictionSingleInfo.delete()
		return redirect('dashboard-history')

	context = {
		predictionSingleInfo: 'predictionSingleInfo'
	}

	return render(request, 'dashboard/delete-prediction-history.html', context)



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


# Getting all users

# from django.contrib.auth import get_user_model
# User = get_user_model()
# users = User.objects.all()



# One to many relationship

# class Business(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
# class Job(models.Model):
#     business = models.ForeignKey(Business, on_delete= models.CASCADE)

# Job.objects.filter(business__user=user) 

