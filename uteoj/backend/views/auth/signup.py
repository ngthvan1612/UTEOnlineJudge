from django.http.response import Http404, HttpResponseRedirect
from backend.models.settings import OJSettingModel
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
import re
from django.core.mail import send_mail, BadHeaderError
from backend.task.sendmail import SendMail
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt

from backend.models.usersetting import UserSetting

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
        list_requirements = ['email', 'password1', 'password2']
        for x in list_requirements:
            if x not in request.POST:
                return HttpResponse(status=500)
        email = request.POST['email']
        email_addr, domain = email.split('@')
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if User.objects.filter(username=email_addr).exists():
            messages.add_message(request, messages.ERROR, 'Tên người dùng ' + email_addr + ' đã được đăng ký')
        elif len(email) == 0:
            messages.add_message(request, messages.ERROR, 'Email không được trống')
        elif User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Email này đã được đăng ký')
        elif len(password1) < 8:
            messages.add_message(request, messages.ERROR, 'Mật khẩu phải ít nhất 8 kí tự')
        elif password1 != password2:
            messages.add_message(request, messages.ERROR, 'Mật khẩu không khớp')
        else:
            if domain not in ['student.hcmute.edu.vn', 'hcmute.edu.vn']:
                messages.add_message(request, messages.ERROR, 'Vui lòng sử dụng email trường để đăng ký tài khoản')
            else:
                user = User.objects.create_user(username=email_addr, email=email, password=password1)
                user.save()
                UserSetting.createSettingIfNotExists(user=user)

                subject = 'Xác nhận tài khoản'
                email_template = 'auth-template/verifyEmail.txt'
                c = {
                    "email": user.email,
                    "domain": OJSettingModel.getDeployAddr(),
                    "site_name": "UTE ONLINE JUDGE",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": "user",
                    "token": default_token_generator.make_token(user),
                    "protocol": "http",
                }
                try:
                    settings.EMAIL_HOST_USER = OJSettingModel.getSTMPEmail()
                    settings.EMAIL_HOST_PASSWORD = OJSettingModel.getSTMPPassword()
                    settings.EMAIL_USE_TLS = OJSettingModel.getSTMPEnableTLS()
                    settings.EMAIL_HOST = OJSettingModel.getSTMPServer()
                    settings.EMAIL_PORT = OJSettingModel.getSTMPPort()
                    print('port = ' + str(settings.EMAIL_PORT))
                    send_mail(subject, render_to_string(email_template, c), settings.EMAIL_HOST_USER, [email], fail_silently=False)
                except:
                    messages.add_message(request, messages.ERROR, 'Có lỗi trong quá trình xử lý, vui lòng thử lại sau ít phút')
                    user.delete()
                    return render(request, 'auth-template/signup.html', context)

                messages.add_message(request, messages.SUCCESS, 'Một liên kết xác thực tài khoản đã được gửi đến {}. Vui lòng kiểm tra hộp thư và xác nhận.'.format(email))
                return render(request, 'auth-template/signup.html', context)
    return render(request, 'auth-template/signup.html', context)

def VerifyEmailView(request, uidb64, token):
    try:
        uid = int(urlsafe_base64_decode(uidb64).decode('utf-8'))
    except UnicodeDecodeError:
        raise Http404()
    users = User.objects.filter(id=uid)
    if users.exists() == False:
        raise Http404()
    user = users[0]
    if user.usersetting.verified:
        raise Http404()
    if default_token_generator.check_token(user, token) == False:
        raise Http404()
    default_token_generator.make_token(user)
    user.usersetting.verified = True
    user.usersetting.save()
    messages.add_message(request, messages.SUCCESS, 'Xác nhận thành công')
    return redirect('/login')
