from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login


def WhoView(request):
    msg = 'Trang này để test đăng nhập'
    per = 'Người dùng thường'
    if request.user.is_staff:
        per = 'Admin'
    return HttpResponse('<center><h1>' + 
        msg + '</br>Tên người dùng hiện tại: ' + 
        str(request.user) + '</br>Phân quyền: ' + per + '</h1></center>')


def LoginView(request):
    context = {
        'website_header_title': 'Đăng nhập',
    }
    if request.method == 'POST':
        list_requirements = ['username', 'password']
        for x in list_requirements:
            if x not in request.POST:
                return HttpResponse(status=500)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/who')
        context['login_error'] = 'Tên đăng nhập hoặc mật khẩu sai'
    request.method = 'GET'
    return render(request, 'auth-template/login.html', context)
