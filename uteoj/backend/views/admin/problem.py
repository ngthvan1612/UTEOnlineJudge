import zipfile
import os.path
from io import BytesIO
from django.views.decorators.http import require_http_methods
from natsort import natsorted, ns

from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib import messages
from django.http.response import Http404, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from numpy import short

from backend.models.problem import PROBLEM_TYPE_CHOICES, PROBLEM_DIFFICULT_CHOICES, ProblemDifficultType, ProblemTestCaseModel, ProblemType, SubmissionVisibleModeType
from backend.models.problem import ProblemModel
from backend.models.problem import ProblemCategoryModel
from backend.views.admin.require import admin_member_required
from backend.filemanager.problemstorage import ProblemStorage
from backend.models.problem import SUBMISSION_VISIBLE_MODE_CHOICES

import json

from backend.models.settings import OJSettingModel

@admin_member_required
def AdminEditProblemDeatailsview(request, problem_short_name):
    problem = get_object_or_404(ProblemModel, shortname=problem_short_name)

    #edit
    if request.method == 'POST':
        shortname = request.POST.get('shortname')
        fullname = request.POST.get('fullname')
        is_public = True if 'is_public' in request.POST else False

        if len(shortname) == 0 or len(fullname) == 0:
            messages.add_message(request, messages.ERROR, 'Tên bài không được trống')
        elif not re.match("^[A-Za-z0-9_-]*$", shortname) or len(shortname) == 0:
            messages.add_message(request, messages.ERROR, 'ID của bài chỉ được chứa các kí tự a-ZA-Z0-9 và _ - và không được trống')
        elif shortname != problem_short_name and ProblemModel.objects.filter(shortname=shortname).exists():
            messages.add_message(request, messages.ERROR, 'Tên bài này đã có, vui lòng chọn tên khác [shortname]')
        else:
            problem.fullname = fullname
            problem.shortname = shortname
            problem.is_public = is_public

            if 'statement' in request.FILES:
                statement = request.FILES.get('statement')
                file_manager = ProblemStorage(problem=problem)
                file_manager.saveStatement(statement)

            problem.save()

            messages.add_message(request, messages.SUCCESS, 'Cập nhật thành công')
            return redirect('/admin/problems/edit/{}/'.format(shortname))
        return redirect('/admin/problems/edit/{}/'.format(problem_short_name))
    elif request.method == 'GET':
        problem_context = {
            'shortname': problem.shortname,
            'fullname': problem.fullname,
            'publish_date': problem.publish_date,
        }
        if problem.is_public:
            problem_context['is_public'] = True

        context = {
            'problem': problem_context,
        }
        return render(request, 'admin-template/problem/edit/details.html', context)
    else:
        return HttpResponse(status=405)

@admin_member_required
def AdminEditProblemProblemSetterview(request, problem_short_name):
    filter_problem = ProblemModel.objects.filter(shortname=problem_short_name)
    if not filter_problem.exists():
        return HttpResponse(status=404)
    problem = filter_problem[0]
    
    #edit
    if request.method == 'POST':
        if 'list_author[]' not in request.POST:
            messages.add_message(request, messages.ERROR, 'Phải có ít nhất một người ra đề')
            return HttpResponseRedirect(request.path_info)
        list_author = request.POST.getlist('list_author[]')
        if len(list_author) == 0:
            messages.add_message(request, messages.ERROR, 'Phải có ít nhất một người ra đề')
        else:
            testok = True
            for author in list_author:
                if not User.objects.filter(username=author).exists():
                    testok = False
                    messages.add_message(request, messages.ERROR, 'Không tìm thấy người dùng \'{}\''.format(author))
                    #no break, show all
            if testok == True:
                list_author_id = []
                for author in list_author:
                    for author_id in User.objects.filter(username=author):
                        list_author_id.append(author_id.id)
                problem.author.set(list_author_id)
                problem.save()
                messages.add_message(request, messages.SUCCESS, 'Cập nhật thành công')
        return HttpResponseRedirect(request.path_info)
    else:
        context = {
            'list_authors': [x.username for x in problem.author.all()]
        }
        return render(request, 'admin-template/problem/edit/problemsetter.html', context)

