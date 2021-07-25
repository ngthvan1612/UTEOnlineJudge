from django.http.response import HttpResponseRedirect
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


def UserProblemView(request, shortname):
    problems = ProblemModel.objects.filter(shortname=shortname)
    if problems.exists() == False:
        return HttpResponse(status=404)
    return HttpResponse(serializers.serialize('json', problems, indent=4),
        content_type="text/json-comment-filtered")

from backend.task.submit import SubmitSolution


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
        if 'source_code' not in request.POST:
            return HttpResponse('Thiếu source code')
        language_filter = LanguageModel.objects.filter(name=request.POST['language'])
        if not language_filter.exists():
            return HttpResponse('Không có ngôn ngữ nào tên \'{}\''.format(request.POST['language']))
        language=LanguageModel.objects.get(name=request.POST['language'])
        source_code = request.POST['source_code']

        submission = SubmissionModel.objects.create(
            user=request.user,
            problem=problem,
            submission_date=datetime.now(),
            source_code = source_code,
            language=language)
        submission.status = SubmissionStatusType.InQueued
        submission.save()
        
        SubmitSolution.delay(submission.id)
        return HttpResponse('<h2>Submit ok: id = {}</br>Bài tập: <font style="color:red;">{}</font> ({})</br>Người dùng: {}</br>Ngôn ngữ: {}</h2>'
            .format(submission.id, problem.shortname, problem.fullname, request.user.username, language.name))
    elif request.method == 'GET':
        template = """
        <form action="" method="post">
            <label>Ngôn ngữ: </label>
            <input name="language" type="text"/>
            </br>
            </br>
            <label>Source code: </label>
            <textarea name="source_code" cols="100" rows="20"></textarea>
            </br>
            <input value="Nộp bài" type="submit">
        </form>
        """
        return HttpResponse(template)
    else:
        return HttpResponse(status=405)



