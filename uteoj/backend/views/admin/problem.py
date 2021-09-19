from backend.models.problem import PROBLEM_TYPE_CHOICES, ProblemTestCaseModel
import uuid
import zipfile
import os.path
from os import mkdir
import shutil
from django.core import serializers

from django.views.decorators.cache import never_cache
from django.conf import settings
from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseRedirectBase
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import transaction
from django.core.paginator import Paginator

from backend.models.problem import ProblemModel
from backend.models.problem import ProblemSettingModel
from backend.models.problem import ProblemGraderModel
from backend.models.problem import ProblemStatisticsModel
from backend.models.problem import ProblemCategoryModel
from backend.views.admin.require import admin_member_required

from backend.models.problem import SUBMISSION_VISIBLE_MODE_CHOICES

from django import template
register = template.Library()

@register.filter
def totalPoints(arg):
    return sum(testcase.points for testcase in arg.problemtestcasemodel.all())

@admin_member_required
def AdminEditProblemDeatailsview(request, problem_short_name):
    filter_problem = ProblemModel.objects.filter(shortname=problem_short_name)
    if not filter_problem.exists():
        return HttpResponse(status=404)
    problem = filter_problem[0]
    problem_setting = ProblemSettingModel.objects.get(problem=problem)

    #edit
    if request.method == 'POST':
        list_requirements = ['shortname', 'fullname', 'difficult', 'points_per_test',
            'statement', 'input_statement', 'constraints_statement', 'output_statement']
        for x in list_requirements:
            if x not in request.POST:
                return HttpResponse(status=500)
        #get & process data
        shortname = str(request.POST['shortname'])
        fullname = str(request.POST['fullname'])
        try:
            difficult = float(request.POST['difficult'])
        except:
            messages.add_message(request, messages.ERROR, 'Độ khó của bài phải là số thực')
            return HttpResponseRedirect(request.path_info)
        try:
            points_per_test = float(request.POST['points_per_test'])
        except:
            messages.add_message(request, messages.ERROR, 'Điểm của mỗi test phải là số thực')
            return HttpResponseRedirect(request.path_info)
        statement = str(request.POST['statement'])
        constraints_statement = str(request.POST['constraints_statement'])
        input_statement = str(request.POST['input_statement'])
        output_statement = str(request.POST['output_statement'])
        if len(shortname) == 0 or len(fullname) == 0:
            messages.add_message(request, messages.ERROR, 'Tên bài không được trống')
        elif not re.match("^[A-Za-z0-9_-]*$", shortname) or len(shortname) == 0:
            messages.add_message(request, messages.ERROR, 'Tên ngắn của bài chỉ được chứa các kí tự a-ZA-Z0-9 và _ - và không được trống')
        elif shortname != problem_short_name and ProblemModel.objects.filter(shortname=shortname).exists():
            messages.add_message(request, messages.ERROR, 'Tên bài này đã có, vui lòng chọn tên khác [shortname]')
        elif difficult < 0.0 or difficult > 10.0:
            messages.add_message(request, messages.ERROR, 'Độ khó của mỗi bài phải thuộc khoảng [0.00, 10.00]')
        elif points_per_test <= 0.0:
            messages.add_message(request, messages.ERROR, 'Độ khó của mỗi test phải lớn hơn 0.00')
        elif len(statement) == 0:
            messages.add_message(request, messages.ERROR, 'Đề bài không được trống')
        elif len(input_statement) == 0:
            messages.add_message(request, messages.ERROR, 'Đầu vào không được trống')
        elif len(constraints_statement) == 0:
            messages.add_message(request, messages.ERROR, 'Ràng buộc không được trống')
        elif len(output_statement) == 0:
            messages.add_message(request, messages.ERROR, 'Đầu ra không được trống')
        else:
            list_categories = []
            if 'list_categories[]' in request.POST:
                list_categories_tmp = request.POST.getlist('list_categories[]')
                for x in list_categories_tmp:
                    for y in ProblemCategoryModel.objects.filter(name=x):
                        list_categories.append(y.id)
            problem.fullname = fullname
            problem.shortname = shortname

            problem.difficult = difficult
            problem_setting.points_per_test = round(points_per_test, 4)
            problem_setting.statement = statement
            problem_setting.input_statement = input_statement
            problem_setting.output_statement = output_statement
            problem_setting.constraints_statement = constraints_statement
            problem_setting.save()
            problem.categories.set(list_categories)
            problem.save()

            messages.add_message(request, messages.SUCCESS, 'Cập nhật thành công')
            return redirect('/admin/problems/edit/{}/'.format(shortname))
        return redirect('/admin/problems/edit/{}/'.format(problem_short_name))
    elif request.method == 'GET':
        problem = filter_problem[0]

        problem_context = {
            'shortname': problem.shortname,
            'fullname': problem.fullname,
            'difficult': round(problem.difficult, 2),
            'categories': [x.name for x in problem.categories.all()],
            'publish_date': problem.publish_date,

            'points_per_test': problem_setting.points_per_test,
            'statement': problem_setting.statement
                if problem_setting.statement and len(problem_setting.statement) != 0 else '',
            'input_statement': problem_setting.input_statement
                if problem_setting.input_statement and len(problem_setting.input_statement) != 0 else '',
            'output_statement': problem_setting.output_statement
                if problem_setting.output_statement and len(problem_setting.output_statement) != 0 else '',
            'constraints_statement': problem_setting.constraints_statement
                if problem_setting.constraints_statement and len(problem_setting.constraints_statement) != 0 else '',
        }
        context = {
            'problem': problem_context,
            'list_categories': [x.name for x in ProblemCategoryModel.objects.all()],
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
        print(problem)
        context = {
            'list_authors': [x.username for x in problem.author.all()]
        }
        return render(request, 'admin-template/problem/edit/problemsetter.html', context)

from backend.models.filemanager import OverwriteStorage

def AdminEditProblemTestcasesDeleteView(request, problem_short_name, testcase_pk):
    if request.method == 'POST':
        filter_problem = ProblemModel.objects.filter(shortname=problem_short_name)
        if not filter_problem.exists():
            return HttpResponse(status=404)
        for problem in filter_problem:
            filter_testcase = problem.problemtestcasemodel_set.filter(pk=testcase_pk)
            if filter_testcase.exists() == False:
                return HttpResponse(status=404)
            file_manager = OverwriteStorage(settings.MEDIA_ROOT)
            for test in filter_testcase:
                file_manager.delete(test.input_file)
                file_manager.delete(test.output_file)
            filter_testcase.delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)