@csrf_exempt
@admin_member_required
def AdminEditProblemTestcasesDeleteView(request, problem_short_name, testcase_pk):
    if request.method == 'POST':
        problem = get_object_or_404(ProblemModel, shortname=problem_short_name)
        test = get_object_or_404(ProblemTestCaseModel, problem=problem, pk=testcase_pk)
        file_manager = ProblemStorage(problem)
        file_manager.deleteTestCaseFile(test.name, problem.input_filename)
        file_manager.deleteTestCaseFile(test.name, problem.output_filename)
        problem.total_points -= test.points
        problem.save()
        test.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)

@admin_member_required
def AdminViewTestcase(request, id, test_name, io):
    if not request.user.is_authenticated or io not in ['input', 'output']:
        raise Http404('File not found') # :((((, chỉ có admin mới xem được test
    if request.method == 'GET':
        problem = get_object_or_404(ProblemModel, shortname=id)
        file_name = problem.input_filename if io == 'input' else problem.output_filename
        return ProblemStorage(problem).loadTestcaseFile(test_name, file_name)
    else:
        return HttpResponse(status=405)


@require_http_methods(['POST'])
def AdminEditProblemTestcaseUploadTestcase(request, shortname):
    problem = get_object_or_404(ProblemModel, shortname=shortname)
    testcase_name = request.POST.get('test_name')
    input_testcase = request.FILES.get('test_input')
    output_testcase = request.FILES.get('test_output')
    if testcase_name is None or len(testcase_name) == 0:
        messages.add_message(request, messages.ERROR, f"Thiếu tên testcase")
    elif problem.problemtestcasemodel_set.filter(name=testcase_name).exists():
        messages.add_message(request, messages.ERROR, f"Testcase {testcase_name} đã có, vui lòng chọn tên khác")
    elif not re.match("^[A-Za-z0-9_]*$", testcase_name):
        messages.add_message(request, messages.ERROR, f"Tên testcase chỉ bao gồm các kí tự, số hoặc _")
    elif input_testcase is None:
        messages.add_message(request, messages.ERROR, f"Thiếu file input")
    elif output_testcase is None:
        messages.add_message(request, messages.ERROR, f"Thiếu file output")
    else:
        file_manager = ProblemStorage(problem)
        file_manager.saveTestcaseFile(testcase_name, problem.input_filename, input_testcase)
        file_manager.saveTestcaseFile(testcase_name, problem.output_filename, output_testcase)

        problem.problemtestcasemodel_set.create(
            time_limit=problem.time_limit,
            memory_limit=problem.memory_limit,
            points=problem.points_per_test,
            name=testcase_name
        ).save()

        problem.total_points += problem.points_per_test
        problem.save()

        messages.add_message(request, messages.SUCCESS, f"Upload thành công")
    return redirect(f"/admin/problems/edit/{problem.shortname}/testcases")

