from django.db import models

SUPPORT_EMAIL_HANDLE_SETTING_NAME = 'support.email.handle'
SUPPORT_EMAIL_PASSWORD_SETTING_NAME = 'support.email.password'

CHANGE_PASSWORD_EMAIL_HANDLE_SETTING_NAME = 'changepassword.email.handle'
CHANGE_PASSWORD_EMAIL_PASSWORD_SETTING_NAME = 'changepassword.email.password'

class OJSettingModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    value = models.TextField()

    @staticmethod 
    def get(setting_name):
        if OJSettingModel.objects.filter(name=setting_name).exists() == False:
            OJSettingModel.objects.create(name=setting_name, value='')
        return OJSettingModel.objects.get(name=setting_name)

    def __str__(self):
        return self.name