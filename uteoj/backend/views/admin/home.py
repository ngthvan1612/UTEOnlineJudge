from backend.models.settings import OJSettingModel
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from backend.views.auth.login import LoginView
from backend.views.admin.require import admin_member_required
from backend.models.problem import ProblemModel
from django.contrib.auth.models import User
from django.http import HttpResponse

def Error404Page(request, exception):

    return HttpResponse('Not found')

@admin_member_required
def AdminHomeView(request):
    list_problems = ProblemModel.objects.order_by('-id').all()[:2]
    context = {
        'website_header_title': 'Trang chu',
        'list_problems': list_problems,
        'problems_count': ProblemModel.objects.count(),
        'users_count': User.objects.count(),
    }
    return render(request, 'admin-template/index.html', context)


@admin_member_required
def AdminSubmissionStatusView(request):

    return render(request, 'admin-template/Status/status.html')


@admin_member_required
def AdminRankingView(request):

    return render(request, 'admin-template/rank.html')


@admin_member_required
def AdminContactView(request):

    return render(request, 'admin-template/contact.html')


@admin_member_required
def AdminSettingView(request):
    if request.method == 'POST':
        allow_submission = 'allow_submission' in request.POST
        allow_register = 'allow_register' in request.POST
        OJSettingModel.setAllowSubmission(allow_submission)
        OJSettingModel.setAllowRegister(allow_register)
        return HttpResponseRedirect(request.path_info) # remove post dasta
    elif request.method == 'GET':
        context = {
            'allow_submission': OJSettingModel.getAllowSubmission(),
            'allow_register': OJSettingModel.getAllowRegister(),
        }
        return render(request, 'admin-template/Setting/setting.html', context)
    else:
        return HttpResponse(status=405) # method is not allowed
    

@admin_member_required
def AdminSettingSTMP(request):
    if request.method == 'POST':
        server = request.POST['server'] if 'server' in request.POST else ''
        email = request.POST['email'] if 'email' in request.POST else ''
        port = request.POST['port'] if 'port' in request.POST else ''
        password = request.POST['password'] if 'password' in request.POST else ''
        tls = 'tls' in request.POST
        OJSettingModel.setSTMPServer(server)
        OJSettingModel.setSTMPEmail(email)
        OJSettingModel.setSTMPPort(port)
        OJSettingModel.setSTMPPassword(password)
        OJSettingModel.setSTMPEnableTLS(tls)
        return HttpResponseRedirect(request.path_info) # remove post dasta
    elif request.method == 'GET':
        context = {
            'server': OJSettingModel.getSTMPServer(),
            'email': OJSettingModel.getSTMPEmail(),
            'port': OJSettingModel.getSTMPPort(),
            #'password': OJSettingModel.getSTMPPassword(),
            'tls': OJSettingModel.getSTMPEnableTLS()
        }
        return render(request, 'admin-template/Setting/stmp.html', context)
    else:
        return HttpResponse(status=405) # method is not allowed
