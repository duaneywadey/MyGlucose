from django.contrib.auth.decorators import user_passes_test

def is_admin(user):
    return user.groups.filter(name='doctors').exists()

admin_only = user_passes_test(is_admin, login_url='admindashboard-error')
