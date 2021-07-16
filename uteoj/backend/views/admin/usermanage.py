from random import randint
import re
import os.path
import json
from django.conf import settings
from django.contrib import messages
from django.db.models.query_utils import Q
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from backend.views.auth.login import LoginView
from backend.views.admin.require import admin_member_required
from django.contrib.auth.models import User
from backend.models.usersetting import UserSetting
from django.http import HttpResponse
from backend.models.filemanager import UserFileManager
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

def AdminFilterListUser(request, is_staff, template):
    list_user_filter = User.objects.all()
    if 'search' in request.GET:
        search = request.GET['search']
        list_user_filter = list_user_filter.filter(
            Q(username__contains=search) | 
            Q(first_name__contains=search) | 
            Q(last_name__contains=search)
        )
    list_users = [{
            'id': -1,
            'username': x.username,
            'first_name': x.first_name,
            'last_name': x.last_name,
            'date_joined': x.date_joined,
            'is_active': x.is_active,
        } for x in list_user_filter.order_by('is_active') if x.is_staff == is_staff]
    for x in range(0, len(list_users), 1):
        list_users[x]['id'] = x + 1
    rows_per_page = request.GET.get('rows_per_page') if 'rows_per_page' in request.GET else 10
    paginator = Paginator(list_users, rows_per_page)
    page_num = request.GET.get('page')
    page_obj = paginator.get_page(page_num)
    context = {
        'page_obj': page_obj,
    }
    return render(request, template, context)

@admin_member_required
def AdminListAdministratorsView(request):
    return AdminFilterListUser(request, True, 'admin-template/user/listAdmin.html')

@admin_member_required
def AdminListUsersView(request):
    return AdminFilterListUser(request, False, 'admin-template/user/listContestant.html')


@admin_member_required
def AdminDeleteUser(request, user_name):
    if request.method == 'POST':
        filter_user = User.objects.filter(username=user_name)
        if filter_user.exists() == False:
            return HttpResponse(status=404)
        if user_name in settings.LIST_SUPER_USER:
            is_staff = True
            messages.add_message(request, messages.ERROR, 'Không thể xóa người dùng \'{}\''.format(user_name))
        else:
            is_staff = filter_user[0].is_staff
            for user in filter_user:
                UserFileManager.deleteUserFile(user)
            filter_user.delete()
            messages.add_message(request, messages.SUCCESS, 'Xóa người dùng \'{}\' thành công'.format(user_name))
        if is_staff == True:
            return HttpResponseRedirect('/admin/users/administrators/')
        else:
            return HttpResponseRedirect('/admin/users/contestants/')
    else:
        return HttpResponse(status=405)


@admin_member_required
def AdminCreateUserView(request):
    if request.method == 'POST':
        #check data
        list_requirements = [ 'first_name', 'last_name', 'user_name', 'password', 'email', 'job']
        for x in list_requirements:
            if x not in request.POST:
                return HttpResponse(status=500)
        
        #get data
        make_user_admin = True if 'make_user_admin' in request.POST else False
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user_name = request.POST['user_name']
        password = request.POST['password']
        job = request.POST['job']

        #check require
        if len(first_name) == 0:
            messages.add_message(request, messages.ERROR, 'Tên không được trống')
        elif len(last_name) == 0:
            messages.add_message(request, messages.ERROR, 'Họ không được trống')
        elif len(user_name) < 5:
            messages.add_message(request, messages.ERROR, 'Tên đăng nhập phải có từ 5 kí tự trở lên')
        elif not re.match("^[A-Za-z0-9_-]*$", user_name):
            messages.add_message(request, messages.ERROR, 'Tên đăng nhập chỉ gồm các kí tự A-Za-z0-9 và _')
        elif User.objects.filter(username=user_name).exists():
            messages.add_message(request, messages.ERROR, 'Tên đăng nhập đã tồn tại')
        elif len(email) == 0:
            messages.add_message(request, messages.ERROR, 'Email không được trống')
        elif User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Email này đã được đăng ký')
        elif len(password) < 8:
            messages.add_message(request, messages.ERROR, 'Mật khẩu phải từ 8 ký tự trở lên')
        else:

            #create
            user = User.objects.create_user(username=user_name, email=email, password=password, first_name=first_name, last_name=last_name)
            if make_user_admin == True:
                user.is_staff = True
            user.save()
            UserSetting.objects.create(user=user, job=job).save()
            messages.add_message(request, messages.SUCCESS, 'Đăng ký thành công')
        
        return HttpResponseRedirect(request.path_info)
    elif request.method == 'GET':
        return render(request, 'admin-template/user/createNewUser.html')
    else:
        return HttpResponse(status=405)


@admin_member_required
def AdminEditUserView(request, user_name):
    if not User.objects.filter(username=user_name).exists():
        messages.add_message(request, messages.ERROR, 'Không tìm thấy người dùng \'{}\''.format(user_name))
        return HttpResponseRedirect('/admin/users/contestants/')
    user = User.objects.get(username=user_name)
    if not UserSetting.objects.filter(user=user):
        UserSetting.objects.create(user=user).save()
    user_setting = UserSetting.objects.get(user=user)
    
    #edit
    if request.method == 'POST':
        #check data
        list_requirements = ['first_name', 'last_name', 'user_job', 'email',]
        for x in list_requirements:
            if x not in request.POST:
                print('missing ' + x)
                return HttpResponse(status=500)
        
        is_admin = True if 'is_admin' in request.POST else False
        is_active = True if 'is_active' in request.POST else False

        if (user.username in settings.LIST_SUPER_USER) and (is_admin == False or is_active == False):
            if is_admin == False:
                messages.add_message(request, messages.ERROR, 'Không thể thiết đặt người dùng \'{}\' thành người dùng thường (non-admin)'.format(user.username))
            if is_active == False:
                messages.add_message(request, messages.ERROR, 'Không thể khóa người dùng \'{}\''.format(user.username))
        else:
            #get data
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            user_job = request.POST['user_job']
            email = request.POST['email']

            #update & save
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.is_staff = is_admin
            user.is_active = is_active
            user.save()

            user_setting.job = user_job
            user_setting.save()

            if 'user_avatar' in request.FILES:
                user_avatar = request.FILES['user_avatar']
                extension = os.path.splitext(user_avatar.name)[1]
                UserFileManager.uploadFile(user, 'avatar', extension, user_avatar.file, True, True)
            
            messages.add_message(request, messages.SUCCESS, 'Cập nhật thành công')
        return HttpResponseRedirect(request.path_info)

    #get custom user profile
    elif request.method == 'GET':
        context = {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_staff,
            'is_active': user.is_active,
            'date_joined': user.date_joined,
            'job': user_setting.job,
        }

        context_user_avatar =  UserFileManager.getUserAvatar(user)
        if context_user_avatar is not None:
            context['avatar'] = context_user_avatar + '?v={}'.format(randint(0, 11111111111))
        
        if not user.is_active:
            messages.add_message(request, messages.ERROR, 'Tài khoản này đã bị khóa')
        return render(request, 'admin-template/user/profile.html', context)

    return HttpResponse(status=405)