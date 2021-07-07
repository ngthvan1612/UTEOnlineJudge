from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from backend.views.auth.login import LoginView
from backend.views.admin.require import admin_member_required
from django.contrib.auth.models import User
from django.http import HttpResponse

@admin_member_required
def AdminListAdministratorsView(request):


    return render(request, 'admin-template/user/listAdmin.html')

@admin_member_required
def AdminListUsersView(request):

    
    return render(request, 'admin-template/user/listContestant.html')


@admin_member_required
def AdminEditUserView(request, user_name):
    if not User.objects.filter(username=user_name).exists():
        return HttpResponse(status=404)
    return render(request, 'admin-template/user/profile.html')