@admin_member_required
def AdminEditProblemTestcasesEditView(request, problem_short_name, testcase_pk):
    filter_problem = ProblemModel.objects.filter(shortname=problem_short_name)
    if not filter_problem.exists():
        return HttpResponse(status=404)
    problem = filter_problem[0]
    filter_testcase = problem.problemtestcasemodel_set.filter(pk=testcase_pk)
    if filter_testcase.exists() == False:
        return HttpResponse(status=404)
    if request.method == 'POST':
        list_requirements = ['time_limit', 'memory_limit', 'points', 'tag']
        for x in list_requirements:
            if x not in request.POST:
                return HttpResponse(status=500)
        
        #check data
        try:
            time_limit = int(request.POST['time_limit'])
        except:
            messages.add_message(request, messages.ERROR, 'Thời gian chạy phải là số nguyên dương(ms)')
            return HttpResponseRedirect(request.path_info)
        if time_limit <= 0:
            messages.add_message(request, messages.ERROR, 'Thời gian chạy phải là số nguyên dương')
            return HttpResponseRedirect(request.path_info)

        try:
            memory_limit = int(request.POST['memory_limit'])
        except:
            messages.add_message(request, messages.ERROR, 'Giới hạn bộ nhớ phải là số nguyên dương (KB)')
            return HttpResponseRedirect(request.path_info)
        if memory_limit <= 0:
            messages.add_message(request, messages.ERROR, 'Giới hạn bộ nhớ phải là số nguyên dương')
            return HttpResponseRedirect(request.path_info)

        try:
            points = float(request.POST['points'])
        except:
            messages.add_message(request, messages.ERROR, 'Điểm phải là số thực dương')
            return HttpResponseRedirect(request.path_info)
        if points <= 0:
            messages.add_message(request, messages.ERROR, 'Điểm phải là số thực dương')
            return HttpResponseRedirect(request.path_info)

        tag = request.POST['tag'] if request.POST['tag'] else ''

        #save
        test = filter_testcase[0]
        test.time_limit = time_limit
        test.memory_limit = memory_limit
        if problem.problemsettingmodel.total_points is None:
            problem.problemsettingmodel.total_points = 0
        problem.problemsettingmodel.total_points = problem.problemsettingmodel.total_points - test.points + points
        problem.problemsettingmodel.save()
        test.points = points
        test.tag = tag

        file_manager = OverwriteStorage(settings.MEDIA_ROOT)

        if 'input_file' in request.FILES:
            input_file = request.FILES['input_file']
            #input_file_path = 'problems/{}/tests/input{}.txt'.format(problem.id,str(test.id).zfill(3))
            #test.input_file = input_file_path
            file_manager.save(test.input_file, input_file)
        
        if 'output_file' in request.FILES:
            output_file = request.FILES['output_file']
            #output_file_path = 'problems/{}/tests/output{}.txt'.format(problem.id,str(test.id).zfill(3))
            #test.output_file = output_file_path
            file_manager.save(test.output_file, output_file)

        if 'is_sample' in request.POST:
            test.is_sample = True

        test.save()

        messages.add_message(request, messages.SUCCESS, 'Cập nhật thành công')

        return HttpResponseRedirect(request.path_info)
    elif request.method == 'GET':
        test = filter_testcase[0]
        context = {
            'problem': problem,
            'testcase': {
                'time_limit': test.time_limit,
                'memory_limit': test.memory_limit,
                'is_sample': test.is_sample,
                'points': test.points,
                'tag': test.tag if test.tag and len(test.tag) != 0 else '',
            }
        }
        return render(request, 'admin-template/problem/edit/edittestcase.html', context)
    else:
        return HttpResponse(status=405)


