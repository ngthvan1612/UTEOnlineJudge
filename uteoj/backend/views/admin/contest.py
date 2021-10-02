from io import BytesIO
from random import randint
import re

from django.db.models.aggregates import Max, Sum
from backend.views.admin.tools import Remove_accents
from backend.filemanager.problemstorage import ProblemStorage
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.views.decorators.csrf import csrf_exempt
from numpy import less, short
from backend.models.problem import ProblemModel, ProblemTestCaseModel, ProblemType
from django.contrib import messages
from django.db.models.fields import DateTimeField
from django.http.request import HttpRequest
from django.http.response import FileResponse, Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators import http
from backend.views.auth.login import LoginView
from backend.views.admin.require import admin_member_required
from backend.models.contest import ContestModel
from backend.models.submission import SubmissionModel
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
from django.http import JsonResponse
from backend.filemanager.importuser import ImportUserStorage
from backend.models.usersetting import ImportUserFileModel
from django.db.models.functions import Length
from django.utils import timezone
from django.db.models import F
import uuid

import pandas as pd
import numpy as np


@admin_member_required # xíu xóa
@require_http_methods(['GET', 'POST'])
def AdminCreateContestView(request):
    if request.method == 'POST':
        title = request.POST.get('title') # không được rỗng
        desc = request.POST.get('desc') # được rỗng
        startTime = request.POST.get('startTime')
        endTime = request.POST.get('endTime')

        result, title, startTime, endTime, msg = ContestModel.prepareData(title, startTime, endTime)
        if not result:
            messages.add_message(request, messages.ERROR, msg)
            return render(request, 'admin-template/contest/createcontest.html')

        result, msg, contest = ContestModel.createContest(title, desc, startTime, endTime)
        if not result:
            messages.add_message(request, messages.ERROR, msg)
            return render(request, 'admin-template/contest/createcontest.html')
        else:
            messages.add_message(request, messages.SUCCESS, msg)
            return redirect(f"/admin/contests/edit/{contest.id}")

    else: # GET
        return render(request, 'admin-template/contest/createcontest.html')


@require_http_methods(['GET'])
@admin_member_required
def AdminListContestView(request):
    context = {
        'list_contests': ContestModel.objects.all()[::-1]
    }

    return render(request, 'admin-template/contest/listcontest.html', context)

@require_http_methods(['GET', 'POST'])
def AdminEditContestView(request, id):
    contest = get_object_or_404(ContestModel, pk=id)

    if request.method == 'POST':
        title = request.POST.get('title') # không được rỗng
        desc = request.POST.get('desc') # được rỗng
        startTime = request.POST.get('startTime')
        endTime = request.POST.get('endTime')

        result, title, startTime, endTime, msg = ContestModel.prepareData(title, startTime, endTime)

        if not result:
            messages.add_message(request, messages.ERROR, msg)
            context = {
                'title': contest.title,
                'desc': contest.description,
                'startTime': contest.startTime,
                'endTime': contest.endTime,
            }
            return render(request, 'admin-template/contest/edit/details.html', context)

        contest.title = title
        contest.description = desc
        contest.startTime = startTime
        contest.endTime = endTime
        contest.save()

        messages.add_message(request, messages.SUCCESS, 'Lưu thành công')
        return HttpResponseRedirect(request.path_info)
    else: #GET
        context = {
            'title': contest.title,
            'desc': contest.description,
            'startTime': contest.startTime,
            'endTime': contest.endTime,
        }

        return render(request, 'admin-template/contest/edit/details.html', context)

