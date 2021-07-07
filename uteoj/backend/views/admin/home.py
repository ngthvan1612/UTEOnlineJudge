from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from backend.views.auth.login import LoginView
from backend.views.admin.require import admin_member_required


@admin_member_required
def AdminHomeView(request):
    list_problems = [
        {
            'id': 1,
            'shortname': 'SUMAB',
            'fullname': 'Tinh tong 2 so nguyen AB'
        },
        {
            'id': 2,
            'shortname': 'MULAB',
            'fullname': 'Tinh tich 2 so nguyen AB'
        },
        {
            'id': 3,
            'shortname': 'POWERAB',
            'fullname': 'Mu 2 so nguyen AB'
        },
    ]
    context = {
        'website_header_title': 'Trang chu',
        'list_problems': list_problems,
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