def AdminEditProblemTestcasesUploadZipView(request, problem_short_name):
    filter_problem = ProblemModel.objects.filter(shortname=problem_short_name)
    if not filter_problem.exists():
        return HttpResponse(status=404)
    problem = filter_problem[0]
    problem_grader = ProblemGraderModel.objects.get(problem=problem)
    if request.method == 'POST':
        if 'zip_testcases' not in request.FILES or 'filetype' not in request.POST:
            return HttpResponse(status=500)

        #get
        zip_testcases = request.FILES['zip_testcases']
        filetype = request.POST['filetype']
        if filetype not in ['themis', 'combine']:
            return HttpResponse(status=501)
        random_file_name = str(uuid.uuid4().hex) + '_upload_testcase.zip'
        filepath = 'problems/{}/tmp/{}'.format(problem.id, random_file_name)

        #save to tmp
        file_manager = OverwriteStorage(settings.MEDIA_ROOT)

        file_manager.save(filepath, zip_testcases)
        
        #check directory ok
        test = ''
        try:
            with zipfile.ZipFile(os.path.join(settings.MEDIA_ROOT, filepath)) as z:
                z.close()
                pass
        except:
            file_manager.delete(filepath)
            return HttpResponse('File error')

        #extract
        if filetype == 'themis':
            problem_input_file_name = problem_grader.input_filename
            problem_output_file_name = problem_grader.output_filename
            list_testcases_folder = []
            with zipfile.ZipFile(os.path.join(settings.MEDIA_ROOT, filepath)) as z:
                all_path = z.namelist()
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
                    #success
                    folderpath = 'problems/{}/tests/'.format(problem.id, uuid.uuid4().hex)
                    try:
                        shutil.rmtree(os.path.join(settings.MEDIA_ROOT, folderpath))
                    except: pass
                    try:
                        os.mkdir(os.path.join(settings.MEDIA_ROOT, folderpath))
                    except: pass
                    problem.problemtestcasemodel_set.all().delete()
                    problem.problemsettingmodel.total_points = problem.problemsettingmodel.points_per_test * len(list_testcases_folder)
                    problem.problemsettingmodel.save()
                    prepare_db = []
                    for tmp_id in range(0, len(list_testcases_folder), 1):
                        zip_folder = list_testcases_folder[tmp_id]
                        zip_input = list_input[tmp_id]
                        zip_output = list_output[tmp_id]

                        id = tmp_id + 1
                        os.mkdir(os.path.join(settings.MEDIA_ROOT, 'problems', str(problem.id), 'tests', zip_folder))

                        #update database
                        testdb = ProblemTestCaseModel(
                            problem=problem,
                            time_limit=problem_grader.time_limit,
                            memory_limit=problem_grader.time_limit,
                            points=problem.problemsettingmodel.points_per_test,
                            name=zip_folder.strip('/').strip('\\'),
                            input_file=os.path.join('problems', str(problem.id), 'tests', zip_folder, problem.problemgradermodel.input_filename),
                            output_file=os.path.join('problems', str(problem.id), 'tests', zip_folder, problem.problemgradermodel.output_filename))
                        prepare_db.append(testdb)

                        #write input
                        with open(os.path.join(settings.MEDIA_ROOT, 'problems', str(problem.id), 'tests', zip_folder, problem.problemgradermodel.input_filename), 'wb') as f:
                            f.write(z.read(zip_input))

                        #write output
                        with open(os.path.join(settings.MEDIA_ROOT, 'problems', str(problem.id), 'tests', zip_folder, problem.problemgradermodel.output_filename), 'wb') as f:
                            f.write(z.read(zip_output))
                    problem.problemtestcasemodel_set.bulk_create(prepare_db)

                    messages.add_message(request, messages.SUCCESS, 'Tải lên thành công')
                    
            file_manager.delete(filepath)
            return HttpResponseRedirect('/admin/problems/edit/{}/testcases'.format(problem.shortname))
            
        elif filetype == 'combine':
            with zipfile.ZipFile(os.path.join(settings.MEDIA_ROOT, filepath)) as z:
                pass
        return HttpResponse(test)
    else:
        return HttpResponse(status=405)


