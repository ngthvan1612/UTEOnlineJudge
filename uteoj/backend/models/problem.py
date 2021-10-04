from django.http.request import MediaType
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

    @staticmethod
    def getAcceptValue():
        return ['easy', 'medium', 'hard']

    @staticmethod
    def getModeName(mode):
        build = {
            ProblemDifficultType.Easy: "easy",
            ProblemDifficultType.Medium: "medium",
            ProblemDifficultType.Hard: "hard"
        }
        return build[mode]
    
    @staticmethod
    def getValueFromName(name):
        build = {
            "easy": ProblemDifficultType.Easy,
            "medium": ProblemDifficultType.Medium,
            "hard": ProblemDifficultType.Hard
        }

        return build[name]

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

    @staticmethod
    def getAcceptValue():
        return ['AllowFromAll', 'OnlySolved', 'OnlyMe']

    @staticmethod
    def getModeName(mode):
        build = {
            SubmissionVisibleModeType.AllowedFromAll: "AllowFromAll",
            SubmissionVisibleModeType.OnlySolved: "OnlySolved",
            SubmissionVisibleModeType.OnlyMe: "OnlyMe",
        }
        return build[mode]
    
    @staticmethod
    def getValueFromName(name):
        build = {
            "AllowFromAll": SubmissionVisibleModeType.AllowedFromAll,
            "OnlySolved": SubmissionVisibleModeType.OnlySolved,
            "OnlyMe": SubmissionVisibleModeType.OnlyMe,
        }

        return build[name]


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

    is_public = models.BooleanField(default=False)

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
    def CreateNewProblem(shortname:str, fullname:str, first_author:User, default_setting:dict) -> None:
        problem = ProblemModel.objects.create(shortname = shortname,fullname = fullname, author=first_author)
        problem.hash_problem = str(uuid.uuid4().hex) + '_' + shortname

        # setting
        problem.statement = ""

        # grader
        problem.input_filename = shortname.upper() + '.INP'
        problem.output_filename = shortname.upper() + '.OUT'

        # default
        if default_setting:
            problem.is_public = default_setting['is_public']
            problem.problem_type = default_setting['problem_type']
            problem.time_limit = default_setting['time_limit']
            problem.memory_limit = default_setting['memory_limit']
            problem.submission_visible_mode = default_setting['submission_visible_mode']
            problem.difficult = default_setting['difficult']
            problem.points_per_test = default_setting['points_per_test']

        problem.save()

        return problem
    
    def getSetting(self):
        return {
            'is_public': self.is_public,
            'problem_type': self.problem_type,
            'time_limit': self.time_limit,
            'memory_limit': self.memory_limit,
            'submission_visible_mode': self.submission_visible_mode,
            'difficult': self.difficult,
            'points_per_test': self.points_per_test
        }


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

