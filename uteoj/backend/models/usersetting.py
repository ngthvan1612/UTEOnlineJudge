from django.contrib.auth.decorators import user_passes_test
from django.core.files.base import ContentFile
from django.http.response import FileResponse
from backend.filemanager.userstorage import UserStorage
from django.utils.translation import npgettext
from backend.models.problem import ProblemModel
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import uuid
import os
from io import BytesIO
from PIL import Image


class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    hash_user_profile = models.CharField(max_length=255, blank=True, null=True)
    public_key = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True)
    job = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

    @staticmethod
    def createSettingIfNotExists(user:User):
        if not UserSetting.objects.filter(user=user).exists():
            new_setting = UserSetting.objects.create(
                user=user,
                hash_user_profile=uuid.uuid4().hex + '_' + uuid.uuid4().hex,
                public_key=uuid.uuid4().hex + '_' + uuid.uuid4().hex,
                avatar='',
                job='')
            new_setting.save()
            return new_setting
        return UserSetting.objects.get(user=user)

    @staticmethod
    def deleteUserSettingAndFile(user:User) -> None:
        pass
    
    @staticmethod
    def getSetting(user:User):
        setting_filter = UserSetting.objects.filter(user=user)
        if not setting_filter.exists():
            return UserSetting.createSettingIfNotExists(user)
        return setting_filter[0]
    
    def getAvatar(self):
        file_manager = UserStorage(self.user)
        return file_manager.loadUserAvatar()

    def uploadAvatar(self, content) -> None:
        file_manager = UserStorage(self.user)
        self.public_key = uuid.uuid4().hex + '_' + uuid.uuid4().hex
        self.save()
        self.avatar = f"/media/user/{UserSetting.encryptUserId(self.user.id)}/{self.public_key}/avatar"
        file_manager.saveUserAvatar(content)
    
    @staticmethod
    def encryptUserId(userId) -> int:
        return (userId * 347983247) ^ 320392843
    
    @staticmethod
    def decryptUserId(token) -> int:
        return (token ^ 320392843) // 347983247

from random import random

def context_processors_user_setting(request):
    return {
        
    }

class UserProblemStatisticsModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    totalSubmission = models.IntegerField(default=0)
    solvedCount = models.IntegerField(default=0)
    waCount = models.IntegerField(default=0)
    tleCount = models.IntegerField(default=0)
    rteCount = models.IntegerField(default=0)
    mleCount = models.IntegerField(default=0)
    ceCount = models.IntegerField(default=0)

    @staticmethod
    def createStatIfNotExists(user:User):
        setting_filter = UserProblemStatisticsModel.objects.filter(user=user)
        if not setting_filter.exists():
            new_setting = UserProblemStatisticsModel.objects.create(user=user)
            new_setting.save()

    @staticmethod
    def getStat(user:User):
        setting_filter = UserProblemStatisticsModel.objects.filter(user=user)
        if not setting_filter.exists():
            return UserProblemStatisticsModel.createStatIfNotExists(user)
        return setting_filter[0]
    
    def __str__(self) -> str:
        return self.user.username + ' ----- '  + ' -> total = ' + str(self.solvedCount)


class ImportUserFileModel(models.Model):
    name = models.CharField(max_length=512, unique=True)
    token = models.CharField(max_length=4096)

    @staticmethod
    def EncryptId(id:int) -> int:
        return (id * 347329) ^ 123456
    
    @staticmethod
    def DecryptId(token:int) -> int:
        return (token ^ 123456) // 347329
