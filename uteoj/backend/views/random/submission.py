from backend.models.language import LanguageModel
from backend.models.submission import SubmissionModel, SubmissionStatusType
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

from django.utils import timezone

@csrf_exempt
def CreateRandomSubmission(request):
    list_requirements = ['count']
    for x in list_requirements:
        if x not in request.GET:
            return JsonResponse({
                'status': 'error',
                'message': 'missing \'' + x + '\' parameter',
            })
    try:
        count = int(request.GET['count'])
    except:
        return HttpResponse('count phải là số')
    return HttpResponse('Đang chạy nền...')
