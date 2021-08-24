from backend.views.user.home import UserHomeView
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from backend.models.problem import ProblemCategoryModel, ProblemModel
from datetime import datetime
import json
from random import randint, random

from backend.views.admin.tools import Remove_accents


def RandomFromList(input:list, size) -> list:
    cnt = 0
    result = []
    for i in range(0, len(input), 1):
        if randint(0, 1) % 2 == 0:
            result.append(input[i])
            cnt = cnt + 1
            if cnt > 5:
                break
    return result

@csrf_exempt
def CreateRandomProblem(request):
    list_requirements = ['startwith', 'count']
    for x in list_requirements:
        if x not in request.GET:
            return JsonResponse({
                'status': 'error',
                'message': 'missing \'' + x + '\' parameter',
            })
    try:
        msg_error = 'startwith error'
        startwith = request.GET['startwith']
        msg_error = 'count error (must be integer)'
        count = int(request.GET['count'])
    except:
        return JsonResponse({
                'status': 'error',
                'message': msg_error
            })
    
    with transaction.atomic():
        categories_count = ProblemCategoryModel.objects.count()
        user_count = User.objects.count()
        list_categories = [x.id for x in ProblemCategoryModel.objects.all()]
        list_user = [x.id for x in User.objects.all()]

        admin = User.objects.get(username='admin')

        for i in range(1, count + 1, 1):
            fullname = startwith + ' - ' + str(i)
            shortname = Remove_accents(fullname.upper()).replace(' ', '_')
            problem = ProblemModel.CreateNewProblem(shortname, fullname, admin)
            problem.difficult = round(random() * 5, 2)
            if randint(0, 9) % 3 == 0:
                problem.problem_type = 1
            problem.save()
        list_update = ProblemModel.objects.order_by('-id')[:count]
        for p in list_update:
            random_categories = RandomFromList(list_categories, categories_count)
            random_user = RandomFromList(list_user, user_count)
            p.categories.set(random_categories)
            p.author.set(random_user)
            p.save()
    return HttpResponse('Created ' + str(count) + ' problem ok')

