from django.contrib import admin
from . models import DashboardData, PredictionData, ProfileModel

# Register your models here.

admin.site.register(DashboardData)
admin.site.register(PredictionData)
admin.site.register(ProfileModel)

