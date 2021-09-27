from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from backend.models.problem import ProblemModel
from backend.filemanager.filemanager import OverwriteStorage

from django.http import FileResponse, Http404
from django.conf import settings

import os
import cv2

class UserStorage(FileSystemStorage):

    def __init__(self, user:User):
        self.__user_dir = user.usersetting.hash_user_profile
        super().__init__(settings.USER_ROOT)
    
    def saveUserAvatar(self, content:ContentFile):
        self.save(os.path.join(self.__user_dir, 'avatar.png'), content)
    
    def loadUserAvatar(self):
        if self.exists(os.path.join(self.__user_dir, 'avatar.png')):
            return FileResponse(self.open(os.path.join(self.__user_dir, 'avatar.png')), content_type='image/ief')
        return FileResponse('')

    # OVERRIDE FROM BASE CLASS
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.USER_ROOT, name))
        return name