@require_http_methods(['POST'])
def AdminEditProblemTestcasesUploadZipView(request, problem_short_name):
    problem = get_object_or_404(ProblemModel, shortname=problem_short_name)
    if request.method == 'POST':
        
        # Lọc + xử lý + clean đàu vào
        if 'zip_testcases' not in request.FILES or 'filetype' not in request.POST:
            messages.add_message(request, messages.ERROR, 'Phải upload một file lên')
            return redirect(f"/admin/problems/edit/{problem.shortname}/testcases")
        zip_testcases = request.FILES.get('zip_testcases')
        filetype = request.POST.get('filetype')
        if filetype not in ['themis', 'combine']:
            return HttpResponse(status=501)
        
        
        # Kiểm tra thử xem file mở được không? (đúng format .zip hay không)
        file_manager = ProblemStorage(problem=problem)
        try:
            zipf = zipfile.ZipFile(BytesIO(zip_testcases.read()))
        except:
            messages.add_message(request, messages.ERROR, 'Không thể đọc file, định dạng file lỗi')
            return redirect(f"/admin/problems/edit/{problem.shortname}/testcases")

        # !! Ok check xong

        # Nếu format là themis
        if filetype == 'themis':
            problem_input_file_name = problem.input_filename
            problem_output_file_name = problem.output_filename
            list_testcases_folder = []

            # Kiểm tra lại xem đúng định dạng của themis hay không?
            all_path = zipf.namelist()
            all_path = natsorted(all_path, alg=ns.IGNORECASE)
            all_path_lower = [x.lower() for x in all_path]
            reverse_all_path = {x.lower():x for x in all_path}
            list_testcases_folder = [x for x in all_path if x.endswith('/') or x.endswith('\\')]
            list_input = []
            list_output = []
            list_message_error = []
            for testcase in list_testcases_folder:
                testcase_input_file_name = testcase + problem_input_file_name
                testcase_output_file_name = testcase + problem_output_file_name

                #check existed and fix name
                if testcase_input_file_name.lower() not in all_path_lower:
                    list_message_error.append('Test \'{}\' thiếu file input [{}]'.format(testcase[:-1], testcase_input_file_name))
                else:
                    testcase_input_file_name = reverse_all_path[testcase_input_file_name.lower()]
                if testcase_output_file_name.lower() not in all_path_lower:
                    list_message_error.append('Test \'{}\' thiếu file output [{}]'.format(testcase[:-1], testcase_output_file_name))
                else:
                    testcase_output_file_name = reverse_all_path[testcase_output_file_name.lower()]
                if len(list_message_error) > 5:
                    break
                list_input.append(testcase_input_file_name)
                list_output.append(testcase_output_file_name)
            if len(list_message_error) != 0:
                for message in list_message_error:
                    messages.add_message(request, messages.ERROR, message)
            else:
                # Nếu đúng
                
                # Xóa hết test cũ đi + cập nhật tổng điểm
                problem.problemtestcasemodel_set.all().delete()
                problem.total_points = round(problem.points_per_test * len(list_testcases_folder), settings.NUMBER_OF_DECIMAL)
                problem.save()

                # Optimize: Cho tất cả testcase model vào prepare_db sau đó comit vào database một lượt
                prepare_db = []

                for tmp_id in range(0, len(list_testcases_folder), 1):
                    test_name = list_testcases_folder[tmp_id].strip('/').strip('\\') # tên test
                    zip_input = list_input[tmp_id] # file input - fix
                    zip_output = list_output[tmp_id] # file output - fix

                    #update database
                    testdb = ProblemTestCaseModel(
                        problem=problem,
                        time_limit=problem.time_limit,
                        memory_limit=problem.memory_limit,
                        points=problem.points_per_test,
                        name=test_name)
                    prepare_db.append(testdb)

                    # ghi file input + output
                    file_manager.saveTestcaseFile(test_name, problem.input_filename, ContentFile(zipf.read(zip_input)))
                    file_manager.saveTestcaseFile(test_name, problem.output_filename, ContentFile(zipf.read(zip_output)))

                problem.problemtestcasemodel_set.bulk_create(prepare_db)

                messages.add_message(request, messages.SUCCESS, 'Tải lên thành công')
                
            return HttpResponseRedirect('/admin/problems/edit/{}/testcases'.format(problem.shortname))

        return HttpResponse(status=500)
    else:
        return HttpResponse(status=405) # method is not allowed

