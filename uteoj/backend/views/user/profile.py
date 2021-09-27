from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from backend.models.problem import ProblemModel
from backend.models.problem import ProblemCategoryModel
from backend.models.usersetting import UserSetting
from django.db.models import Q

from datetime import datetime
from random import random
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import redirect
from django.contrib import messages

from random import randint


def UserAvatarViewer(request, token, sha):
    user_id = UserSetting.decryptUserId(token)
    user = get_object_or_404(User, id=user_id)
    usersetting = UserSetting.getSetting(user)
    if sha != usersetting.public_key:
        raise Http404()
    return usersetting.getAvatar()


def UserEditMyProfile(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    UserSetting.createSettingIfNotExists(request.user)
    if request.method == 'POST':
        last_name = request.POST['last_name'] if 'last_name' in request.POST else ''
        first_name = request.POST['first_name'] if 'first_name' in request.POST else ''
        job = request.POST['job'] if 'job' in request.POST else ''
        request.user.first_name = first_name
        request.user.last_name = last_name
        request.user.usersetting.job = job

        if 'user_avatar' in request.FILES:
            user_avatar = request.FILES['user_avatar']
            if user_avatar.size > 1024 * 1024 * 2:
                messages.add_message(request, messages.ERROR, 'File ảnh đại diên không được vượt quá 2MB')
                return HttpResponseRedirect(request.path_info)
            request.user.usersetting.uploadAvatar(user_avatar.file)
        
        # success
        request.user.usersetting.save()
        request.user.save()
        return HttpResponseRedirect(request.path_info)
    elif request.method == 'GET':
        context = {}
        context_user_avatar = UserSetting.getSetting(request.user).avatar
        if context_user_avatar is not None and len(context_user_avatar) > 0:
            context['avatar'] = context_user_avatar + '?v={}'.format(randint(0, 11111111111)) # Chống cached
        return render(request, 'user-template/profile.html', context)
    else:
        return HttpResponse(status=405)