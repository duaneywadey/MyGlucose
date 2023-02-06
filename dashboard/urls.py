from django.urls import path
from . import views
from django.contrib.auth import views as authView

urlpatterns = [
	path('', views.index, name='dashboard-index'),
	path('signup/', views.signup, name='dashboard-signup'),
	path('login/', authView.LoginView.as_view(template_name='dashboard/login.html'), name='dashboard-log-in'),
	path('logout/', views.logout_view, name='dashboard-logout_view'),
	path('history/', views.history, name='dashboard-history'),
	path('diabetesdashboard/', views.addDashboard, name='dashboard-addDashboard')

	
]