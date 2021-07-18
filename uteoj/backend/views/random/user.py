from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.db import transaction
import json


@csrf_exempt
def CreateRandomUser(request):
    list_requirements = ['startwith', 'count', 'isadmin']
    for x in list_requirements:
        if x not in request.GET:
            return JsonResponse({
                'status': 'error',
                'message': 'missing \'' + x + '\' parameter',
            })
    try:
        msg_error = 'startwith error'
        startwith = request.GET['startwith']
        msg_error = 'count error (must be integer)'
        count = int(request.GET['count'])
        msg_error = 'isadmin error (must be bool)'
        isadmin = True if request.GET['isadmin'] == 'True' else False
    except:
        return JsonResponse({
                'status': 'error',
                'message': msg_error
            })
    
    response = []
    with transaction.atomic():
        for x in range(0, count, 1):
            try:
                user = User.objects.create_user(username=startwith + str(x),password='12345678')
                user.is_staff = isadmin
                user.save()
            except:
                HttpResponse('User \'' + startwith + str(x) + '\' đã tồn tại ')
    return HttpResponse('Created ' + str(count) + ' user ok')

