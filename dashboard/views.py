from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import DashboardData, PredictionData, ProfileModel, MessagePanel
from admindashboard.models import DoctorModel
from .forms import DashboardDataForm, SignUpForm, PredictionDataForm, EditDashboardDataForm, EditPredictionDataForm, UserUpdateForm, ProfileUpdateForm, CommentForm
from .decorators import patient_only
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Avg
from django.shortcuts import redirect 
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User, Group
from django.contrib.auth.views import LoginView
from django.views.generic import View
from django.http import HttpResponse
from .utils import render_to_pdf 
import joblib

class DashboardLoginView(LoginView):
    template_name = 'dashboard/login.html'

def predict(request):
	return render(request, 'dashboard/predict(nosignin).html')


def predictionResult(request):
	height = float(request.POST.get('height'))
	weight = float(request.POST.get('weight'))
	bmi = round(weight / ((height)**2),1)
	dpf = float(request.POST.get('dpf'))
	age	= int(request.POST.get('age'))
	
	model = joblib.load('model/updated_ml_model_diabetes')
	prediction = model.predict_proba([[bmi, dpf, age]])[:, 1]
	prediction = int(prediction * 100)

	context = {
		'height':height,
		'weight':weight,
		'bmi':bmi,
		'dpf':dpf,
		'age':age,
		'prediction':prediction
	}

	return render(request, 'dashboard/result.html', context)


@login_required(login_url='dashboard-login')
@patient_only
def index(request):
	dashboardInfo = DashboardData.objects.filter(author = request.user)
	avgGlucose = DashboardData.objects.filter(author = request.user).aggregate(Avg('glucose')).get('glucose__avg')
	avgWeight = DashboardData.objects.filter(author = request.user).aggregate(Avg('weight')).get('weight__avg')
	avgSystolic = DashboardData.objects.filter(author = request.user).aggregate(Avg('systolic_bp')).get('systolic_bp__avg')
	avgDiastolic = DashboardData.objects.filter(author = request.user).aggregate(Avg('diastolic_bp')).get('diastolic_bp__avg')

	message_panel = MessagePanel.objects.get(user=request.user)
	comments = message_panel.comments.all()

	if request.method == 'POST':
		c_form = CommentForm(request.POST)
		if c_form.is_valid():
			instance = c_form.save(commit=False)
			instance.author = request.user
			instance.message_panel = message_panel
			instance.save()
			return redirect('dashboard-index')
	else:
		c_form = CommentForm()

	context = {
		'dashboardInfo':dashboardInfo,
		'avgGlucose':avgGlucose,
		'avgWeight':avgWeight,
		'avgSystolic':avgSystolic,
		'avgDiastolic':avgDiastolic,
		'comments':comments,
		'c_form':c_form

	}

	return render(request, 'dashboard/index.html', context)


@login_required(login_url='dashboard-login')
@patient_only
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


@login_required(login_url='dashboard-login')
@patient_only
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

@login_required(login_url='dashboard-login')
@patient_only
def history(request):
	dashboardInfo = DashboardData.objects.filter(author = request.user)
	predictionInfo = PredictionData.objects.filter(author = request.user)

	context = {
		'dashboardInfo': dashboardInfo,
		'predictionInfo':predictionInfo
	}

	return render(request, 'dashboard/history.html', context)

@login_required(login_url='dashboard-login')
@patient_only
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

@login_required(login_url='dashboard-login')
@patient_only
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
	
	
@login_required(login_url='dashboard-login')
@patient_only
def historyDelete(request,pk):
	dashboardSingleInfo = DashboardData.objects.get(id=pk)

	if request.method == 'POST':
		dashboardSingleInfo.delete()
		return redirect('dashboard-history')

	context = {
		dashboardSingleInfo: 'dashboardSingleInfo'
	}

	return render(request, 'dashboard/delete-dashboard-history.html', context)

