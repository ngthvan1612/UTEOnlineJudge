from typing import final
from backend.models.settings import OJSettingModel
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

from random import random
from django.http import HttpResponse

from backend.task.submit import SubmitSolution
from backend.filemanager.problemstorage import ProblemStorage

def ProblemStatementViewer(request, id):
    file_manager = ProblemStorage(problem=get_object_or_404(ProblemModel, shortname=id))
    return file_manager.loadStatement()

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

    if 'difficult' in request.GET:
        tmp = request.GET['difficult'].split(',')
        if len(tmp) == 2:
            a, b = tmp
            try:
                a = round(float(a), 2) if len(a) else 0
                b = round(float(b), 2) if len(b) else 1000
                final_filter = final_filter.filter(difficult__gte=a, difficult__lte=b)
            except:
                pass

    paginator = Paginator(final_filter, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    rows = []
    tmp = []
    cnt = 0
    for x in page_obj:
        if cnt % 5 == 0:
            if len(tmp) != 0:
                rows.append(tmp)
            tmp = []
        tmp.append(x)
        cnt = cnt + 1
    if len(tmp) != 0:
        rows.append(tmp)

    context = {
        'page_obj': page_obj,
        'rows': rows,
        'list_categories': ProblemCategoryModel.objects.all(),
    }

    return render(request, 'user-template/problem/listproblem.html', context)


def UserProblemView(request, shortname):
    problems = ProblemModel.objects.filter(shortname=shortname)

    if problems.exists() == False:
        return HttpResponse(status=404)

    list_submission = SubmissionModel.objects.filter(problem=problems[0],user=request.user).all()

    context = {
        'problem': problems[0],
        'list_submission': list_submission,
    }

    return render(request, 'user-template/problem/problemdetail.html', context)

from django.utils import timezone

@csrf_exempt
def UserSubmitSolution(request, shortname):
    problem = get_object_or_404(ProblemModel, shortname=shortname)
    if not request.user.is_authenticated:
        messages.add_message(request, messages.ERROR, 'Vui lòng đăng nhập để nộp bài')
        return redirect('/login')
    if not request.user.is_authenticated:
        return redirect('/login')

    if problem.problemtestcasemodel_set.count() == 0:
        messages.add_message(request, messages.ERROR, 'Không thể chấm bài này, hiện tại không có testcase nào!')
        return redirect('/problems')
    
    if request.method == 'POST':
        if 'language' not in request.POST:
            return HttpResponse(status=500)
        if 'source' not in request.POST:
            return HttpResponse(status=500)
        if not OJSettingModel.getAllowSubmission():
            return HttpResponseRedirect(request.path_info)
        language_filter = LanguageModel.objects.filter(name=request.POST['language'])
        if not language_filter.exists():
            return HttpResponse('Không có ngôn ngữ nào tên \'{}\''.format(request.POST['language']))
        language=LanguageModel.objects.get(name=request.POST['language'])
        source_code = request.POST['source']

        final_source = source_code

        if 'source_file' in request.FILES:
            source_file = request.FILES['source_file'].read()
            try:
                final_source = source_file.decode('utf-8')
            except:
                messages.add_message(request, messages.ERROR, 'Không thể đọc mã nguồn, có thể bạn đã nộp một file thực thi.')
                return HttpResponseRedirect(request.path_info)

        if len(final_source) == 0:
            messages.add_message(request, messages.ERROR, 'Mã nguồn không được để trống')
            return HttpResponseRedirect(request.path_info)
        submission = SubmissionModel.objects.create(
            user=request.user,
            problem=problem,
            submission_date=timezone.localtime(timezone.now()),
            source_code = final_source,
            language=language)
        submission.status = SubmissionStatusType.InQueued
        submission.save()

        SubmitSolution.apply_async(
            args=[submission.id],
            queue='uteoj_judger')
        return redirect('/submissions')
    elif request.method == 'GET':
        if not OJSettingModel.getAllowSubmission():
            messages.add_message(request, messages.ERROR, 'Hiện tại không thể nộp bài')
        context = {
            'languages': [x.name for x in LanguageModel.objects.all()],
            'problem': problem
        }
        return render(request, 'user-template/problem/submit.html', context)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def UserSubmitSolutionTest(request, shortname):
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
        
        SubmitSolutionTest(submission.id)
        return HttpResponse('<h2>Submit ok: id = {}</br>Bài tập: <font style="color:red;">{}</font> ({})</br>Người dùng: {}</br>Ngôn ngữ: {}</h2><br/>Có thể F5 để submit lại'
            .format(submission.id, problem.shortname, problem.fullname, request.user.username, language.name))
    elif request.method == 'GET':
        content = '<h1>Trang này test submit (backend tạo)</h1><br/>'
        context = {
            'languages': [
                {'value': x.name, 'display': x.name }
                for x in LanguageModel.objects.all()
            ]
        }
        list_language = ''
        for x in LanguageModel.objects.all():
            list_language += '<option value="{}">{}</option>\n'.format(x.name, x.name)
        list_language = 'Ngôn ngữ: <select name="language">{}</select><br/>'.format(list_language)
        source_code = 'Source code: <textarea name="source"></textarea><br/>'
        submit_button = '<input type="submit" value="Nộp bài">'
        content += '<form action="" method="post">{}</form>'.format(list_language + source_code + submit_button)
        return HttpResponse(content=content)
    else:
        return HttpResponse(status=405)
