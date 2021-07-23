import re
from django.conf import settings
from django.contrib import messages
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout

from backend.models.settings import OJSettingModel
from backend.models.settings import CHANGE_PASSWORD_EMAIL_HANDLE_SETTING_NAME, CHANGE_PASSWORD_EMAIL_PASSWORD_SETTING_NAME
from backend.views.settings import REDIRECT_FIELD_NAME
from uteoj.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD


def WhoView(request):
    print('cnt user = {}'.format(User.objects.count()))
    msg = 'Trang này để test đăng nhập'
    per = 'Người dùng thường'
    if request.user.is_staff:
        per = 'Admin'
    return HttpResponse('<center><h1>' + 
        msg + '</br>Tên người dùng hiện tại: ' + 
        str(request.user) + '</br>Phân quyền: ' + per + '</h1></center>')


def LoginView(request):
    if request.user.is_staff == True:
        return redirect('/admin/')
    context = {
        'website_header_title': 'Đăng nhập',
    }
    if request.method == 'GET' and REDIRECT_FIELD_NAME in request.GET:
        messages.add_message(request, messages.ERROR, 'Vui lòng đăng nhập với quyền admin để tiếp tục')
    elif request.method == 'POST':
        list_requirements = ['username', 'password']
        for x in list_requirements:
            if x not in request.POST:
                return HttpResponse(status=500)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if REDIRECT_FIELD_NAME in request.POST:
                print('-------------> ' + request.POST[REDIRECT_FIELD_NAME])
                return redirect(request.POST[REDIRECT_FIELD_NAME])
            if user.is_staff:
                return redirect('/admin/')
            return redirect('/who')
        messages.add_message(request, messages.ERROR, 'Tên đăng nhập hoặc mật khẩu sai')
    return render(request, 'auth-template/login.html', context)


def LogoutView(request):
    logout(request)
    return redirect('/')


def ForgotPasswordView(request):
    context = {
        'website_header_title': 'Quen mat khau',
    }
    if request.method == 'POST':
        list_requirements = ['reset_email']
        for x in list_requirements:
            if x not in request.POST:
                return HttpResponse(status=500)
        reset_email = request.POST['reset_email']
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', reset_email):
            context['error_forgot_password'] = 'Vui lòng nhập đúng địa chỉ email'
        else:
            users = User.objects.filter(email=reset_email)
            if users.exists():
                subject = 'Password reset from UTE Online Judge'
                user = users[0]
                email_template = 'auth-template/forgotpassword.txt'
                c = {
                    "email": user.email,
                    "domain": "127.0.0.1:8000",
                    "site_name": "UTE ONLINE JUDGE",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": "user",
                    "token": default_token_generator.make_token(user),
                    "protocol": "http",
                }
                email = render_to_string(email_template, c)
                try:
                    settings.EMAIL_HOST_USER = OJSettingModel.get(CHANGE_PASSWORD_EMAIL_HANDLE_SETTING_NAME)
                    settings.EMAIL_HOST_PASSWORD = OJSettingModel.get(CHANGE_PASSWORD_EMAIL_PASSWORD_SETTING_NAME)
                    send_mail(subject, email, EMAIL_HOST_USER, [user.email], fail_silently=False)
                except BadHeaderError:
                    context['error_forgot_password'] = 'Có lỗi trong quá trình xử lý'
            context['success_forgot_password'] = 'Nếu email này đã được được đăng ký, vui lòng kiểm tra hộp thư đến để đi đến liên kết đặt lại mật khẩu'
    return render(request, 'auth-template/forgotpassword.html', context)


def ForgotPasswordResetView(request, uidb64, token):
    try:
        uid = int(urlsafe_base64_decode(uidb64).decode('utf-8'))
    except UnicodeDecodeError:
        return HttpResponse(status=500)
    users = User.objects.filter(id=uid)
    if users.exists() == False:
        return HttpResponse(status=500)
    user = users[0]
    if default_token_generator.check_token(user, token) == False:
        return HttpResponse(status=500)
    context = {
        'website_header_title': 'New password',
    }
    if request.method == 'POST':
        list_requirements = ['password1', 'password2']
        for x in list_requirements:
            if x not in request.POST:
                return HttpResponse(status=500)
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if len(password1) < 8:
            context['error_new_password'] = 'Mật khẩu phải ít nhất 8 kí tự'
        elif password1 != password2:
            context['error_new_password'] = 'Mật khẩu không khớp'
        else:
            user.set_password(password1)
            user.save()
            context['success_new_password'] = 'Đổi mật khẩu thành công'
    return render(request, 'auth-template/newpassword.html', context)
