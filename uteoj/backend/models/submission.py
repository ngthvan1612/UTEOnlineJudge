from django.db import models
from django.contrib.auth.models import User
from backend.models.problem import ProblemModel
from backend.models.language import LanguageModel


class SubmissionResultType:
    AC = 0
    WA = 1
    TLE = 2
    MLE = 3
    RTE = 4
    OLE = 5
    PE = 6
    CE = 7

class SubmissionStatusType:
    InQueued = 0
    Compiling = 1
    Grading = 2
    Completed = 3

SUBMISSION_RESULT_CHOICES = (
    (SubmissionResultType.CE, 'Dịch lỗi'),
    (SubmissionResultType.AC, 'Được chấp nhận'),
    (SubmissionResultType.WA, 'Kết quả sai'),
    (SubmissionResultType.TLE, 'Chạy quá thời gian'),

    (SubmissionResultType.MLE, 'Vượt quá bộ nhớ'),
    (SubmissionResultType.RTE, 'Lỗi thực thi'),
    (SubmissionResultType.OLE, 'Output Limit Exceed'),
    (SubmissionResultType.PE, 'Presentation Error'),
)

SUBMISSION_STATUS_CHOICES = (
    (SubmissionStatusType.InQueued, 'Đang đợi'),
    (SubmissionStatusType.Compiling, 'Đang biên dịch'),
    (SubmissionStatusType.Grading, 'Đang chấm'),
    (SubmissionStatusType.Completed, 'Chấm xong'),
)

class SubmissionModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(ProblemModel, on_delete=models.CASCADE)
    source_code =models.TextField()

    #Cập nhật lúc nộp bài lên server (không thể không có)
    submission_date = models.DateTimeField(blank=False)
    language = models.ForeignKey(LanguageModel, on_delete=models.SET_NULL, null=True,blank=True)

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

    #Số hiệu test cuối cùng bị sai
    lastest_test = models.IntegerField(null=True, blank=True)

    def __str__(self):
        result_str = self.get_result_display() if self.get_result_display() is not None else ''
        rtest = str(self.lastest_test) if self.lastest_test is not None else 'Đang đợi chấm...'
        if self.result == SubmissionResultType.CE:
            return '{}.{} -> {} --------------------> {}'.format(self.user.username, self.problem.shortname, self.get_status_display(), result_str)
        if self.status != SubmissionStatusType.Completed:
            return '{}.{} -> {} [{}] {}'.format(self.user.username, self.problem.shortname, self.get_status_display(), rtest, result_str)
        else:
            if self.result == SubmissionResultType.AC:
                return '{}.{} -> {} --------------------> {}'.format(self.user.username, self.problem.shortname, self.get_status_display(), result_str)
            else:
                
                return '{}.{} -> {} --------------------> {} test {}'.format(self.user.username, self.problem.shortname, self.get_status_display(), result_str, rtest)

class SubmissionTestcaseResultModel(models.Model):
    submission = models.ForeignKey(SubmissionModel, on_delete=models.CASCADE)
    executed_time = models.IntegerField(blank=False)
    memory_usage = models.IntegerField(blank=False)
    points = models.FloatField(blank=False)
    checker_message = models.TextField(blank=True)

    def __str__(self):
        return str(self.submission) + ' ' + str(self.points)

