from django.contrib import admin
from . models import DashboardData, PredictionData, ProfileModel, MessagePanel, Comment

# Register your models here.

admin.site.register(DashboardData)
admin.site.register(PredictionData)
admin.site.register(ProfileModel)
admin.site.register(MessagePanel)
admin.site.register(Comment)



