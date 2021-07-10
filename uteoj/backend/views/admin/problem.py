from django.shortcuts import render
from django.contrib.auth.models import User
from backend.models.problem import ProblemModel
from backend.models.problem import ProblemCategoryModel
from django.db.models import Q

from django.core.paginator import Paginator


from datetime import datetime
from random import random

from backend.views.admin.require import admin_member_required

@admin_member_required
def AdminListProblemView(request):
    '''
    for i in range(1, 100, 1):
        num = int(random() * 8) + 1
        lc = [x.id for x in ProblemCategoryModel.objects.order_by('?').all()[:num]]
        problem = ProblemModel.objects.create(publish_date=datetime.now(),
            shortname='BAI_TAP_' + str(i),
            fullname='Bai tap ' + str(i),
            difficult=round(random() * 10, 2),
            points_per_test=random() * 100,
            statement='bla bla',
            input_filename='BAI' + str(i) + '.INP',
            output_filename='BAI' + str(i) + '.OUT',
            time_limit=int(random() * 10000),
            memory_limit=int(random() * 1000000),
            problem_type=int(random() * 2),)
        problem.categories.set(lc)
        problem.save()
    '''    
    problem_models_filter = ProblemModel.objects
    if request.method == 'GET':
        if 'problem_type' in request.GET:
            problem_type = request.GET['problem_type'].lower()
            if problem_type == 'acm':
                problem_models_filter = problem_models_filter.filter(problem_type=0)
            if problem_type == 'oi':
                problem_models_filter = problem_models_filter.filter(problem_type=1)
        if 'category' in request.GET:
            category = str(request.GET['category'])
            list_categories_filter = category.split(",")
            if 'All' not in list_categories_filter:
                for x in list_categories_filter:
                    problem_models_filter = problem_models_filter.filter(categories__in=[
                        y.id for y in ProblemCategoryModel.objects.filter(name=x).all()
                    ]).distinct()
        if 'problemnamelike' in request.GET:
            problemnamelike = request.GET['problemnamelike']
            problem_models_filter = problem_models_filter.filter(Q(shortname__contains=problemnamelike) | Q(fullname__contains=problemnamelike))
        if 'orderby' in request.GET:
            orderby_query = request.GET['orderby']
            field = orderby_query
            if field[0] == '-':
                field = field[1:]
            if field == 'difficult':
                problem_models_filter = problem_models_filter.order_by(orderby_query)
    problem_models_filter = problem_models_filter.all()
    list_problems = [
        {
            'id': -1,
            'fullname': x.fullname,
            'shortname': x.shortname,
            'author': ', '.join([y.username for y in x.author.all()]),
            'publish_date': x.publish_date.strftime("%m/%d/%Y"),
            'categories': [y.name for y in x.categories.all()],
            'difficult': x.difficult,
            'problem_type': x.get_problem_type_display(),
        } for x in problem_models_filter
    ]
    for it in range(0, len(list_problems), 1):
        list_problems[it]['id'] = it + 1
    paginator = Paginator(list_problems, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'website_header_title': 'Danh sách bài tập',
        'list_problem': list_problems,
        'list_categories': ['All'] + [x.name for x in ProblemCategoryModel.objects.all()],
        'page_obj': page_obj,
    }


    return render(request, 'admin-template/problem/listproblem.html', context)
@admin_member_required
def AdminCreateProblemView(request):
    
    context = {
        
    }
    return render(request, 'admin-template/problem/createproblem.html', context)
