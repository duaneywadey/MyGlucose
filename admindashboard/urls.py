from django.urls import path
from . import views
from .views import AdminDashboardLoginView
from django.contrib.auth import views as authView

urlpatterns = [
	path('', views.index, name='admindashboard-index'),
	path('login/', AdminDashboardLoginView.as_view(), name='admindashboard-login'),
	path('edit-profile/', views.editProfile, name='admindashboard-editProfile'),
	path('alldoctors/', views.viewAllDoctors, name='admindashboard-viewAllDoctors'),
	path('logout/', views.logout_view, name='admindashboard-logout_view'),
	path('signup/', views.signup, name='admindashboard-signup'),
	path('error/', views.error, name='admindashboard-error'),
	path('info/<int:user_id>/', views.patientInfo, name='admindashboard-patientInfo'),
	path('alldoctors/<int:user_id>/', views.doctorOnly, name='admindashboard-doctorOnly'),

]