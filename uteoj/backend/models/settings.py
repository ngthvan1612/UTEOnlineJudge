from django.db import models

SUPPORT_EMAIL_HANDLE_SETTING_NAME = 'support.email.handle'
SUPPORT_EMAIL_PASSWORD_SETTING_NAME = 'support.email.password'

CHANGE_PASSWORD_EMAIL_HANDLE_SETTING_NAME = 'changepassword.email.handle'
CHANGE_PASSWORD_EMAIL_PASSWORD_SETTING_NAME = 'changepassword.email.password'

class OJSettingModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    value = models.TextField()

    def __str__(self):
        return self.name

    @staticmethod 
    def get(setting_name):
        if OJSettingModel.objects.filter(name=setting_name).exists() == False:
            OJSettingModel.objects.create(name=setting_name, value='').save()
        return OJSettingModel.objects.get(name=setting_name)
    
    @staticmethod
    def set(setting_name, value):
        if OJSettingModel.objects.filter(name=setting_name).exists() == False:
            OJSettingModel.objects.create(name=setting_name, value='').save()
        entry = OJSettingModel.objects.get(name=setting_name)
        entry.value = value
        entry.save()

    @staticmethod
    def getSTMPServer():
        return OJSettingModel.get('stmp.server').value
    
    @staticmethod
    def setSTMPServer(server):
        OJSettingModel.set('stmp.server', server)
    
    @staticmethod
    def getSTMPEmail():
        return OJSettingModel.get('stmp.email').value
    
    @staticmethod
    def setSTMPEmail(email):
        OJSettingModel.set('stmp.email', email)
    
    @staticmethod
    def getSTMPPort():
        return OJSettingModel.get('stmp.port').value
    
    @staticmethod
    def setSTMPPort(port):
        OJSettingModel.set('stmp.port', port)

    @staticmethod
    def getSTMPPassword():
        return OJSettingModel.get('stmp.password').value
    
    @staticmethod
    def setSTMPPassword(password):
        OJSettingModel.set('stmp.password', password)
    
    @staticmethod
    def getSTMPEnableTLS():
        return OJSettingModel.get('stmp.tls')
    
    @staticmethod
    def setSTMPEnableTLS(tls):
        OJSettingModel.set('stmp.tls', tls)

    @staticmethod
    def getAllowRegister():
        return OJSettingModel.get('account.allow_register')
    
    @staticmethod
    def setAllowRegister(value):
        OJSettingModel.set('account.allow_register', value)

