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

class ProblemModel(models.Model):
    author = models.ManyToManyField(User, blank=False)
    publish_date = models.DateTimeField(blank=False, default=django.utils.timezone.now)
    categories = models.ManyToManyField(ProblemCategoryModel, blank=True)
    categories_str = models.CharField(blank=True, null=True, max_length=2048)
    shortname = models.CharField(max_length=32, unique=True)
    fullname = models.CharField(max_length=255)
    difficult = models.FloatField(default=5.0)
    points_per_test = models.FloatField(default=1.0)
    statement = models.TextField(blank=False)
    input_statement = models.TextField(blank=False, null=True)
    output_statement = models.TextField(blank=False, null=True)
    constraints_statement = models.TextField(blank=False, null=True)

    input_filename = models.CharField(max_length=32)
    output_filename = models.CharField(max_length=32)
    use_stdin = models.BooleanField(default=True)
    use_stdout = models.BooleanField(default=True)

    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=65536)

    use_checker = models.BooleanField(default=False)
    checker = models.TextField(blank=True,null=True)
    problem_type = models.IntegerField(default=0, choices=PROBLEM_TYPE_CHOICES)
    submission_visible_mode = models.IntegerField(default=0, choices=SUBMISSION_VISIBLE_MODE_CHOICES)

    def __str__(self):
        return self.shortname + ' - ' + self.fullname

    def set_categories(self, lc):
        self.categories.set(lc)
        tmp = [str(x.id) for x in self.categories.all()]
        self.categories_str = ','.join(tmp)


class ProblemStatisticsModel(models.Model):
    problem = models.OneToOneField(ProblemModel, on_delete=models.CASCADE)
    solvedCount = models.IntegerField(default=0, blank=False)

    def __str__(self):
        return self.problem.shortname + ' ' + str(self.solvedCount)


class ProblemTestCaseModel(models.Model):
    problem = models.ForeignKey(ProblemModel, on_delete=models.CASCADE)
    tag = models.CharField(max_length=255, blank=True, null=True)
    time_limit = models.IntegerField(default=1000)
    memory_limit = models.IntegerField(default=65536)
    points = models.FloatField(default=1.0)

    input_file = models.CharField(max_length=255, blank=False, null=True)
    output_file = models.CharField(max_length=255, blank=False, null=True)

    def __str__(self):
        return str(self.id) + ' - ' + self.problem.shortname
