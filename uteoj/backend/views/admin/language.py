import re
import os.path
import json
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from backend.views.auth.login import LoginView
from backend.views.admin.require import admin_member_required
from django.contrib.auth.models import User
from backend.models.usersetting import UserSetting
from django.http import HttpResponse
from backend.models.filemanager import UserFileManager
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.contrib import messages
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from backend.models.language import LanguageModel
from backend.models.language import LanguageSerializer


@admin_member_required
def AdminListLanguageView(request):
    if request.method == 'GET':
        list_language = [{
                'id': 0,
                'lang_id': x.id,
                'lang_name': x.name,
                'lang_ext': x.ext,
                'lang_description': x.description,
                'lang_compile_command': x.compile_command,
                'lang_run_command': x.run_command,
            }
            for x in LanguageModel.objects.all()]
        for id in range(0, len(list_language), 1):
            list_language[id]['id'] = id + 1

        context = {
            'list_language': list_language,
        }

        return render(request, 'admin-template/language/listLanguage.html', context)
    
    return HttpResponse(status=405)

def CheckLanguageRequire(name, ext, desc, compile_command, run_command, check_name_existed):
    if len(name) == 0 or not name:
        return ['error', 'Tên không được trống']
    if check_name_existed == True:
        if LanguageModel.objects.filter(name=name).exists():
            return [ 'error', 'Tên này đã tồn tại']
    if len(ext) == 0 or not ext:
        return ['error', 'Ext không được trống']
    if len(desc) == 0 or not desc:
        return ['error', 'Thông tin không được trống']
    if len(run_command) == 0 or not run_command:
        return ['error', 'Lệnh thực thi không được trống']
    return ['success', 'success']

@never_cache
@admin_member_required
def AdminCreateNewLanguage(request):
    #create new
    if request.method == 'POST':
        list_requirements = ['lang_name', 'lang_ext', 'lang_description','lang_compile_command', 'lang_run_command']
        for x in list_requirements:
                if x not in request.POST:
                    return HttpResponse(status=500)
        lang_name = request.POST['lang_name']
        lang_ext = request.POST['lang_ext']
        lang_description = request.POST['lang_description']
        lang_compile_command = request.POST['lang_compile_command']
        lang_run_command = request.POST['lang_run_command']
        status, message = CheckLanguageRequire(lang_name, lang_ext, lang_description,
            lang_compile_command, lang_run_command, True)
        if status == 'error':
            messages.add_message(request, messages.ERROR, message)
        else:
            messages.add_message(request, messages.SUCCESS, 'Tạo thành công')
            LanguageModel.objects.create(name=lang_name,
                ext=lang_ext, description=lang_description, run_command=lang_run_command,
                compile_command = lang_compile_command).save()
        return HttpResponseRedirect(request.path_info)
    return render(request, 'admin-template/language/createNewLanguage.html')


@never_cache
@admin_member_required
def AdminDeleteLanguage(request, lang_id):
    if request.method == 'POST':
        LanguageModel.objects.filter(id=lang_id).delete()
        return HttpResponseRedirect('/admin/language/')
    return HttpResponse(status=405)

@never_cache
@admin_member_required
def AdminEditLanguageView(request, lang_id):
    #pre-process
    filter_lang = LanguageModel.objects.filter(id=lang_id)
    if not filter_lang.exists():
        return HttpResponse(status=404)
    lang = filter_lang[0]

    #edit
    if request.method == 'POST':
        list_requirements = ['lang_name', 'lang_ext', 'lang_description','lang_compile_command', 'lang_run_command']

        for x in list_requirements:
            if x not in request.POST:
                return HttpResponse(status=500)
        
        lang_name = request.POST['lang_name']
        lang_ext = request.POST['lang_ext']
        lang_description = request.POST['lang_description']
        lang_compile_command = request.POST['lang_compile_command']
        lang_run_command = request.POST['lang_run_command']
        
        if lang_name != lang.name and LanguageModel.objects.filter(name=lang_name).exists():
            messages.add_message(request, messages.ERROR, 'Tên này đã tồn tại')
        else:
            status, message = CheckLanguageRequire(lang_name, lang_ext, lang_description,
                lang_compile_command, lang_run_command, False)
            if status == 'error':
                messages.add_message(request, messages.ERROR, message)
            else:
                lang.name = lang_name
                lang.ext = lang_ext
                lang.description = lang_description
                lang.compile_command = lang_compile_command
                lang.run_command = lang_run_command
                lang.save()
                messages.add_message(request, messages.SUCCESS, 'Cập nhật thành công')
        
        return HttpResponseRedirect(request.path_info)

    elif request.method == 'GET':

        context = {
            'lang_id': lang.id,
            'lang_name': lang.name,
            'lang_ext': lang.ext,
            'lang_description': lang.description,
            'lang_compile_command': lang.compile_command,
            'lang_run_command': lang.run_command,
        }

        return render(request, 'admin-template/language/editLanguage.html', context)
    
    #unknown method
    else:
        return HttpResponse(status=405)
