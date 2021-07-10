from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from backend.views.auth.login import LoginView
from backend.views.admin.require import admin_member_required
from backend.models.problem import ProblemModel
from django.contrib.auth.models import User

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


    return render(request, 'admin-template/Setting/setting.html')
