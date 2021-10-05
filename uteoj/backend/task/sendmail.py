from backend.models.settings import OJSettingModel
from celery.decorators import task
from django.contrib.auth.models import User
from django.utils import timezone
import time
import uuid
from judger.grader import *
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

@task(name="SendMail")
def SendMail(subject, email, user_email):
    settings.EMAIL_HOST_USER = OJSettingModel.getSTMPEmail()
    settings.EMAIL_HOST_PASSWORD = OJSettingModel.getSTMPPassword()
    settings.EMAIL_USE_TLS = OJSettingModel.getSTMPEnableTLS()
    settings.EMAIL_HOST = OJSettingModel.getSTMPServer()
    settings.EMAIL_PORT = OJSettingModel.getSTMPPort()
    send_mail(subject, email, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)
    print(f"Gửi mail cho {user_email} xong!")