@require_http_methods(['POST'])
def AdminEditProblemTestcasesImportSetting(request, problem_short_name):
    problem = get_object_or_404(ProblemModel, shortname=problem_short_name)
    if 'importSettingFile' not in request.FILES:
        messages.add_message(request, messages.ERROR, 'Phải upload một file lên')
        return redirect(f"/admin/problems/edit/{problem_short_name}/testcases")
    importSettingFile = request.FILES.get('importSettingFile')
    
    # check file correct format (.json)
    try:
        data = importSettingFile.read().decode('utf-8')
        data = json.loads(data)
    except:
        messages.add_message(request, messages.ERROR, 'Định dạng file lỗi')
        return redirect(f"/admin/problems/edit/{problem_short_name}/testcases")
    
    list_requirements = {'name': str, 'time_limit':int, 'memory_limit': int, 'points': float}
    name_of_type = {
        str: 'chuỗi',
        int: 'số nguyên',
        float: 'số thực',
    }

    list_testcases = {}
    # check testcases
    for test in data['testcases']:
        for key in list_requirements:
            if key not in test:
                if key != 'name':
                    messages.add_message(request, messages.ERROR, f"Test {test['name']} không có trường {key}")
                    return redirect(f"/admin/problems/edit/{problem_short_name}/testcases")
                else:
                    messages.add_message(request, messages.ERROR, f"Một hoặc nhiều testcase có không có tên")
                    return redirect(f"/admin/problems/edit/{problem_short_name}/testcases")
            elif type(test[key]) != list_requirements[key]:
                messages.add_message(request, messages.ERROR, f"Trường {key} phải là một {name_of_type[list_requirements[key]]}")
                return redirect(f"/admin/problems/edit/{problem_short_name}/testcases")
        if test['name'] in list_testcases:
            messages.add_message(request, messages.ERROR, f"Có 2 (hoặc nhiều) testcase có tên {test['name']}")
            return redirect(f"/admin/problems/edit/{problem_short_name}/testcases")
        list_testcases[test['name']] = test

    # update to database
    total_points = 0.0

    for testcase in problem.problemtestcasemodel_set.all():
        if testcase.name in list_testcases:
            test_json = list_testcases[testcase.name]
            testcase.time_limit = test_json['time_limit']
            testcase.memory_limit = test_json['memory_limit']
            testcase.points = round(test_json['points'], settings.NUMBER_OF_DECIMAL)
            total_points += round(testcase.points, settings.NUMBER_OF_DECIMAL)
            testcase.save()
    
    problem.total_points = total_points
    problem.save()
    
    messages.add_message(request, messages.SUCCESS, 'Nhập cấu hình thành công')
    return redirect(f"/admin/problems/edit/{problem_short_name}/testcases")

@require_http_methods(['GET'])
def AdminEditProblemTestcasesExportSetting(request, problem_short_name):
    
    problem = get_object_or_404(ProblemModel, shortname=problem_short_name)
    res = {}
    tmp = []
    for test in problem.problemtestcasemodel_set.all():
        testcase_json = {
            'name': test.name,
            'time_limit': test.time_limit,
            'memory_limit': test.memory_limit,
            'points': test.points,
        }
        tmp.append(testcase_json)
    
    res['testcases'] = tmp
    # sinh test có testcases rỗng: chưa làm

    json_str = json.dumps(res, indent=4)
    response = HttpResponse(json_str, content_type='application/json')
    response['Content-Disposition'] = f"attachment; filename={problem.shortname}_testcases.json"

    return response

@admin_member_required
@never_cache
def AdminEditProblemTestcasesview(request, problem_short_name):
    problem = get_object_or_404(ProblemModel, shortname=problem_short_name)

    #edit
    if request.method == 'POST':
        list_time_limit = [int(x) for x in request.POST.getlist('list_time_limit[]')]
        list_memo_limit = [int(x) for x in request.POST.getlist('list_memo_limit[]')]
        list_points = [float(x) for x in request.POST.getlist('list_points[]')]
        it = 0
        total_points = 0.0
        for x in problem.problemtestcasemodel_set.all():
            x.time_limit = list_time_limit[it]
            x.memory_limit = list_memo_limit[it]
            x.points = round(list_points[it], settings.NUMBER_OF_DECIMAL)
            total_points += round(list_points[it], settings.NUMBER_OF_DECIMAL)
            x.save()
            it += 1
        problem.total_points = round(total_points, settings.NUMBER_OF_DECIMAL)
        problem.save()
        return HttpResponseRedirect(request.path_info)

    #show list testcases
    elif request.method == 'GET':
        list_testcases = [{
                'pk': x.id,
                'id': 0,
                'time_limit': x.time_limit,
                'memory_limit': x.memory_limit,
                'is_sample': x.is_sample,
                'points': x.points,
                'name': x.name,
            } for x in problem.problemtestcasemodel_set.all()]
        for id in range(0, len(list_testcases), 1):
            list_testcases[id]['id'] = id + 1
        list_allow_format = [
            {
                'value': 'themis',
                'display': 'Themis format',
            },
        ]
        context = {
            'list_testcases': list_testcases,
            'problem': problem,
            'list_formats': list_allow_format,
        }
        return render(request, 'admin-template/problem/edit/listtestcase.html', context)
    else:
        return HttpResponse(status=405)


