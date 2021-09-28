from django.contrib.auth.decorators import user_passes_test
from django.core.files.base import ContentFile
from django.http.response import FileResponse
from backend.filemanager.userstorage import UserStorage
from django.utils.translation import npgettext
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from datetime import datetime
from django.utils.timezone import get_current_timezone, utc
from django.test import override_settings
from django.utils.timezone import make_aware
from django.utils import timezone


class ContestType:
    ACM = 0
    OI = 1

CONTEST_TYPE_CHOICES = (
    (ContestType.ACM, "ACM"),
    (ContestType.OI, "OI"),
)

class ContestModel(models.Model):
    title = models.CharField(max_length=2048)
    description = models.TextField()
    startTime = models.DateTimeField()
    endTime = models.DateTimeField()
    contestants = models.ManyToManyField(User)

    @staticmethod
    def prepareData(title, startTime, endTime):
        if title is None or len(title) == 0:
            return (False, None, None, None, 'Tên kỳ thi không được trống')

        try:
            _tmp = datetime.strptime(startTime, '%Y-%m-%dT%H:%M')
            _startTime = timezone.localtime(timezone.now()).replace(year=_tmp.year, month=_tmp.month, day=_tmp.day, hour=_tmp.hour, minute=_tmp.minute, second=0)
        except:
            return (False, None, None, None, 'Ngày bắt đầu không đúng định dạng, hoặc ngày này không có')
        
        try:
            _tmp = datetime.strptime(endTime, '%Y-%m-%dT%H:%M')
            _endTime = timezone.localtime(timezone.now()).replace(year=_tmp.year, month=_tmp.month, day=_tmp.day, hour=_tmp.hour, minute=_tmp.minute, second=0)
        except:
            return (False, None, None, None, 'Ngày kết thúc không đúng định dạng, hoặc ngày này không có')
        
        if (_startTime > _endTime):
            return (False, None, None, None, 'Ngày bắt đầu phải <= ngày kết thúc')
        
        return (True, title, _startTime, _endTime, '')

    @staticmethod
    def createContest(title:str, desc:str, startTime:str, endTime:str):
        
        contest = ContestModel.objects.create(
            title=title,
            description=desc,
            startTime=startTime,
            endTime=endTime,
        )

        contest.save()

        return (True, 'Tạo thành công', contest)

    def addProblem(self, problem):
        if problem in self.problem_set.all():
            return (False, 'Bài tập này đã có trong kỳ thi')
        
        self.problem_set.add(problem)
        
        return (True, 'Thêm thành công')

    def removeProblem(self, problem):
        if not (problem in self.problemmodel_set.all()):
            return (False, 'Bài tập này không có trong kỳ thi')
        
        self.problemmodel_set.remove(problem)
        
        return (True, 'Xóa thành công')
    
    def addListContestant(self, list_contestants:User):
        self.contestants.add(list_contestants)
