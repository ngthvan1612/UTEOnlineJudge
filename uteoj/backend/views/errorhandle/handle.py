from django.http import HttpResponse


def ErrorHandle404(request, exception):

    return HttpResponse('Khong tim thay trang yeu cau')


def ErrorHandle403(request, exception):

    return HttpResponse('Error 403')


def ErrorHandle400(request, exception):

    return HttpResponse('Error 400')


def ErrorHandle500(request, exception):

    return HttpResponse('Error 500')

