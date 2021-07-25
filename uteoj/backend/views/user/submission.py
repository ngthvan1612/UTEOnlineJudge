from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from backend.models.problem import ProblemModel
from backend.models.problem import ProblemCategoryModel
from django.db.models import Q

from datetime import datetime
from random import random
from django.http import HttpResponse
from django.core import serializers


from backend.task.submit import SubmitSolution

