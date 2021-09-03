from typing import final
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

from datetime import datetime
from random import random
from django.http import HttpResponse
from django.core import serializers

from backend.task.submit import SubmitSolution


def UserListProblemView(request):

    final_filter = ProblemModel.objects.all().order_by('-id')

    if 'category' in request.GET:
        category = str(request.GET['category'])
        list_categories_filter = category.split(",")
        if 'All' not in list_categories_filter:
            for x in list_categories_filter:
                final_filter = final_filter.filter(categories__in=[
                    y.id for y in ProblemCategoryModel.objects.filter(name=x).all()
                ]).distinct()
    
    if 'problem_type' in request.GET:
        problem_type = request.GET['problem_type'].lower()
        if problem_type == 'acm':
            final_filter = final_filter.filter(problem_type=0)
        if problem_type == 'oi':
            final_filter = final_filter.filter(problem_type=1)
    
    if 'name' in request.GET:
        problemnamelike = request.GET['name']
        final_filter = final_filter.filter(Q(shortname__icontains=problemnamelike) | Q(fullname__icontains=problemnamelike))

    if 'orderby' in request.GET:
        orderby = str(request.GET['orderby'])
        if orderby == 'difficult' or orderby == '-difficult':
            final_filter = final_filter.order_by(orderby)
        if orderby == 'solvedCount' or orderby == '-solvedCount':
            neg = '-' if orderby[0] == '-' else ''
            orderby = orderby if orderby[0] != '-' else orderby[1:]
            final_filter = final_filter.order_by(neg + 'problemstatisticsmodel__' + orderby)

    paginator = Paginator(final_filter, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'list_categories': [x.name for x in ProblemCategoryModel.objects.all()],
    }

    return render(request, 'user-template/problem/listproblem.html', context)


def UserProblemView(request, shortname):
    problems = ProblemModel.objects.filter(shortname=shortname)

    if problems.exists() == False:
        return HttpResponse(status=404)
    problem = problems[0]
    problem_setting = problem.problemsettingmodel

    context = {
        'fullname': problem.fullname,
        'statement': problem_setting.statement,
        'input_statement': problem_setting.input_statement,
        'output_statement': problem_setting.output_statement,
        'constraints_statement': problem_setting.constraints_statement
    }

    return render(request, 'user-template/problem/problemdetail.html', context)


def UserListSubmission(request):
    template = """
            <html>
                <head>
                    <script type = "text/JavaScript">
                            function AutoRefresh(t) {
                                setTimeout("location.reload(true);", t);
                            }
                    </script>
                </head>
                <body onload = "JavaScript:AutoRefresh(2000);" style="font-size:17px;font-family:Arial;">
                    <ul>
        """
    end_tem = """
                    </ul>
                </body>
            </html>
    """
    list_submission = ""
    for x in SubmissionModel.objects.order_by('-id').all()[:30]:
        color = "black"
        if x.status == SubmissionStatusType.Completed:
            color="red"
            if x.result == SubmissionResultType.AC:
                color = "green"
        list_submission += '<li style="color:{};">{}</li>\n'.format(color,str(x))
    return HttpResponse(template + list_submission + end_tem)

from django.utils import timezone

@csrf_exempt
def UserSubmitSolution(request, shortname):
    problem = get_object_or_404(ProblemModel, shortname=shortname)
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Vui lòng đăng nhập để nộp bài')
        return redirect('/login')
    if not request.user.is_authenticated:
        return redirect('/login')
    
    if request.method == 'POST':
        if 'language' not in request.POST:
            return HttpResponse('Thiếu ngôn ngữ')
        if 'source' not in request.POST:
            return HttpResponse('Thiếu source code')
        language_filter = LanguageModel.objects.filter(name=request.POST['language'])
        if not language_filter.exists():
            return HttpResponse('Không có ngôn ngữ nào tên \'{}\''.format(request.POST['language']))
        language=LanguageModel.objects.get(name=request.POST['language'])
        source_code = request.POST['source']

        if len(source_code) == 0:
            messages.add_message(request, messages.ERROR, 'Mã nguồn không được để trống')
            return HttpResponseRedirect(request.path_info)

        submission = SubmissionModel.objects.create(
            user=request.user,
            problem=problem,
            submission_date=timezone.localtime(timezone.now()),
            source_code = source_code,
            language=language)
        submission.status = SubmissionStatusType.InQueued
        submission.save()
        
        SubmitSolution.delay(submission.id)
        #return redirect('/status')
        return HttpResponse('<h2>Submit ok: id = {}</br>Bài tập: <font style="color:red;">{}</font> ({})</br>Người dùng: {}</br>Ngôn ngữ: {}</h2>'
            .format(submission.id, problem.shortname, problem.fullname, request.user.username, language.name))
    elif request.method == 'GET':
        
        context = {
            'languages': [
                {'value': x.name, 'display': x.name }
                for x in LanguageModel.objects.all()
            ]
        }
        return render(request, 'user-template/problem/submit.html', context)
    else:
        return HttpResponse(status=405)


def UserStatusView(request):
    if request.method == 'GET':

        final_filter = SubmissionModel.objects.order_by('-id').all()

        paginator = Paginator(final_filter, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
        }

        return render(request, 'user-template/status.html', context)
    else:
        return HttpResponse(status=405)

