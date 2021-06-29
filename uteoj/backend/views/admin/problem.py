from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required


def AdminListProblemView(request):
    context = {
        'website_header_title': 'Danh sách bài tập'
    }
    return render(request, 'admin-template/problem/listproblem.html', context)
