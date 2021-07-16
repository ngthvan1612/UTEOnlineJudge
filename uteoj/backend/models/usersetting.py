from django.db import models
from django.contrib.auth.models import User

from backend.models.filemanager import UserFileManager

class UserSetting(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=255, blank=True)
    job = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username


