from django.contrib import admin
from . models import DashboardData, PredictionData, ProfileModel, MessagePanel, Comment, VerificationPanel, Verification

# Register your models here.

admin.site.register(DashboardData)
admin.site.register(PredictionData)
admin.site.register(ProfileModel)
admin.site.register(MessagePanel)
admin.site.register(Comment)
admin.site.register(VerificationPanel)
admin.site.register(Verification)