@admin_member_required
def AdminEditProblemSettingsview(request, problem_short_name):
    problem = get_object_or_404(ProblemModel, shortname=problem_short_name)

    if request.method == 'POST':
        input_filename = request.POST.get('input_filename')
        output_filename = request.POST.get('output_filename')
        submission_visible_mode = int(request.POST.get('submission_visible_mode'))
        difficult = int(request.POST.get('difficult'))
        problem_type = int(request.POST.get('problem_type'))
        points_per_test = round(float(request.POST.get('points_per_test')), settings.NUMBER_OF_DECIMAL)
        
        try:
            time_limit = int(request.POST.get('time_limit'))
            if time_limit <= 0:
                raise 'error'
        except:
            messages.add_message(request, messages.ERROR, 'Thời gian chạy phải là số  nguyên dương')
            return HttpResponseRedirect(request.path_info)
        try:
            memory_limit = int(request.POST.get('memory_limit'))
            if memory_limit <= 0:
                raise 'error'
        except:
            messages.add_message(request, messages.ERROR, 'Giới hạn bộ nhớ phải là số nguyên dương')
            return HttpResponseRedirect(request.path_info)

        use_stdin = True if 'use_stdin' in request.POST else False
        use_stdout = True if 'use_stdout' in request.POST else False

        problem.problem_type = problem_type

        problem.submission_visible_mode = submission_visible_mode

        problem.input_filename = input_filename
        problem.output_filename = output_filename
        problem.use_stdin = use_stdin
        problem.use_stdout = use_stdout

        problem.time_limit = time_limit
        problem.memory_limit = memory_limit

        problem.difficult = difficult

        problem.points_per_test = points_per_test

        if 'list_categories[]' in request.POST:
            problem.categories.set([int(x) for x in request.POST.getlist('list_categories[]')])

        problem.save()

        messages.add_message(request, messages.SUCCESS, 'Cập nhật thành công')

        return HttpResponseRedirect(request.path_info)
    elif request.method == 'GET':

        context = {
            'list_submode': [
                {
                    'value': x[0],
                    'name': x[1],
                } for x in SUBMISSION_VISIBLE_MODE_CHOICES
            ],
            'list_problemtype': [
                {
                    'value': x[0],
                    'name': x[1]
                } for x in PROBLEM_TYPE_CHOICES
            ],
            'problem_type':problem.problem_type,
            'input_filename': problem.input_filename,
            'output_filename': problem.output_filename,
            'use_stdin': problem.use_stdin,
            'use_stdout': problem.use_stdout,
            'time_limit': problem.time_limit,
            'memory_limit': problem.memory_limit,
            'submission_visible_mode': problem.submission_visible_mode,
            'list_categories': [
                {
                    'name': x.name,
                    'value': x.id
                } for x in ProblemCategoryModel.objects.all()],
            'list_difficult': [
                {
                    'name': x[1],
                    'value': x[0]
                }
            for x in PROBLEM_DIFFICULT_CHOICES],
            'categories': [x.id for x in problem.categories.all()],
            'points_per_test': problem.points_per_test,
            'difficult': problem.difficult,
        }

        return render(request, 'admin-template/problem/edit/settings.html', context)

import os
from judger.grader import CppGrader

