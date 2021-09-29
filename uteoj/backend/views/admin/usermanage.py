from random import randint
import re
from backend.filemanager.importuser import ImportUserStorage
from backend.task.importuser import ImportUserAsync
from django.conf import settings
from django.contrib import messages
from django.db.models.query_utils import Q
from django.http.response import Http404, HttpResponseRedirect
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from backend.views.auth.login import LoginView
from backend.views.admin.require import admin_member_required
from django.contrib.auth.models import User
from backend.models.usersetting import ImportUserFileModel, UserSetting
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from PIL import Image
import pandas as pd
import numpy as np
from django.utils import timezone
import uuid
from django.db.models import Q

def AdminFilterListUser(request, is_staff, template):
    list_user_filter = User.objects.all()
    if 'search' in request.GET:
        search = request.GET['search']
        tmp = search.split(' ')
        ho = ' '.join(tmp[::-1])
        ten = tmp[-1]
        list_user_filter = list_user_filter.filter(
            Q(username__icontains=search) | 
            Q(first_name__icontains=search) | 
            Q(last_name__icontains=search) |
            Q(first_name__icontains=ten) |
            Q(last_name__icontains=ho)
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
    rows_per_page = request.GET.get('rows_per_page') if 'rows_per_page' in request.GET else 50
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
                UserSetting.deleteUserSettingAndFile(user)
            filter_user.delete()
            messages.add_message(request, messages.SUCCESS, 'Xóa người dùng \'{}\' thành công'.format(user_name))
        if is_staff == True:
            return HttpResponseRedirect('/admin/users/administrators/')
        else:
            return HttpResponseRedirect('/admin/users/contestants/')
    else:
        return HttpResponse(status=405)

@admin_member_required
def AdminImportUserResultViewer(request, huid, token, name):
    fid = ImportUserFileModel.DecryptId(huid)
    fileModel = get_object_or_404(ImportUserFileModel, id=fid)
    if token != fileModel.token or name != fileModel.name:
        raise Http404()
    file_manager = ImportUserStorage()
    return file_manager.loadImportUser(fileModel.name)

@admin_member_required
def AdminImportUser(request):
    return HttpResponse('Xoa trang nay')
    if request.method == 'POST':
        if 'userexcelfile' not in request.FILES:
            messages.add_message(request, messages.WARNING, 'Bạn phải upload một file lên')
            return HttpResponseRedirect(request.path_info)
        prefix = request.POST.get('prefix')
        suffix = request.POST.get('suffix')
        xls = request.FILES.get('userexcelfile')
        if prefix == None or suffix == None:
            return HttpResponse(status=500)
        if not re.match("^[A-Za-z0-9_]*$", prefix):
            messages.add_message(request, messages.ERROR, 'Tiền tố chỉ gồm các kí tự A-Za-z0-9 và _')
            return HttpResponseRedirect(request.path_info)
        if not re.match("^[A-Za-z0-9_]*$", suffix):
            messages.add_message(request, messages.ERROR, 'Hậu tố chỉ gồm các kí tự A-Za-z0-9 và _')
            return HttpResponseRedirect(request.path_info)

        # preprocessing
        try:
            df = pd.read_excel(BytesIO(xls.read()))
        except:
            messages.add_message(request, messages.ERROR, 'Không đọc được file')
            return HttpResponseRedirect(request.path_info)
        
        listFilterUser = User.objects.values_list('username').filter(username__startswith=prefix,username__endswith=suffix).all()
        listFilterUser = {x[0] for x in listFilterUser}

        data = df.to_numpy()
        lsSinhVien = []

        for x in data:
            mssv, ho, ten = str(x[1]), str(x[3]), str(x[4])
            if mssv.isdigit() and ho != 'nan' and ten != 'nan':
                username = prefix + mssv + suffix
                if username in listFilterUser:
                    messages.add_message(request, messages.ERROR, f"Tên đăng nhập {username} đã có")
                    return HttpResponseRedirect(request.path_info)

                password = uuid.uuid4().hex[:8]
                lsSinhVien.append((mssv, ho.strip(), ten.strip(), username, password))

        # importing
        fileModel = ImportUserFileModel.objects.create(
            name=f"UTEOJ_IMPORT_USERS_{timezone.localtime(timezone.now()).strftime('%m-%d-%Y__%H-%M-%S')}.xls",
            token=uuid.uuid4().hex + uuid.uuid4().hex)
        fileModel.save()

        messages.add_message(request, messages.SUCCESS, f"Đang nhập")
        lsOutput = np.array(lsSinhVien)
        stream = BytesIO()

        pdOutput = pd.DataFrame(lsOutput, columns=('Mã số SV', 'Họ và tên lót', 'Tên', 'Tên đăng nhập', 'Mật khẩu'))
        pdOutput.index += 1
        pdOutput.to_excel(stream, engine='xlwt')

        file_manager = ImportUserStorage()
        file_manager.saveImportUser(fileModel.name, stream)

        ImportUserAsync.apply_async(
            args=[prefix, suffix, lsSinhVien],
            queue='uteoj_system')
        
        context = {
            'exportFile': f"/admin/users/import/{ImportUserFileModel.EncryptId(fileModel.id)}/{fileModel.token}/{fileModel.name}"
        }

        return render(request, 'admin-template/user/importuser.html', context)
    elif request.method == 'GET':

        return render(request, 'admin-template/user/importuser.html')
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
            UserSetting.createSettingIfNotExists(user)
            messages.add_message(request, messages.SUCCESS, 'Đăng ký thành công')
        
        return HttpResponseRedirect(request.path_info)
    elif request.method == 'GET':
        return render(request, 'admin-template/user/createNewUser.html')
    else:
        return HttpResponse(status=405)

from PIL import Image
from io import BytesIO, StringIO

@admin_member_required
def AdminEditUserView(request, user_name):
    if not User.objects.filter(username=user_name).exists():
        messages.add_message(request, messages.ERROR, 'Không tìm thấy người dùng \'{}\''.format(user_name))
        return HttpResponseRedirect('/admin/users/contestants/')
    user = User.objects.get(username=user_name)
    user_setting = UserSetting.getSetting(user)
    
    #edit
    if request.method == 'POST':
        #check data
        list_requirements = ['first_name', 'last_name', 'user_job', 'email',]
        for x in list_requirements:
            if x not in request.POST:
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

            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.is_staff = is_admin
            user.is_active = is_active
            user.save()

            user_setting.job = user_job

            if 'user_avatar' in request.FILES:
                user_avatar = request.FILES['user_avatar']
                if user_avatar.size > 1024 * 1024 * 200:
                    messages.add_message(request, messages.ERROR, 'File ảnh đại diên không được vượt quá 2MB')
                    return HttpResponseRedirect(request.path_info)
                user_setting.uploadAvatar(user_avatar.file)
            
            user_setting.save()
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

        context_user_avatar =  UserSetting.getSetting(user).avatar
        if context_user_avatar is not None:
            context['avatar'] = context_user_avatar + '?v={}'.format(randint(0, 11111111111))
        
        if not user.is_active:
            messages.add_message(request, messages.ERROR, 'Tài khoản này đã bị khóa')
        return render(request, 'admin-template/user/profile.html', context)

    return HttpResponse(status=405)