@login_required(login_url='dashboard-login')
@patient_only
def predictionDelete(request,pk):
	predictionSingleInfo = PredictionData.objects.get(id=pk)

	if request.method == 'POST':
		predictionSingleInfo.delete()
		return redirect('dashboard-history')

	context = {
		predictionSingleInfo: 'predictionSingleInfo'
	}

	return render(request, 'dashboard/delete-prediction-history.html', context)

@login_required(login_url='dashboard-login')
@patient_only
def editProfile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('dashboard-editProfile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'dashboard/edit-profile.html', context)




# if request.method == 'POST':
#     form = RegistrationForm(request.POST)

#     if form.is_valid():
#         user = form.save(commit=False)

#         user.save()

#         user_group = Group.objects.get(name='Mygroup') 

#         user.groups.add(user_group)



def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)

		if form.is_valid():
			user = form.save(commit=False)
			user.save()
			user_group = Group.objects.get(name='patients')
			user.groups.add(user_group)
			return redirect('dashboard-index')

	else:
		form = SignUpForm()


	context = {
		'form':form,
	}

	return render(request, 'dashboard/sign_up.html', context)


@login_required(login_url='dashboard-login')
@patient_only
def logout_view(request):
	logout(request)
	return render(request, 'dashboard/logout.html')



@login_required(login_url='dashboard-login')
@patient_only
def viewAllDoctors(request):
    User = get_user_model()
    allDoctors = User.objects.filter(groups__name='doctors')
    
    query = request.GET.get('q', '')
    if query:
        allDoctors = allDoctors.filter(
            Q(username__icontains=query) 
        ).distinct()
    
    context = {
        'allDoctors':allDoctors,
        'query': query
    }
    return render(request, 'dashboard/alldoctors.html', context)

@login_required(login_url='dashboard-login')
@patient_only
def doctorOnly(request, user_id):
	user = get_object_or_404(User, pk=user_id)
	profile_data = DoctorModel.objects.filter(user=user)
	print(profile_data)

	context = {
		'profile_data':profile_data
	}
	return render(request, 'dashboard/doctorinfo.html', context)	





















# ADMIN VIEWS TEST

def indexAdmin(request):
	User = get_user_model()
	users = User.objects.all()

	context = {
		'users': users
	}
	return render(request, 'dashboard/adminprofiletest.html', context)

def info(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    dashboard_data = DashboardData.objects.filter(author=user)
    prediction_data = PredictionData.objects.filter(author=user)

    context = {
        'user': user,
        'dashboard_data': dashboard_data,
        'prediction_data': prediction_data,
    }
    return render(request, 'dashboard/admininfo.html', context)




# FOR PDF REPORT

class GeneratePdf(View):
    def get(self, request, *args, **kwargs):
        dashboardInfo = DashboardData.objects.filter(author = request.user)
        predictionInfo = PredictionData.objects.filter(author = request.user)
        profileInfo = ProfileModel.objects.filter(user = request.user)
        data = {
        	'dashboardInfo':dashboardInfo,
        	'predictionInfo':predictionInfo,
        	'profileInfo':profileInfo
        }
        pdf = render_to_pdf('dashboard/report.html',data)
        if pdf:
            response=HttpResponse(pdf,content_type='application/pdf')
            filename = "Report"
            content = "inline; filename= %s" %(filename)
            response['Content-Disposition']=content
            return response
        return HttpResponse("Page Not Found")




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



# Superadmin creates doctor accounts
# Decorators - to prevent patients from logging in to admin

#  --- GROUP REGISTRATION ---

# if request.method == 'POST':
#     form = RegistrationForm(request.POST)

#     if form.is_valid():
#         user = form.save(commit=False)

#         user.save()

#         user_group = Group.objects.get(name='Mygroup') 

#         user.groups.add(user_group)

#         #log the user in
#         login(request, user)

#         return redirect('/summury')

# else:

#     form = RegistrationForm()

# return render(request, 'account/pages/register.html', {'form':form})



# Getting all members in a group 

# users = User.objects.filter(groups__name='group_name')

