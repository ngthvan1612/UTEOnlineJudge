from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from backend.models.problem import ProblemModel
from backend.models.problem import ProblemCategoryModel
from django.db.models import Q
from django.contrib import messages
from datetime import datetime
from random import random
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth import update_session_auth_hash


def UserChangePassword(request):
    if not request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        list_requiremenst = ['old_password', 'new_password1', 'new_password2']
        for x in list_requiremenst:
            if x not in request.POST:
                return HttpResponse(status=500)
        
        old_password = request.POST['old_password']
        new_password1 = request.POST['new_password1']
        new_password2 = request.POST['new_password2']

        if not request.user.check_password(old_password):
            messages.add_message(request, messages.ERROR, 'Mật khẩu cũ không đúng')
        elif len(new_password1) < 8:
            messages.add_message(request, messages.ERROR, 'Mật khẩu mới phải có độ dài >= 8 kí tự')
        elif new_password1 != new_password2:
            messages.add_message(request, messages.ERROR, 'Mật khẩu mới không khớp')
        else:
            request.user.set_password(new_password2)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.add_message(request, messages.SUCCESS, 'Đổi mật khẩu thành công')
        
        return HttpResponseRedirect(request.path_info)
    return render(request, 'user-template/changepassword.html')
