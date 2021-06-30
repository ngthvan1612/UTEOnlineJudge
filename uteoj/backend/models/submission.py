from django.db import models
from django.contrib.auth.models import User
from backend.models.problem import ProblemModel
from backend.models.language import LanguageModel


class SubmissionResultType:
    NONE = -2
    CE = -1
    AC = 0
    WA = 1
    TLE = 2
    MLE = 3
    RTE = 4
    OLE = 5
    PE = 6

class SubmissionStatusType:
    NONE = -1
    InQueued = 0
    Compiling = 1
    Grading = 2
    Completed = 3

SUBMISSION_RESULT_CHOICES = (
    (SubmissionResultType.NONE, 'None'),
    (SubmissionResultType.CE, 'Compile error'),
    (SubmissionResultType.AC, 'Accept'),
    (SubmissionResultType.WA, 'Wrong answer'),
    (SubmissionResultType.TLE, 'Time limit exceeded'),

    (SubmissionResultType.MLE, 'memory limit exceeded'),
    (SubmissionResultType.RTE, 'Runtime error'),
    (SubmissionResultType.OLE, 'Output Limit Exceed'),
    (SubmissionResultType.PE, 'Presentation Error'),
)

SUBMISSION_STATUS_CHOICES = (
    (SubmissionStatusType.NONE, 'None'),
    (SubmissionStatusType.InQueued, 'In queued'),
    (SubmissionStatusType.Compiling, 'Compiling'),
    (SubmissionStatusType.Grading, 'Grading'),
    (SubmissionStatusType.Completed, 'Completed'),
)

class SubmissionModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(ProblemModel, on_delete=models.CASCADE)

    #Cập nhật lúc nộp bài lên server (không thể không có)
    submission_date = models.DateTimeField(blank=False)
    language = models.ForeignKey(LanguageModel, on_delete=models.DO_NOTHING)

    #Khi nào lôi bài từ hàng đợi xuống chấm mới cập nhật, mặc định là NULL (chưa chấm)
    submission_judge_date = models.DateTimeField(blank=True, null=True)

    #Biên dịch xong thì cập nhật
    compile_message = models.TextField(blank=True, null=True)

    #Đã chấm xong mới cập nhật thời gian chạy + bộ nhớ
    executed_time = models.IntegerField(blank=True, null=True)
    memory_usage = models.IntegerField(blank=True, null=True)
    points = models.FloatField(blank=True, null=True)

    result = models.IntegerField(choices=SUBMISSION_RESULT_CHOICES, blank=True, null=True)
    status = models.IntegerField(choices=SUBMISSION_STATUS_CHOICES, blank=True, null=True)

    #Số hiệu test cuối cùng bị sai, nếu đúng hết thì coi như -1
    lastest_test = models.IntegerField(default=-1)

    def __str__(self):
        return self.user.username + '.' + self.problem.shortname

class SubmissionTestcaseResultModel(models.Model):
    submission = models.ForeignKey(SubmissionModel, on_delete=models.CASCADE)
    executed_time = models.IntegerField(blank=False)
    memory_usage = models.IntegerField(blank=False)
    points = models.FloatField(blank=False)
    checker_message = models.TextField(blank=True)

    def __str__(self):
        return str(self.submission) + ' ' + str(self.points)

