from hashlib import md5
from re import sub
from backend.models.language import LanguageModel
from datetime import datetime
from backend.models.usersetting import UserProblemStatisticsModel
from backend.models.problem import ProblemModel, ProblemType
from celery.decorators import task
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from backend.models.submission import SubmissionModel, SubmissionResultType, SubmissionStatusType, SubmissionTestcaseResultModel
from random import Random, randint, random, shuffle
from django.utils import timezone
import time
import uuid
#from judger.judger import Compile
from django.db import transaction
from django.conf import settings

from judger.grader import *
import inspect
import sys

from termcolor import colored

logger = get_task_logger(__name__)

def RandomShuffleName(id:int):
    tmp = str(id) + '_' + uuid.uuid4().hex
    return tmp

import os

@task(name='submit_solution')
def SubmitSolution(submission_id:int) -> None:
    submission = SubmissionModel.objects.get(pk=submission_id)
    problem = submission.problem
    language = submission.language
    grader = None
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and issubclass(obj, GraderAbstract) and obj is not GraderAbstract:
            if obj._name == language.name:
                #make compile & run directory
                hash = RandomShuffleName(submission.id)
                compile_dir = os.path.join(settings.COMPILE_ROOT, hash)
                run_dir = os.path.join(settings.RUNNING_ROOT, hash)
                os.system('mkdir -p {}'.format(compile_dir))
                os.system('mkdir -p {}'.format(run_dir))
                grader = obj(compile_dir, run_dir)
    if grader == None:
        #SYSTEM ERROR
        raise Exception('SYSTEM ERROR: NOT FOUND LANGUAGE')

    #starting
    #print('Đang chấm bài tập {} của {}, ngon ngu: {}'.format(problem.fullname, user.username, language.name))
    logger.warning(colored('Đang chấm bài tập #{}'.format(submission.id), 'green'))
    submission.submission_judge_date = timezone.localtime(timezone.now())

    #grading ------------------------------------------------
    grader.grading(
        submission_id=submission.id,
        source_code=submission.source_code,
        problem_dir=os.path.join(settings.PROBLEM_ROOT, problem.hash_problem),
        input_file=problem.input_filename,
        output_file=problem.output_filename,
        time_limit=problem.time_limit,
        memory_limit=problem.memory_limit,
        use_stdin=problem.use_stdin,
        use_stdout=problem.use_stdout,
        use_external_checker=problem.use_checker,
        problem_type=problem.problem_type)

    # erase disk
    try:
        # remove compile dir
        os.system('rm -rf {}'.format(os.path.join(settings.COMPILE_ROOT, hash)))

        # remove run dir
        os.system('rm -rf {}'.format(os.path.join(settings.RUNNING_ROOT, hash)))
    except: pass
    logger.warning(colored('Chấm xong bài tập #{}'.format(submission.id), 'red'))

