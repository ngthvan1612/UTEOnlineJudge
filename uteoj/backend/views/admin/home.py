from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from backend.views.auth.login import LoginView


@staff_member_required(login_url='/login/')
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
