from django.contrib import messages
from backend.models.usersetting import UserProblemStatisticsModel
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from backend.models.problem import ProblemModel, SubmissionVisibleModeType
from backend.models.problem import ProblemCategoryModel
from django.db.models import Q

from datetime import datetime
from random import random
from django.http import HttpResponse
from django.core import serializers


from backend.task.submit import SubmitSolutionTest
from backend.models.submission import SubmissionModel, SubmissionTestcaseResultModel
from django.core.paginator import Paginator

def UserListSubmissionView(request):
    if request.method == 'GET':
        final_filter = SubmissionModel.objects.order_by('-id')
        if 'my' in request.GET and request.user.is_authenticated:
            my = request.GET['my']
            if my == 'on':
                final_filter = final_filter.filter(user=request.user)

        paginator = Paginator(final_filter, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
        }

        return render(request, 'user-template/submissions/listsubmission.html', context)
    else:
        return HttpResponse(status=405)


def UserSubmissionView(request, submission_id):
    if request.method == 'GET':
        submission = SubmissionModel.objects.filter(id=submission_id)
        if not submission.exists():
            return HttpResponse(status=404)

        allow = False

        #check visible
        submission = submission[0]
        vs_mode = submission.problem.problemsettingmodel.submission_visible_mode
        if vs_mode == SubmissionVisibleModeType.AllowedFromAll:
            allow = True
        elif vs_mode == SubmissionVisibleModeType.OnlySolved:
            # check solved
            if not request.user.is_authenticated:
                allow = False
            else:
                userproblemstatistics = UserProblemStatisticsModel.objects.filter(user=request.user, problem=submission.problem)
                if userproblemstatistics.exists():
                    if userproblemstatistics[0].solvedCount > 0:
                        allow = True
        elif vs_mode == SubmissionVisibleModeType.OnlyMe:
            if request.user.id == submission.user.id:
                allow = True


        context = {}

        if allow:
            context['submission'] = submission
            context['list_testcases'] = SubmissionTestcaseResultModel.objects.filter(submission=submission).all()
        else:
            messages.add_message(request, messages.ERROR, 'Bạn không có quyền xem source code này')

        return render(request, 'user-template/submissions/submissiondetail.html', context)
    return HttpResponse(status=405)
    