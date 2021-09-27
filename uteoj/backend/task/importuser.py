from backend.models.settings import OJSettingModel
from celery.decorators import task
from django.contrib.auth.models import User
from django.utils import timezone
import time
import uuid
from judger.grader import *
from django.contrib.auth.hashers import make_password

@task(name="import_user")
def ImportUserAsync(prefix, suffix, lsSinhVien):

    # khóa đăng ký

    __begin = time.time()
    tmp_allow_register = OJSettingModel.getAllowRegister()
    OJSettingModel.setAllowRegister(False)

    # build username + password + create
    prepare_query = []

    for sv in lsSinhVien:
        mssv, ho, ten, username, password = sv
        prepare_query.append(User(
            username=username,
            password=make_password(password, None, 'md5'),
            first_name=ten,
            last_name=ho,
            is_active=True,
            is_staff=False
        ))
    User.objects.bulk_create(prepare_query)
    OJSettingModel.setAllowRegister(tmp_allow_register)

    print(f"Nhập {len(lsSinhVien)} người dùng trong {time.time() - __begin} ms")
