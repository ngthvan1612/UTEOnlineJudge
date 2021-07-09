from django.shortcuts import render
from django.contrib.auth.models import User
from backend.models.problem import ProblemModel
from backend.models.problem import ProblemCategoryModel
from django.db.models import Q

from datetime import datetime
from random import random

from backend.views.admin.require import admin_member_required

@admin_member_required
def AdminListProblemView(request):
    problem_models_filter = ProblemModel.objects
    if request.method == 'GET':
        if 'category' in request.GET:
            category = str(request.GET['category'])
            if category != 'All':
                problem_models_filter = problem_models_filter.filter(categories__in=[
                    z.id for z in ProblemCategoryModel.objects.filter(name=category)
                ]).distinct()
        if 'problemnamelike' in request.GET:
            problemnamelike = request.GET['problemnamelike']
            problem_models_filter = problem_models_filter.filter(Q(shortname__contains=problemnamelike) | Q(fullname__contains=problemnamelike))
    problem_models_filter = problem_models_filter.all()
    list_problems = [
        {
            'id': -1,
            'shortname': x.shortname,
            'fullname': x.fullname,
            'author': ', '.join([y.username for y in x.author.all()]),
            'publish_date': x.publish_date.strftime("%m/%d/%Y"),
            'categories': [y.name for y in x.categories.all()],
            'difficult': x.difficult,
            'problem_type': x.get_problem_type_display(),
        } for x in problem_models_filter
    ]
    for it in range(0, len(list_problems), 1):
        list_problems[it]['id'] = it + 1
    context = {
        'website_header_title': 'Danh sách bài tập',
        'list_problem': list_problems,
        'list_categories': ['All'] + [x.name for x in ProblemCategoryModel.objects.all()],
    }
    return render(request, 'admin-template/problem/listproblem.html', context)


@admin_member_required
def AdminCreateProblemView(request):

    return render(request, 'admin-template/problem/createproblem.html')
