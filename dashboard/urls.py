from django.urls import path
from . import views
from .views import DashboardLoginView, GeneratePdf
from django.contrib.auth import views as authView

urlpatterns = [
	path('', views.index, name='dashboard-index'),
	path('predict/', views.predict, name='dashboard-predict'),
	path('predict/result', views.predictionResult, name='dashboard.predictionResult'),
	path('signup/', views.signup, name='dashboard-signup'),
	path('login/', DashboardLoginView.as_view(), name='dashboard-login'),
	path('logout/', views.logout_view, name='dashboard-logout_view'),
	path('history/', views.history, name='dashboard-history'),
	path('history/<int:pk>/', views.historyEdit, name='history-edit'),
	path('history/delete/<int:pk>/', views.historyDelete, name='history-delete'),
	path('history/predictions/<int:pk>', views.predictionEdit, name='prediction-edit'),
	path('history/delete/predictions/<int:pk>', views.predictionDelete, name='prediction-delete'),
	path('diabetesdashboard/', views.addDashboard, name='dashboard-addDashboard'),
	path('addandpredictdiabetes/', views.addAndPredictDiabetes, name='dashboard-addAndPredictDiabetes'),
	path('edit-profile/', views.editProfile, name='dashboard-editProfile'),
	path('indexadmin/', views.indexAdmin, name='dashboard-indexAdmin'),
	path('indexadmin/info/<int:user_id>/', views.info, name='dashboard-info'),
    path('pdf/', GeneratePdf.as_view(),name='dashboard-pdf'),
	path('alldoctors/', views.viewAllDoctors, name='dashboard-viewAllDoctors'),
	path('alldoctors/<int:user_id>/', views.doctorOnly, name='dashboard-doctorOnly') 





	
]