@admin_member_required
def AdminEditProblemCustomCheckerview(request, problem_short_name):
    problem = get_object_or_404(ProblemModel, shortname=problem_short_name)

    #edit
    if request.method == 'POST':
        list_requirements = ['checker_source']

        for x in list_requirements:
            if x not in request.POST:
                return HttpResponse(status=500)
        
        use_checker = True if 'use_checker' in request.POST else False
        checker_source = request.POST.get('checker_source')

        context = {}
        context['checker_source'] = checker_source
        context['use_checker'] = use_checker

        # biên dịch
        if use_checker:
            grader = CppGrader(None, None)
            file_manager = ProblemStorage(problem=problem)
            file_manager.saveCheckerFile(ContentFile(checker_source))
            result, msg = grader.compileChecker(os.path.join(settings.PROBLEM_ROOT, file_manager.getCheckerDir()))
            if not result:
                messages.add_message(request, messages.ERROR, 'Biên dịch gặp lỗi')
                context['compile_error'] = msg
                return render(request, 'admin-template/problem/edit/checker.html', context)
            
        problem.use_checker = use_checker
        problem.checker = checker_source
        problem.save()

        messages.add_message(request, messages.SUCCESS, 'Cập nhật thành công')

        return render(request, 'admin-template/problem/edit/checker.html', context)

    elif request.method == 'GET':
        context = {
            'use_checker': problem.use_checker,
            'checker_source': problem.checker,
        }
        return render(request, 'admin-template/problem/edit/checker.html', context)
    else:
        return HttpResponse(status=405)

from time import time

@admin_member_required
def AdminListProblemView(request):
    with transaction.atomic():
        problem_models_filter = ProblemModel.objects.order_by('-id')
        tmp = time()
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
            if 'name' in request.GET:
                problemnamelike = request.GET['name']
                problem_models_filter = problem_models_filter.filter(Q(shortname__icontains=problemnamelike) | Q(fullname__icontains=problemnamelike))
            if 'orderby' in request.GET:
                orderby_query = request.GET['orderby']
                if orderby_query == 'difficult' or orderby_query == '-difficult':
                    problem_models_filter = problem_models_filter.order_by(orderby_query)
                elif orderby_query == 'solvedCount' or orderby_query == '-solvedCount':
                    neg = '-' if '-' in orderby_query else ''
                    orderby_query = orderby_query if '-' not in orderby_query else orderby_query[1:]
                    problem_models_filter = problem_models_filter.order_by(neg + 'problemstatisticsmodel__' + orderby_query)
            if 'difficult' in request.GET:
                tmp = request.GET['difficult'].split(',')
                if len(tmp) == 2:
                    a, b = tmp
                    try:
                        a = round(float(a), 2) if len(a) else 0
                        b = round(float(b), 2) if len(b) else 1000
                        problem_models_filter = problem_models_filter.filter(difficult__gte=a, difficult__lte=b)
                    except:
                        pass
        problem_models_filter = problem_models_filter.all()
        pre = 0
        for x in problem_models_filter:
            x.index = pre + 1
            pre = pre + 1

        paginator = Paginator(problem_models_filter, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'website_header_title': 'Danh sách bài tập',
            'list_categories': ['All'] + [x.name for x in ProblemCategoryModel.objects.all()],
            'page_obj': page_obj,
        }

    return render(request, 'admin-template/problem/listproblem.html', context)

import re

def AdminCreateProblemView(request):
    if request.method == 'POST':
        list_requirements = ['shortname', 'fullname']
        for x in list_requirements:
            if x not in request.POST:
                return HttpResponse(status=500)

        shortname = str(request.POST['shortname'])
        fullname = str(request.POST['fullname'])
        if not re.match("^[A-Za-z0-9_-]*$", shortname) or len(shortname) == 0:
            messages.add_message(request, messages.ERROR, 'ID của bài chỉ được chứa các kí tự a-ZA-Z0-9 và _ và không được trống')
        elif ProblemModel.objects.filter(shortname=shortname).exists():
            messages.add_message(request, messages.ERROR, 'Bài {} đã tồn tại'.format(shortname))
        elif len(fullname) == 0:
            messages.add_message(request, messages.ERROR, 'Tên đầy đủ của bài không được trống')
        else:
            problem = ProblemModel.CreateNewProblem(shortname, fullname, request.user, OJSettingModel.getDefaultProblemConfig())
            problem.save()
            messages.add_message(request, messages.SUCCESS, 'Tạo thành công')
            return redirect('/admin/problems/edit/{}'.format(shortname))
        return HttpResponseRedirect(request.path_info)
    elif request.method == 'GET':

        return render(request, 'admin-template/problem/createproblem.html')
    else:
        return HttpResponse(status=405)

