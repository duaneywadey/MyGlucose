from django.contrib import admin
from . models import DashboardData, PredictionData

# Register your models here.

admin.site.register(DashboardData)
admin.site.register(PredictionData)
