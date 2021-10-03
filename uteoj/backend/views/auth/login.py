import re
from django.conf import settings
from django.contrib import messages
from django.http.response import Http404
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from backend.task.sendmail import SendMail
from backend.models.settings import OJSettingModel
from backend.models.settings import CHANGE_PASSWORD_EMAIL_HANDLE_SETTING_NAME, CHANGE_PASSWORD_EMAIL_PASSWORD_SETTING_NAME
from backend.views.settings import REDIRECT_FIELD_NAME
from backend.models.usersetting import UserSetting


def WhoView(request):
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
            UserSetting.createSettingIfNotExists(user)
            if not user.usersetting.verified:
                messages.add_message(request, messages.ERROR, 'Tài khoản này chưa được xác thực')
            else:
                login(request, user)
                next_url = request.POST.get('next')
                if not next_url or len(next_url) == 0:
                    next_url = '/admin' if user.is_staff else '/'
                print('redir to ' + str(next_url))
                return redirect(next_url)
        else:
            messages.add_message(request, messages.ERROR, 'Tên đăng nhập hoặc mật khẩu sai')
    return render(request, 'auth-template/login.html', context)


def LogoutView(request):
    logout(request)
    return redirect('/')


def ForgotPasswordView(request):
    if request.user.is_authenticated:
        return redirect('/')
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
            messages.add_message(request, messages.ERROR, 'Vui lòng nhập đúng định dạng email')
        else:
            users = User.objects.filter(email=reset_email)
            if users.exists():
                subject = 'Password reset from UTE Online Judge'
                user = users[0]
                email_template = 'auth-template/forgotpassword.txt'
                c = {
                    "email": user.email,
                    "domain": "127.0.0.1:" + str(request.get_port()),
                    "site_name": "UTE ONLINE JUDGE",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": "user",
                    "token": default_token_generator.make_token(user),
                    "protocol": "http",
                }
                email = render_to_string(email_template, c)
                try:
                    SendMail.apply_async(
                        args=[subject, email, user.email],
                        queue='uteoj_system'
                    )
                except BadHeaderError:
                    messages.add_message(request, messages.ERROR, 'Có lỗi trong quá trình xử lý')
            messages.add_message(request, messages.SUCCESS, 'Nếu email này đã được được đăng ký, vui lòng kiểm tra hộp thư đến để đi đến liên kết đặt lại mật khẩu')
    return render(request, 'auth-template/forgotpassword.html', context)


def ForgotPasswordResetView(request, uidb64, token):
    try:
        uid = int(urlsafe_base64_decode(uidb64).decode('utf-8'))
    except UnicodeDecodeError:
        raise Http404()
    users = User.objects.filter(id=uid)
    if users.exists() == False:
        raise Http404()
    user = users[0]
    if default_token_generator.check_token(user, token) == False:
        raise Http404()
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
            messages.add_message(request, messages.ERROR, 'Mật khẩu phải dài ít nhất 8 ký tự')
        elif password1 != password2:
            messages.add_message(request, messages.ERROR, 'Mật khẩu không khớp')
        else:
            user.set_password(password1)
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Đổi mật khẩu thành công')
            return redirect('/login')
    return render(request, 'auth-template/newpassword.html', context)
