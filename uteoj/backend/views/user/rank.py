from typing import final

from backend.models.usersetting import UserProblemStatisticsModel
from django.core.paginator import Paginator
from django.http.response import HttpResponseNotAllowed, HttpResponseRedirect
from backend.models.language import LanguageModel
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from backend.models.problem import ProblemModel
from backend.models.problem import ProblemCategoryModel
from backend.models.submission import SubmissionModel, SubmissionResultType, SubmissionStatusType
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from copy import copy

from datetime import datetime
from random import random
from django.http import HttpResponse
from django.core import serializers
from django.db.models import F, Sum, Count


def UserRankView(request):

    final_filter = UserProblemStatisticsModel.objects.values(username=F('user__username')).annotate(total_solvedCount=Count('solvedCount')).order_by('-total_solvedCount')

    id = 0
    pre = -1
    for x in final_filter:
        if pre != x['total_solvedCount']:
            id = id + 1
            pre = x['total_solvedCount']
        x['rank'] = id
    
    paginator = Paginator(final_filter, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj
    }

    return render(request, 'user-template/rank.html', context)
