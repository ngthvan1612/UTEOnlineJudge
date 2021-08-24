from datetime import datetime
from celery.decorators import task
from django.contrib.auth.models import User


from backend.models.submission import SubmissionModel, SubmissionResultType, SubmissionStatusType

from random import randint, random

from django.utils import timezone
import time

import uuid

def rnd(upper_bound:int) -> int:
    tmp = str(uuid.uuid4().hex)
    result = 0
    for z in tmp:
        result = (result * 16 + ord(z)) % upper_bound
    return result

@task(name="submit_solution")
def SubmitSolution(submission_id:int) -> None:
    submission = SubmissionModel.objects.get(pk=submission_id)
    problem = submission.problem
    user = submission.user
    language = submission.language

    #starting
    print('Đang chấm bài tập {} của {}, ngon ngu: {}'.format(problem.fullname, user.username, language.name))
    submission.submission_judge_date = datetime.now(tz=timezone.utc)

    #begin compile
    submission.status = SubmissionStatusType.Compiling
    submission.save()
    time.sleep(5)

    #endcompile
    if rnd(5) == 1:
        #compile error
        submission.result = SubmissionResultType.CE
        submission.status = SubmissionStatusType.Completed
        submission.save()
        return

    #grading
    submission.status = SubmissionStatusType.Grading
    num_test = 30
    stopped = False
    time_sleep_count = random()
    for i in range(0, num_test, 1):
        submission.lastest_test = i + 1
        random_can_out = rnd(60)
        if random_can_out == 2:
            random_result = rnd(4) + 1
            if random_result == 1:
                submission.result = SubmissionResultType.WA
            elif random_result == 2:
                submission.result = SubmissionResultType.TLE
            elif random_result == 3:
                submission.result = SubmissionResultType.MLE
            else:
                submission.result = SubmissionResultType.RTE
            stopped = True
            submission.status = SubmissionStatusType.Completed
            submission.save()
            break
        submission.save()
        time.sleep(time_sleep_count)
    
    if stopped:
        return

    #collect result
    submission.status = SubmissionStatusType.Completed
    submission.result = SubmissionResultType.AC
    submission.save()

@task(name="sum_two_numbers")
def add(x, y):
    for i in range(0, x, 1):
        print(y)
    


