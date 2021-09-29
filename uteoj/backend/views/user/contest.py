from django.utils import timezone
from backend.models.contest import ContestModel
from django.http.response import Http404, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def UserContestListView(request):
    currentTime = timezone.localtime(timezone.now())
    list_contests = ContestModel.objects.all()[::-1]

    print('Hiện tại: ' + str(currentTime))
    for contest in list_contests:
        if currentTime < contest.startTime:
            contest.status = 'notstarted'
        elif currentTime > contest.endTime:
            contest.status = 'ended'
        else:
            contest.status = 'running'
    
    context = {
        'list_contests': list_contests
    }

    return render(request, 'user-template/contest/listcontest.html', context)


@require_http_methods(['GET'])
def UserContestView(request, id):
    contest = get_object_or_404(ContestModel, pk=id)

    currentTime = timezone.localtime(timezone.now())
    print('Hiện tại: ' + str(currentTime))
    if currentTime < contest.startTime:
        contest.status = 'notstarted'
    elif currentTime > contest.endTime:
        contest.status = 'ended'
    else:
        contest.status = 'running'

    context = {
        'contest': contest
    }

    return render(request, 'user-template/contest/details.html', context)