@require_http_methods(['GET', 'POST'])
def AdminEditContestProblemsView(request, id):
    contest = get_object_or_404(ContestModel, pk=id)
    
    if request.method == 'POST':
        shortname = request.POST.get('shortname')
        new_shortname = request.POST.get('new_shortname')
        copy = True if 'copy' in request.POST else False

        problem = ProblemModel.objects.filter(shortname=shortname)
        if not problem.exists():
            messages.add_message(request, messages.ERROR, f"Không có bài tập này: {str(shortname)}")
            return HttpResponseRedirect(request.path_info)
        problem = problem[0]

        if not copy:
            problem.contest = contest
            problem.save()
            return HttpResponseRedirect(request.path_info)

        if not re.match("^[A-Za-z0-9_-]*$", new_shortname) or len(new_shortname) == 0:
            messages.add_message(request, messages.ERROR, 'ID của bài chỉ được chứa các kí tự a-ZA-Z0-9 và _ và không được trống')
            return HttpResponseRedirect(request.path_info)
        
        if ProblemModel.objects.filter(shortname=new_shortname).exists():
            messages.add_message(request, messages.ERROR, f"Bài tập với ID {new_shortname} đã có, vui lòng chọn tên khác")
            return HttpResponseRedirect(request.path_info)

        new_problem = ProblemModel.CreateNewProblem(new_shortname, problem.fullname, problem.author)
        
        # check xong
        
        source = ProblemStorage(problem)
        dest = ProblemStorage(new_problem)

        # clone all file
        ProblemStorage.copyProblem(problem, new_problem)
        
        # clone settingss
        new_problem.categories.set(problem.categories.all())
        new_problem.is_public = False
        new_problem.problem_type = problem.problem_type
        new_problem.difficult = problem.difficult
        new_problem.points_per_test = problem.points_per_test
        new_problem.total_points = problem.total_points
        new_problem.submission_visible_mode = problem.submission_visible_mode
        new_problem.input_filename = problem.input_filename
        new_problem.output_filename = problem.output_filename
        new_problem.use_stdin = problem.use_stdin
        new_problem.use_stdout = problem.use_stdout
        new_problem.time_limit = problem.time_limit
        new_problem.memory_limit = problem.memory_limit
        new_problem.use_checker = problem.use_checker
        new_problem.checker = problem.checker
        new_problem.save()

        # clone testcases model
        testcasemodel = problem.problemtestcasemodel_set.all()
        prepare_db = []
        for x in testcasemodel:
            testcase = ProblemTestCaseModel(
                problem=new_problem,
                tag=x.tag,
                time_limit=x.time_limit,
                memory_limit=x.memory_limit,
                points=x.points,
                name=x.name,
            )
            prepare_db.append(testcase)
        new_problem.problemtestcasemodel_set.all().delete()
        new_problem.problemtestcasemodel_set.bulk_create(prepare_db)

        # clone checker -> ok

        # thêm vô kì thi hiện tại
        contest.problemmodel_set.add(new_problem)

        return HttpResponseRedirect(request.path_info)
    else: #GET
        context = {
            'list_problems': contest.problemmodel_set.all(),
            'contest': contest,
        }

        return render(request, 'admin-template/contest/edit/problems.html', context)

@csrf_exempt
@require_http_methods(['POST'])
def AdminEditContestRemoveProblems(request, id, shortname):
    contest = get_object_or_404(ContestModel, pk=id)
    problem = get_object_or_404(ProblemModel, shortname=shortname)
    reuslt, msg = contest.removeProblem(problem)
    return HttpResponse('')

@require_http_methods(['GET'])
def AdminContestFilterProblem(request, id):
    contest = get_object_or_404(ContestModel, pk=id)
    name = request.GET.get('name')
    if not name:
        name = ''

    tmp = ProblemModel.objects.values('shortname', 'fullname').filter(
        (Q(shortname__icontains=name) | Q(fullname__icontains=name)) & 
        (Q(contest__isnull=True) & (~Q(contest=contest))))[:10]
    response = {}
    for x in tmp:
        response[x['shortname']] = x['fullname']

    return JsonResponse(response, json_dumps_params={'ensure_ascii': False, 'indent': 4})


@require_http_methods(['GET', 'POST'])
def AdminEditContestCreateProblem(request, id):
    contest = get_object_or_404(ContestModel, pk=id)
    if request.method == 'POST':
        shortname = str(request.POST['shortname'])
        fullname = str(request.POST['fullname'])

        if not re.match("^[A-Za-z0-9_-]*$", shortname) or len(shortname) == 0:
            messages.add_message(request, messages.ERROR, 'ID của bài chỉ được chứa các kí tự a-ZA-Z0-9 và _ và không được trống')
        elif ProblemModel.objects.filter(shortname=shortname).exists():
            messages.add_message(request, messages.ERROR, 'Bài {} đã tồn tại'.format(shortname))
        elif len(fullname) == 0:
            messages.add_message(request, messages.ERROR, 'Tên đầy đủ của bài không được trống')
        else:
            problem = ProblemModel.CreateNewProblem(shortname, fullname, request.user)
            problem.contest = contest
            problem.save()
            messages.add_message(request, messages.SUCCESS, 'Tạo thành công')
            return redirect('/admin/problems/edit/{}'.format(shortname))
        
        return HttpResponseRedirect(request.path_info)
    elif request.method == 'GET':

        return render(request, 'admin-template/problem/createproblem.html')
    else:
        return HttpResponse(status=405)