def AdminExportProblemConfig(request, shortname):
    
    problem = get_object_or_404(ProblemModel, shortname=shortname)

    res = {}
    res['input_filename'] = problem.input_filename
    res['output_filename'] = problem.output_filename
    res['problem_type'] = 'ACM' if problem.problem_type == ProblemType.ACM else 'OI'
    res['time_limit'] = problem.time_limit
    res['memory_limit'] = problem.memory_limit
    res['submission_visible_mode'] = SubmissionVisibleModeType.getModeName(problem.submission_visible_mode)
    res['difficult'] = ProblemDifficultType.getModeName(problem.difficult)
    res['points_per_test'] = problem.points_per_test

    json_str = json.dumps(res, indent=4)
    response = HttpResponse(json_str, content_type='application/json')
    response['Content-Disposition'] = f"attachment; filename={problem.shortname}_config.json"

    return response

def AdminImportProblemConfig(request, shortname):
    problem = get_object_or_404(ProblemModel, shortname=shortname)

    if request.method == 'POST':
        config = request.FILES.get('config')
        if not config:
            messages.add_message(request, messages.ERROR, 'Bạn phải chọn một file')
            return HttpResponseRedirect(request.path_info)
        
        # check file correct format (.json)
        try:
            data = config.read().decode('utf-8')
            data = json.loads(data)
        except:
            messages.add_message(request, messages.ERROR, 'Định dạng file lỗi')
            return HttpResponseRedirect(request.path_info)
        
        # check file correct format (web) [name & datatype]
        list_requirements = {'input_filename' : str, 'output_filename': str, 'problem_type': str, 'time_limit': int, 'memory_limit': int,
            'submission_visible_mode': str, 'difficult': str, 'points_per_test':float,}
        name_of_type = {str: 'chuỗi', int: 'số nguyên', list: 'danh sách', float: 'số thực'}
        accept_values = {
            'problem_type': ['ACM', 'OI'],
            'submission_visible_mode': SubmissionVisibleModeType.getAcceptValue(),
            'difficult': ProblemDifficultType.getAcceptValue(),
        }
        for key in list_requirements:
            if key not in data:
                messages.add_message(request, messages.ERROR, f"Thiếu tường: {key}")
                return HttpResponseRedirect(request.path_info)
            elif type(data[key]) != list_requirements[key]:
                messages.add_message(request, messages.ERROR, f"Trường {key} phải là một {name_of_type[list_requirements[key]]}")
                return HttpResponseRedirect(request.path_info)
            elif key in accept_values:
                if data[key] not in accept_values[key]:
                    messages.add_message(request, messages.ERROR, f"Không rõ giá trị \"{data[key]}\" của trường {key}")
                    return HttpResponseRedirect(request.path_info)
        # update to database

        problem.input_filename = data['input_filename']
        problem.output_filename = data['output_filename']
        problem.problem_type = ProblemType.ACM if data['problem_type'] == 'ACM' else ProblemType.OI
        problem.time_limit = data['time_limit']
        problem.memory_limit = data['memory_limit']
        problem.submission_visible_mode = SubmissionVisibleModeType.getValueFromName(data['submission_visible_mode'])
        problem.difficult = ProblemDifficultType.getValueFromName(data['difficult'])
        problem.points_per_test = round(data['points_per_test'], settings.NUMBER_OF_DECIMAL)
        problem.save()
        
        messages.add_message(request, messages.SUCCESS, 'Nhập cấu hình thành công')
    return redirect(f"/admin/problems/edit/{shortname}/settings")