@admin_member_required
@never_cache
def AdminEditProblemTestcasesview(request, problem_short_name):
    filter_problem = ProblemModel.objects.filter(shortname=problem_short_name)
    if not filter_problem.exists():
        return HttpResponse(status=404)
    problem = filter_problem[0]

    #edit
    if request.method == 'POST':
        if 'input_file' not in request.FILES:
            return HttpResponse(status=500)
        file = OverwriteStorage(settings.MEDIA_ROOT)
        input_file = request.FILES['input_file']
        file.save('test.txt', input_file)
        return HttpResponseRedirect(request.path_info)

    #show list testcases
    elif request.method == 'GET':
        '''
        for x in range(1, 100, 1):
            problem.problemtestcasemodel_set.create(problem=problem, tag=str(randint(1, 999999)),
                time_limit=randint(1,999999), memory_limit=randint(1,99999999), points=random(), input_file='input',
                output_file='output').save()
        '''
        list_testcases = [{
                'pk': x.id,
                'id': 0,
                'tag': x.tag if x.tag and len(x.tag) != 0 else '',
                'time_limit': x.time_limit,
                'memory_limit': x.memory_limit,
                'is_sample': x.is_sample,
                'points': x.points,
                'input_file': settings.MEDIA_URL + x.input_file,
                'output_file': settings.MEDIA_URL + x.output_file,
            } for x in problem.problemtestcasemodel_set.all()]
        for id in range(0, len(list_testcases), 1):
            list_testcases[id]['id'] = id + 1
        list_allow_format = [
            {
                'value': 'themis',
                'display': 'Themis format',
            },
            {
                'value': 'pc2',
                'display': 'PC^2 format',
            },
            {
                'value': 'combine',
                'display': 'Combine format'
            }
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
def AdminEditProblemLanguagesview(request, problem_short_name):
    
    return render(request, 'admin-template/problem/edit/languages.html')

@admin_member_required
def AdminEditProblemSettingsview(request, problem_short_name):
    filter_problem = ProblemModel.objects.filter(shortname=problem_short_name)
    if not filter_problem.exists():
        return HttpResponse(status=404)
    problem = filter_problem[0]
    problem_setting = ProblemSettingModel.objects.get(problem=problem)
    problem_grader = ProblemGraderModel.objects.get(problem=problem)

    if request.method == 'POST':
        list_requirements = ['input_filename', 'output_filename', 'submission_visible_mode', 'time_limit', 'memory_limit', 'problem_type']
        for x in list_requirements:
            if x not in request.POST:
                return HttpResponse(status=500)

        input_filename = request.POST['input_filename']
        output_filename = request.POST['output_filename']
        try:
            submission_visible_mode = int(request.POST['submission_visible_mode'])
        except: return HttpResponse(status=500)
        try:
            problem_type = int(request.POST['problem_type'])
        except: return HttpResponse(status=500)
        try:
            time_limit = int(request.POST['time_limit'])
            if time_limit <= 0:
                raise 'error'
        except:
            messages.add_message(request, messages.ERROR, 'Thời gian chạy phải là số  nguyên dương')
            return HttpResponseRedirect(request.path_info)
        try:
            memory_limit = int(request.POST['memory_limit'])
            if memory_limit <= 0:
                raise 'error'
        except:
            messages.add_message(request, messages.ERROR, 'Giới hạn bộ nhớ phải là số nguyên dương')
            return HttpResponseRedirect(request.path_info)

        use_stdin = True if 'use_stdin' in request.POST else False
        use_stdout = True if 'use_stdout' in request.POST else False

        problem.problem_type = problem_type
        problem.save()

        problem_setting.submission_visible_mode = submission_visible_mode
        problem_setting.save()

        problem_grader.input_filename = input_filename
        problem_grader.output_filename = output_filename
        problem_grader.use_stdin = use_stdin
        problem_grader.use_stdout = use_stdout
        problem_grader.time_limit = time_limit
        problem_grader.memory_limit = memory_limit
        problem_grader.save()

        messages.add_message(request, messages.SUCCESS, 'Cập nhật thành công')

        return HttpResponseRedirect(request.path_info)
    elif request.method == 'GET':

        context = {
            'submission_visible_mode_choices': [
                {
                    'value': x[0],
                    'display': x[1],
                } for x in SUBMISSION_VISIBLE_MODE_CHOICES
            ],
            'problem_type_choices': [
                {
                    'value': x[0],
                    'display': x[1]
                } for x in PROBLEM_TYPE_CHOICES
            ],
            'problem_type':problem.problem_type,
            'input_filename': problem_grader.input_filename,
            'output_filename': problem_grader.output_filename,
            'use_stdin': problem_grader.use_stdin,
            'use_stdout': problem_grader.use_stdout,
            'time_limit': problem_grader.time_limit,
            'memory_limit': problem_grader.memory_limit,
            'submission_visible_mode': problem_setting.submission_visible_mode
        }

        return render(request, 'admin-template/problem/edit/settings.html', context)

import os
from judger.grader import CppGrader

@admin_member_required
def AdminEditProblemCustomCheckerview(request, problem_short_name):
    filter_problem = ProblemModel.objects.filter(shortname=problem_short_name)
    if not filter_problem.exists():
        return HttpResponse(status=404)
    problem = filter_problem[0]
    problem_grader = ProblemGraderModel.objects.get(problem=problem)

    #edit
    if request.method == 'POST':
        list_requirements = ['checker_source']

        for x in list_requirements:
            if x not in request.POST:
                return HttpResponse(status=500)
        
        use_checker = True if 'use_checker' in request.POST else False
        checker_source = str(request.POST['checker_source'])

        context = {}
        context['checker_source'] = checker_source
        context['use_checker'] = use_checker

        # biên dịch
        if use_checker:
            grader = CppGrader(None, None)
            os.system('mkdir -p ' + os.path.join(settings.MEDIA_ROOT, 'problems/{}/checker'.format(problem.id)))
            os.system('cp checker/testlib.h ' + os.path.join(settings.MEDIA_ROOT, 'problems/{}/checker/testlib.h'.format(problem.id)))
            with open(os.path.join(settings.MEDIA_ROOT, 'problems/{}/checker/checker.cpp'.format(problem.id)), 'w', encoding='utf-8') as f:
                f.write(checker_source)
            result, msg = grader.compileChecker(os.path.join(settings.MEDIA_ROOT, 'problems/{}'.format(problem.id)))
            if not result:
                messages.add_message(request, messages.ERROR, 'Biên dịch gặp lỗi')
                context['compile_error'] = msg
                return render(request, 'admin-template/problem/edit/checker.html', context)
            
        problem_grader.use_checker = use_checker
        problem_grader.checker = checker_source
        problem_grader.save()

        messages.add_message(request, messages.SUCCESS, 'Cập nhật thành công')

        return render(request, 'admin-template/problem/edit/checker.html', context)

    elif request.method == 'GET':
        context = {
            'use_checker': problem_grader.use_checker,
            'checker_source': problem_grader.checker,
        }
        return render(request, 'admin-template/problem/edit/checker.html', context)
    else:
        return HttpResponse(status=405)


from time import time
from datetime import datetime
from django.db.models import Max, Count

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
            messages.add_message(request, messages.ERROR, 'Tên ngắn của bài chỉ được chứa các kí tự a-ZA-Z0-9 và _ và không được trống')
        elif ProblemModel.objects.filter(shortname=shortname).exists():
            messages.add_message(request, messages.ERROR, 'Bài {} đã tồn tại'.format(shortname))
        elif len(fullname) == 0:
            messages.add_message(request, messages.ERROR, 'Tên đầy đủ của bài không được trống')
        else:
            problem = ProblemModel.CreateNewProblem(shortname, fullname, request.user)
            problem.save()
            messages.add_message(request, messages.SUCCESS, 'Tạo thành công')
            return redirect('/admin/problems/edit/{}'.format(shortname))
        return HttpResponseRedirect(request.path_info)
    elif request.method == 'GET':



        return render(request, 'admin-template/problem/createproblem.html')
    else:
        return HttpResponse(status=405)

