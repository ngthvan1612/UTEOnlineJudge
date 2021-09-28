from backend.models.contest import ContestModel
from django.db import models
from django.contrib.auth.models import User
from django.db.models.query_utils import check_rel_lookup_compatibility
from rest_framework import serializers


class ProblemCategoryModel(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class ProblemDifficultType:
    Easy = -10
    Medium = 0
    Hard = 10

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

PROBLEM_DIFFICULT_CHOICES = (
    (ProblemDifficultType.Easy, 'Dễ'),
    (ProblemDifficultType.Medium, 'Trung bình'),
    (ProblemDifficultType.Hard, 'Khó'),
)

SUBMISSION_VISIBLE_MODE_CHOICES = (
    (SubmissionVisibleModeType.AllowedFromAll, "Ai cũng có thể xem được"),
    (SubmissionVisibleModeType.OnlySolved, "Chỉ những người giải được"),
    (SubmissionVisibleModeType.OnlyMe, "Chỉ mình tôi"),
)


import django
import uuid
from django.utils import timezone


class ProblemModel(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, blank=False)

    contest = models.ForeignKey(ContestModel, on_delete=models.CASCADE, blank=True, null=True)

    publish_date = models.DateTimeField(blank=False, default=timezone.localtime(timezone.now()))

    categories = models.ManyToManyField(ProblemCategoryModel, blank=True)

    shortname = models.CharField(max_length=32, unique=True)
    fullname = models.CharField(max_length=255)

    problem_type = models.IntegerField(default=0, choices=PROBLEM_TYPE_CHOICES)

    difficult = models.IntegerField(default=ProblemDifficultType.Easy, choices=PROBLEM_DIFFICULT_CHOICES)

    hash_problem = models.CharField(max_length=255, blank=True)

    points_per_test = models.FloatField(default=1.0)
    total_points = models.FloatField(default=0.0)

    statement = models.CharField(max_length=2048)

    submission_visible_mode = models.IntegerField(default=0, choices=SUBMISSION_VISIBLE_MODE_CHOICES)

    input_filename = models.CharField(max_length=32)
    output_filename = models.CharField(max_length=32)
    use_stdin = models.BooleanField(default=True)
    use_stdout = models.BooleanField(default=True)

    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=65536)

    use_checker = models.BooleanField(default=False)
    checker = models.TextField(blank=True,default='')

    solvedCount = models.IntegerField(default=0)
    totalSubmission = models.IntegerField(default=0)
    waCount = models.IntegerField(default=0)
    tleCount = models.IntegerField(default=0)
    rteCount = models.IntegerField(default=0)
    mleCount = models.IntegerField(default=0)
    ceCount = models.IntegerField(default=0)

    def __str__(self):
        return self.shortname + ' - ' + self.fullname

    @staticmethod
    def CreateNewProblem(shortname:str, fullname:str, first_author:User) -> None:
        problem = ProblemModel.objects.create(shortname = shortname,fullname = fullname, author=first_author)
        problem.hash_problem = str(uuid.uuid4().hex) + '_' + shortname

        #setting
        problem.statement = ""

        #Grader
        problem.input_filename = shortname.upper() + '.INP'
        problem.output_filename = shortname.upper() + '.OUT'

        problem.save()

        return problem


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

