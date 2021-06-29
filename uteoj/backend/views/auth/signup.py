from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import re

def SignupView(request):
    context = {
        'website_header_title': 'Đăng ký',
    }
    if request.method == 'POST':
        list_requirements = ['username', 'email', 'password1', 'password2']
        for x in list_requirements:
            if x not in request.POST:
                return HttpResponse(status=500)
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if len(username) < 5:
            context['signup_error'] = 'Tên đăng nhập phải có từ 5 kí tự trở lên'
        elif re.match("^[A-Za-z0-9_-]*$", username) == False:
            context['signup_error'] = 'Tên đăng nhập chỉ gồm các kí tự A-Za-z0-9 và _'
        elif User.objects.filter(username=username).exists():
            context['signup_error'] = 'Tên đăng nhập đã tồn tại'
        elif len(email) == 0:
            context['signup_error'] = 'Email không được trống'
        elif User.objects.filter(email=email).exists():
            context['signup_error'] = 'Email này đã được đăng ký'
        elif len(password1) < 8:
            context['signup_error'] = 'Mật khẩu phải ít nhất 8 kí tự'
        elif password1 != password2:
            context['signup_error'] = 'Mật khẩu không khớp'
        else:
            User.objects.create_user(username=username, email=email, password=password1)
            context['signup_success'] = 'Đăng ký thành công'
    return render(request, 'auth-template/signup.html', context)
