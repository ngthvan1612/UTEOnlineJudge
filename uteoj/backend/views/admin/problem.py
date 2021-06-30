from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from backend.models.problem import ProblemModel


def AdminListProblemView(request):
    list_problem = [
        {
            'id': -1,
            'shortname': x.shortname,
            'fullname': x.fullname,
            'author': ', '.join([y.username for y in x.author.all()]),
            'publish_date': x.publish_date.strftime("%H:%M:%S - %m/%d/%Y"),
            'categories': ', '.join([y.name for y in x.categories.all()]),
            'difficult': x.difficult,
        } for x in ProblemModel.objects.all()
    ]
    for it in range(0, len(list_problem), 1):
        list_problem[it]['id'] = it + 1
    context = {
        'website_header_title': 'Danh sách bài tập',
        'list_problem': list_problem,
    }
    return render(request, 'admin-template/problem/listproblem.html', context)
