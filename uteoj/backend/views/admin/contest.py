from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from backend.views.auth.login import LoginView
from backend.views.admin.require import admin_member_required



@admin_member_required
def AdminCreateContestView(request):

    return render(request, 'admin-template/contest/createcontest.html')


@admin_member_required
def AdminListContestView(request):

    return render(request, 'admin-template/contest/listcontest.html')
