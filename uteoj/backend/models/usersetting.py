from backend.models.problem import ProblemModel
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from backend.models.filemanager import OverwriteStorage

import uuid
import os
from io import BytesIO
from PIL import Image


class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    hash_user_profile = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True)
    job = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

    @staticmethod
    def createSettingIfNotExists(user:User):
        hash_user_profile = uuid.uuid4().hex + '_' + user.username
        new_setting = UserSetting.objects.create(
            user=user,
            hash_user_profile=hash_user_profile,
            avatar='',
            job='')
        new_setting.save()
        return new_setting

    @staticmethod
    def deleteUserSettingAndFile(user:User) -> None:
        """
        Xóa toàn bộ dữ liệu trong database và file liên quan (avatar)
        """
        file_manager = OverwriteStorage(settings.MEDIA_ROOT)
        setting_filter = UserSetting.objects.filter(user=user)
        for user_setting in setting_filter:
            file_manager.delete(user_setting.avatar)
            user_setting.delete()
    
    @staticmethod
    def getSetting(user:User):
        setting_filter = UserSetting.objects.filter(user=user)
        if not setting_filter.exists():
            return UserSetting.createSettingIfNotExists(user)
        return setting_filter[0]
    
    def getAvatar(self):
        return self.avatar

    def uploadAvatar(self, file_name_with_ext, content) -> None:
        file_manager = OverwriteStorage()
        #file path = usermedia/hash_profile/avatar_with_ext
        self.avatar = settings.MEDIA_URL + 'usermedia/' + self.hash_user_profile + '/avatar' + os.path.splitext(file_name_with_ext)[1]
        path = 'usermedia/' + self.hash_user_profile + '/avatar' + os.path.splitext(file_name_with_ext)[1]
        
        print('save to ' + path)
        self.save()

        # optimize content
        image_file = BytesIO(content.read())
        image = Image.open(image_file)
        image = image.resize((256, 256), Image.ANTIALIAS)
        image = image.convert("RGB")
        image_file = BytesIO()
        image.save(image_file, 'PNG', quality=90)
        # end

        file_manager.save(path, image_file)

def context_processors_user_setting(request):
    if request.user.is_authenticated:
        avatar = UserSetting.getSetting(request.user).avatar
        if avatar is not None and len(avatar) != 0:
            return {
                'user.avatar': UserSetting.getSetting(request.user).avatar
            }
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


