from django.urls import path
from . import views
from django.contrib.auth import views as authView

urlpatterns = [
	path('', views.index, name='dashboard-index'),
	path('predict/', views.predict, name='dashboard-predict'),
	path('predict/result', views.predictionResult, name='dashboard.predictionResult'),
	path('signup/', views.signup, name='dashboard-signup'),
	path('login/', authView.LoginView.as_view(template_name='dashboard/login.html'), name='dashboard-log-in'),
	path('logout/', views.logout_view, name='dashboard-logout_view'),
	path('history/', views.history, name='dashboard-history'),
	path('history/<int:pk>/', views.historyEdit, name='history-edit'),
	path('history/delete/<int:pk>/', views.historyDelete, name='history-delete'),
	path('history/predictions/<int:pk>', views.predictionEdit, name='prediction-edit'),
	path('history/delete/predictions/<int:pk>', views.predictionDelete, name='prediction-delete'),
	path('diabetesdashboard/', views.addDashboard, name='dashboard-addDashboard'),
	path('addandpredictdiabetes/', views.addAndPredictDiabetes, name='dashboard-addAndPredictDiabetes'),
	path('edit-profile/', views.editProfile, name='dashboard-editProfile')



	
]