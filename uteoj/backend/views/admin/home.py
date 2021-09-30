from django.db.models.fields import BooleanField
from backend.models.settings import OJSettingModel
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from backend.views.auth.login import LoginView
from backend.views.admin.require import admin_member_required
from backend.models.problem import PROBLEM_DIFFICULT_CHOICES, PROBLEM_TYPE_CHOICES, SUBMISSION_VISIBLE_MODE_CHOICES, ProblemModel
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings

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

        if not port.isdigit():
            messages.add_message(request, messages.ERROR, 'Port phải là số nguyên')
            return redirect('/admin/setting/stmp')

        OJSettingModel.setSTMPServer(server)
        OJSettingModel.setSTMPEmail(email)
        OJSettingModel.setSTMPPort(port)
        if len(password) > 0:
            OJSettingModel.setSTMPPassword(password)
        OJSettingModel.setSTMPEnableTLS(tls)
        return HttpResponseRedirect(request.path_info) # remove post dasta
    elif request.method == 'GET':
        context = {
            'server': OJSettingModel.getSTMPServer(),
            'email': OJSettingModel.getSTMPEmail(),
            'port': OJSettingModel.getSTMPPort(),
            'tls': OJSettingModel.getSTMPEnableTLS()
        }
        return render(request, 'admin-template/Setting/stmp.html', context)
    else:
        return HttpResponse(status=405) # method is not allowed

@admin_member_required
def AdminSettingProblemDetault(request):
    if request.method == 'POST':
        try:
            _ = int(request.POST.get('time_limit'))
        except:
            messages.add_message(request, messages.ERROR, 'Giới hạn thời gian phải là số nguyên')
            return redirect('/admin/setting/problemdefault')
        
        try:
            _ = int(request.POST.get('memory_limit'))
        except:
            messages.add_message(request, messages.ERROR, 'Giới hạn bộ nhớ phải là số nguyên')
            return redirect('/admin/setting/problemdefault')
        
        try:
            _ = float(request.POST.get('points_per_test'))
        except:
            messages.add_message(request, messages.ERROR, 'Điểm mỗi test phải là số thực')
            return redirect('/admin/setting/problemdefault')

        data = {
            'is_public': True if 'is_public' in request.POST else False,
            'problem_type': int(request.POST.get('problem_type')),
            'time_limit': int(request.POST.get('time_limit')),
            'memory_limit': int(request.POST.get('memory_limit')),
            'submission_visible_mode': int(request.POST.get('submission_visible_mode')),
            'difficult': int(request.POST.get('difficult')),
            'points_per_test': round(float(request.POST.get('points_per_test')), settings.NUMBER_OF_DECIMAL),
        }

        OJSettingModel.setDefaultProblemConfig(data)
        messages.add_message(request, messages.SUCCESS, 'Cập nhật thành công')
        return redirect('/admin/setting/problemdefault')
    elif request.method == 'GET':
        data = OJSettingModel.getDefaultProblemConfig()
        context = {
            'problem_type': data['problem_type'],
            'time_limit': data['time_limit'],
            'memory_limit': data['memory_limit'],
            'submission_visible_mode': data['submission_visible_mode'],
            'difficult': data['difficult'],
            'points_per_test': data['points_per_test'],
            'list_difficult': [
                {
                    'name': x[1],
                    'value': x[0]
                }
            for x in PROBLEM_DIFFICULT_CHOICES],
            'list_submode': [
                {
                    'value': x[0],
                    'name': x[1],
                } for x in SUBMISSION_VISIBLE_MODE_CHOICES
            ],
            'list_problemtype': [
                {
                    'value': x[0],
                    'name': x[1]
                } for x in PROBLEM_TYPE_CHOICES
            ],
        }
        if data['is_public']:
            context['is_public'] = True
        return render(request, 'admin-template/Setting/problemdefault.html', context)
    else:
        return HttpResponse(status=405) # method is not allowed
