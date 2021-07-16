from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import default_storage

import uuid

from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        """Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Found at http://djangosnippets.org/snippets/976/

        This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):

        def save(self, *args, **kwargs):
            try:
                this = MyModelName.objects.get(id=self.id)
                if this.MyImageFieldName != self.MyImageFieldName:
                    this.MyImageFieldName.delete()
            except: pass
            super(MyModelName, self).save(*args, **kwargs)
        """
        # If the filename already exists, remove it as if it was a true file system
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name

class UserFileManager(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username + '/' + self.file_name

    def getFullPath(self):
        return 'usermedia/' + str(self.user.username) + '/' + self.file_name

    @staticmethod
    def deleteUserFile(user):
        for x in UserFileManager.objects.filter(user=user):
            default_storage.delete(x.getFullPath())

    @staticmethod
    def uploadFile(user, file_name, extension, content, uniqueFileNameWithoutExt, encryptFileName):
        en_file_name = file_name + extension
        if encryptFileName == True:
            en_file_name = str(uuid.uuid4().hex) + '_' + file_name + extension
        path = 'usermedia/' + str(user.username) + '/' + en_file_name
        if uniqueFileNameWithoutExt==True:
            list_old_file = UserFileManager.objects.filter(user=user, file_name__contains=file_name)
        else:
            list_old_file = UserFileManager.objects.filter(user=user, file_name__contains=file_name + extension)
        for old_file in list_old_file:
            default_storage.delete(old_file.getFullPath())
        list_old_file.delete()
        UserFileManager.objects.create(user=user, file_name=en_file_name).save()
        default_storage.save(path, content)
    
    @staticmethod
    def getUserAvatar(user):
        avatar = UserFileManager.objects.filter(user=user, file_name__contains='avatar').order_by('-id')
        if avatar.exists():
            return settings.MEDIA_URL + 'usermedia/' + user.username + '/' + avatar[0].file_name
        return None