@require_http_methods(['GET', 'POST'])
def AdminEditContestImportUser(request, id):
    contest = get_object_or_404(ContestModel, pk=id)

    if request.method == 'POST':
        files = request.FILES.getlist('listUsersFile[]')
        options = int(request.POST.get('mdImport'))
        if not files or len(files) == 0:
            messages.add_message(request, messages.ERROR, 'Bạn phải upload ít nhất một file')
            return HttpResponseRedirect(request.path_info)
        
        tmp = {}
        lsSinhVien = []
        for xls in files:
            try:
                df = pd.read_excel(BytesIO(xls.read()))
            except Exception as e:
                print(e)
                messages.add_message(request, messages.ERROR, f"Không đọc được file {xls.name}")
                return HttpResponseRedirect(request.path_info)
            
            data = df.to_numpy()

            for x in data:
                mssv, ho, ten, ns = str(x[1]), str(x[3]), str(x[4]), str(x[5])
                if mssv.isdigit() and ho != 'nan' and ten != 'nan':
                    if mssv not in tmp:
                        ns = pd.to_datetime(ns)
                        password = mssv + '_' + Remove_accents(ten).lower()
                        username = mssv
                        lsSinhVien.append((mssv, ho.strip(), ten.strip(), username, password))
                        tmp[mssv] = 1
        
        list_users = []
        if options == 0:
            contest.contestants.clear()
        for mssv, ho, ten, username, password in lsSinhVien:
            users = User.objects.filter(username=mssv)
            if users.exists():
                if options == 1 or options == 0:
                    for user in users:
                        user.set_password(password)
                        user.save()
                        list_users.append(user)
            else:
                user = User.objects.create_user(username=username, first_name=ten, last_name=ho, password=password, email=username+'@student.hcmute.edu.vn')
                user.save()
                list_users.append(user)

        contest.contestants.add(*list_users)

        messages.add_message(request, messages.SUCCESS, f"Nhập xong {len(lsSinhVien)} thí sinh")
        return HttpResponseRedirect(request.path_info)

    else: # GET
        options = [
            {
                'name': 'Thay thế hoàn bằng danh sách mới',
                'value': 0
            },
            {
                'name': 'Ghi đè dữ liệu mới vào (nếu thí sinh không có trong danh sách mới thì giữa nguyên)',
                'value': 1
            },
            {
                'name': 'Không thay thế / ghi đè, nếu thí sinh không có trong danh sách thì thêm vào',
                'value': 2
            }
        ]
        return render(request, 'admin-template/contest/edit/import.html', {
            'options': options,
        })


@require_http_methods(['GET'])
def AdminEditContestExportView(request, id):

    return render(request, 'admin-template/contest/edit/export.html')

def compareFuncUser(u):
    hoten = (u[1] + ' ' + u[2]).split()[::-1]
    result = []
    for x in hoten:
        result.append(Remove_accents(x).lower())
        result.append(x.lower())
    return result

@require_http_methods(['GET'])
def AdminEditContestExportContestantView(request, id):
    contest = get_object_or_404(ContestModel, pk=id)

    lsSinhVien = []
    for sv in contest.contestants.all():
        lsSinhVien.append((sv.username, sv.last_name, sv.first_name, sv.username, sv.username + '_' + Remove_accents(sv.first_name).lower()))
    lsSinhVien.sort(key=compareFuncUser)

    lsOutput = np.array(lsSinhVien)
    stream = BytesIO()

    pdOutput = pd.DataFrame(lsOutput, columns=('Mã số SV', 'Họ và tên lót', 'Tên', 'Tên đăng nhập', 'Mật khẩu'))
    pdOutput.index += 1
    pdOutput.to_excel(stream, engine='xlwt')
    stream.seek(0)

    fileResponse = FileResponse(stream)    
    fileResponse['Content-Disposition'] = f"attachment; filename=UTEOJ_DANH_SACH_THI_SINH_{timezone.localtime(timezone.now()).strftime('%d-%m-%Y_%H-%M-%S')}.xls"

    return fileResponse

@require_http_methods(['GET'])
def AdminEditContestExportResultView(request, id):
    contest = get_object_or_404(ContestModel, pk=id)

    headers = ['Mã số SV', 'Họ và tên lót', 'Tên']
    lsMSSV = {x.username for x in contest.contestants.all()}
    lsSinhVien = []
    for sv in contest.contestants.all():
        lsSinhVien.append((sv.username, sv.last_name, sv.first_name))
    lsSinhVien.sort(key=compareFuncUser)

    df = pd.DataFrame(lsSinhVien, columns=headers)
    
    for problem in contest.problemmodel_set.all():
        list_submission = SubmissionModel.objects.filter(problem=problem, submission_date__range=[contest.startTime, contest.endTime]).all()
        result = {}
        if problem.problem_type == ProblemType.OI:
            # get max
            for sub in list_submission:
                if sub.user.username not in result:
                    result[sub.user.username] = sub.points
                else:
                    result[sub.user.username] = max(result[sub.user.username], sub.points)
            pass
        else: #ACM
            # chua lam
            pass
        
        col = []
        for sv in lsSinhVien:
            if sv[0] in result:
                col.append(result[sv[0]])
            else:
                col.append('Không có bài')
            
        df[problem.shortname] = col

    stream = BytesIO()
    
    df.index += 1
    df.to_excel(stream, engine='xlwt')
    stream.seek(0)

    fileResponse = FileResponse(stream)    
    fileResponse['Content-Disposition'] = f"attachment; filename=TEST_{timezone.localtime(timezone.now()).strftime('%d-%m-%Y_%H-%M-%S')}.xls"

    return fileResponse


