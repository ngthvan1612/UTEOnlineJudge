from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from backend.models.filemanager import OverwriteStorage

import uuid
import os


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
        return settings.MEDIA_URL + 'usermedia/' + self.avatar

    def uploadAvatar(self, file_name_with_ext, content) -> None:
        file_manager = OverwriteStorage()
        #file path = usermedia/hash_profile/avatar_with_ext
        self.avatar = self.hash_user_profile + '/avatar' + os.path.splitext(file_name_with_ext)[1]
        path = 'usermedia/' + self.avatar
        self.save()
        file_manager.save(path, content)


