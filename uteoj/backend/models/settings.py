import json
from django.db import models

from backend.models.problem import ProblemDifficultType, ProblemModel, ProblemType, SubmissionVisibleModeType

SUPPORT_EMAIL_HANDLE_SETTING_NAME = 'support.email.handle'
SUPPORT_EMAIL_PASSWORD_SETTING_NAME = 'support.email.password'

CHANGE_PASSWORD_EMAIL_HANDLE_SETTING_NAME = 'changepassword.email.handle'
CHANGE_PASSWORD_EMAIL_PASSWORD_SETTING_NAME = 'changepassword.email.password'

class OJSettingModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    value = models.TextField()

    def __str__(self):
        return self.name + ' = ' + self.value

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
    def getSTMPServer() -> str:
        return OJSettingModel.get('stmp.server').value
    
    @staticmethod
    def setSTMPServer(server):
        OJSettingModel.set('stmp.server', server)
    
    @staticmethod
    def getSTMPEmail() -> str:
        return OJSettingModel.get('stmp.email').value
    
    @staticmethod
    def setSTMPEmail(email) -> str:
        OJSettingModel.set('stmp.email', email)
    
    @staticmethod
    def getSTMPPort() -> str:
        tmp = OJSettingModel.get('stmp.port').value
        return tmp
    
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
    def getSTMPEnableTLS() -> bool:
        tmp = OJSettingModel.get('stmp.tls').value
        return tmp == 'True'
    
    @staticmethod
    def setSTMPEnableTLS(tls):
        OJSettingModel.set('stmp.tls', tls)

    @staticmethod
    def getAllowRegister() -> bool:
        tmp = OJSettingModel.get('account.allow_register').value
        return tmp == 'True'
    
    @staticmethod
    def setAllowRegister(value):
        OJSettingModel.set('account.allow_register', value)

    @staticmethod
    def getAllowSubmission() -> bool:
        tmp = OJSettingModel.get('submission.allow_submission').value
        return tmp == 'True'
    
    @staticmethod
    def setAllowSubmission(value):
        OJSettingModel.set('submission.allow_submission', value)
    
    @staticmethod
    def setDefaultProblemConfig(data):
        OJSettingModel.set('problem.defaultconfig', json.dumps(data))
    
    @staticmethod
    def getDefaultProblemConfig():
        try:
            data = json.loads(OJSettingModel.get('problem.defaultconfig').value)
            return data
        except Exception as e:
            return {
                'is_public': False,
                'problem_type': ProblemType.OI,
                'time_limit': 1000,
                'memory_limit': 65536,
                'submission_visible_mode': SubmissionVisibleModeType.OnlySolved,
                'difficult': ProblemDifficultType.Medium,
                'points_per_test': 1.0
            }