from re import S
from django.db import models
from django.contrib.auth.models import User
from django.db.models.query_utils import check_rel_lookup_compatibility


class ProblemCategoryModel(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class ProblemType:
    ACM = 0
    OI = 1

def context_processors_problem_type(request):
    return {
        'PROBLEM_TYPE': {
            'ACM': ProblemType.ACM,
            'OI': ProblemType.OI,
        },
    }

class SubmissionVisibleModeType:
    AllowedFromAll = 0
    OnlySolved = 1
    OnlyMe = 2


PROBLEM_TYPE_CHOICES = (
    (ProblemType.ACM, "ACM"),
    (ProblemType.OI, "OI"),
)


SUBMISSION_VISIBLE_MODE_CHOICES = (
    (SubmissionVisibleModeType.AllowedFromAll, "Ai cũng có thể xem được"),
    (SubmissionVisibleModeType.OnlySolved, "Chỉ những người giải được"),
    (SubmissionVisibleModeType.OnlyMe, "Chỉ mình tôi"),
)


import django
import uuid


class ProblemModel(models.Model):
    author = models.ManyToManyField(User,blank=False)

    publish_date = models.DateTimeField(blank=False, default=django.utils.timezone.now)

    categories = models.ManyToManyField(ProblemCategoryModel, blank=True)

    shortname = models.CharField(max_length=32, unique=True)
    fullname = models.CharField(max_length=255)

    problem_type = models.IntegerField(default=0, choices=PROBLEM_TYPE_CHOICES)

    difficult = models.FloatField(default=5.0)

    hash_problem = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.shortname + ' - ' + self.fullname

    @staticmethod
    def CreateNewProblem(shortname:str, fullname:str, first_author:User) -> None:
        problem = ProblemModel.objects.create(shortname = shortname,fullname = fullname,)
        problem.author.set([first_author.id])
        problem.hash_problem = str(uuid.uuid4().hex) + '_' + shortname
        problem.save()

        #setting
        problem_setting = ProblemSettingModel.objects.create(problem=problem)
        problem_setting.statement = "Cho 3 số nguyên a, b, c ($-1000\le a,b,c \le 1000$). Xác định xem phương trinh $ax^2 + bx + c = 0$ có nghiệm trên tập $\mathbb{R}$ hay không và in ra màn hình nếu có."
        problem_setting.input_statement = "Gồm 1 dòng 3 số nguyên $a, b, c$ cách nhau ít nhất một khoảng trắng."
        problem_setting.output_statement = 'Nếu phương trình vô nghiệm chỉ cần in ra 1 dòng "NO SOLUTION" (không có ngoặc kép).'
        problem_setting.constraints_statement = "$-1000\le a,b,c \le 1000$"
        problem_setting.save()

        #Grader
        problem_grader = ProblemGraderModel.objects.create(problem=problem)
        problem_grader.input_filename = shortname.upper() + '.INP'
        problem_grader.output_filename = shortname.upper() + '.OUT'
        problem_grader.save()

        #Statistics
        problem_statistics = ProblemStatisticsModel.objects.create(problem=problem)
        problem_statistics.save()

        return problem


class ProblemSettingModel(models.Model):
    problem = models.OneToOneField(ProblemModel, on_delete=models.CASCADE)
    points_per_test = models.FloatField(default=1.0)

    statement = models.TextField(blank=False)
    input_statement = models.TextField(blank=False, null=True)
    output_statement = models.TextField(blank=False, null=True)
    constraints_statement = models.TextField(blank=False, null=True)

    submission_visible_mode = models.IntegerField(default=0, choices=SUBMISSION_VISIBLE_MODE_CHOICES)

    def __str__(self) -> str:
        return self.problem.shortname + ' settings'


class ProblemGraderModel(models.Model):
    problem = models.OneToOneField(ProblemModel, on_delete=models.CASCADE)

    input_filename = models.CharField(max_length=32)
    output_filename = models.CharField(max_length=32)
    use_stdin = models.BooleanField(default=True)
    use_stdout = models.BooleanField(default=True)

    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=65536)

    use_checker = models.BooleanField(default=False)
    checker = models.TextField(blank=True,default='')

    def __str__(self) -> str:
        return self.problem.shortname + ' graders'


class ProblemStatisticsModel(models.Model):
    problem = models.OneToOneField(ProblemModel, on_delete=models.CASCADE)
    solvedCount = models.IntegerField(default=0)
    totalSubmission = models.IntegerField(default=0)
    waCount = models.IntegerField(default=0)
    tleCount = models.IntegerField(default=0)
    rteCount = models.IntegerField(default=0)
    mleCount = models.IntegerField(default=0)
    ceCount = models.IntegerField(default=0)

    def __str__(self):
        return self.problem.shortname + ' ' + str(self.solvedCount)


class ProblemTestCaseModel(models.Model):
    problem = models.ForeignKey(ProblemModel, on_delete=models.CASCADE)
    tag = models.CharField(max_length=255, blank=True, null=True)
    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=65536)
    points = models.FloatField(default=1.0)
    name = models.CharField(null=True, max_length=255)

    is_sample = models.BooleanField(default=False)

    input_file = models.CharField(max_length=255, blank=False, null=True)
    output_file = models.CharField(max_length=255, blank=False, null=True)

    def __str__(self):
        return str(self.id) + ' - ' + self.problem.shortname

