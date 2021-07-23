from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from backend.views.auth.login import LoginView
from backend.views.admin.require import admin_member_required



@admin_member_required
def AdminListTagView(request):


    return render(request, 'admin-template/tags/listtag.html')



@admin_member_required
def AdminEditTagView(request, topic_name):

    return render(request, 'admin-template/tags/edittag.html')

