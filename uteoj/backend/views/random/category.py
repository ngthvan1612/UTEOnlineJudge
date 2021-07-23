from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from backend.models.problem import ProblemCategoryModel, ProblemModel
from datetime import datetime
import json
from random import random

@csrf_exempt
def CreateRandomCate(request):
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
    
    response = []
    with transaction.atomic():
        for i in range(1, count + 1, 1):
            ProblemCategoryModel.objects.create(name=startwith + ' - ' + str(i), description='bla bla gi do').save()
    return HttpResponse('Created ' + str(count) + ' problem ok')

