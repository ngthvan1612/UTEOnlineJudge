from django.http.response import HttpResponseRedirect
from backend.models.settings import OJSettingModel
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import re

from django.views.decorators.csrf import csrf_exempt

def countChar(pat, src):
    res = 0
    for c in src:
        if c in pat:
            res += 1
    return res

@csrf_exempt
def SignupView(request):
    context = {
        'website_header_title': 'Đăng ký',
    }
    if not OJSettingModel.getAllowRegister():
        messages.add_message(request, messages.ERROR, 'Hiện tại không được đăng ký tài khoản mới')
    elif request.method == 'POST':
        list_requirements = ['username', 'email', 'password1', 'password2']
        for x in list_requirements:
            if x not in request.POST:
                return HttpResponse(status=500)
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        pat = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
        if len(username) < 5 or len(username) > 20:
            messages.add_message(request, messages.ERROR, 'Tên đăng nhập phải có từ 5 đến 20 kí tự')
        elif not re.match("^[A-Za-z0-9_]*$", username) or countChar(pat, username) == 0:
            messages.add_message(request, messages.ERROR, 'Tên đăng nhập chỉ gồm các kí tự A-Za-z0-9_ và phải có ít nhất một ký tự a-z')
        elif User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Tên đăng nhập đã tồn tại')
        elif len(email) == 0:
            messages.add_message(request, messages.ERROR, 'Email không được trống')
        elif User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Email này đã được đăng ký')
        elif len(password1) < 8:
            messages.add_message(request, messages.ERROR, 'Mật khẩu phải ít nhất 8 kí tự')
        elif password1 != password2:
            messages.add_message(request, messages.ERROR, 'Mật khẩu không khớp')
        else:
            User.objects.create_user(username=username, email=email, password=password1)
            messages.add_message(request, messages.SUCCESS, 'Đăng ký thành công')
            return render(request, 'auth-template/login.html', context)
    return render(request, 'auth-template/signup.html', context)
