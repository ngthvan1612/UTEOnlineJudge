from datetime import datetime
from backend.models.usersetting import UserStatisticsModel
from backend.models.problem import ProblemStatisticsModel
from celery.decorators import task
from django.contrib.auth.models import User
from backend.models.submission import SubmissionModel, SubmissionResultType, SubmissionStatusType
from random import randint, random
from django.utils import timezone
import time
import uuid
from judger.judger import Compile
from django.db import transaction

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

    #Update
    with transaction.atomic():
        problemStatisticsEntries = ProblemStatisticsModel.objects.select_for_update().filter(problem=problem)
        for problemStatistics in problemStatisticsEntries:
            problemStatistics.submitCount = problemStatistics.submitCount + 1
            problemStatistics.save()
    
    with transaction.atomic():
        UserStatisticsModel.createStatIfNotExists(user)
        userStatisticEntries = UserStatisticsModel.objects.select_for_update().filter(user=user)
        for stat in userStatisticEntries:
            stat.totalSubmission = stat.totalSubmission + 1
            stat.save()

    #starting
    print('Đang chấm bài tập {} của {}, ngon ngu: {}'.format(problem.fullname, user.username, language.name))
    submission.submission_judge_date = timezone.localtime(timezone.now())

    #begin compile
    # Compile(submission=submission)
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
                with transaction.atomic():
                    UserStatisticsModel.createStatIfNotExists(user)
                    userStatisticEntries = UserStatisticsModel.objects.select_for_update().filter(user=user)
                    for stat in userStatisticEntries:
                        stat.waCount = stat.waCount + 1
                        stat.save()
            elif random_result == 2:
                submission.result = SubmissionResultType.TLE
                with transaction.atomic():
                    UserStatisticsModel.createStatIfNotExists(user)
                    userStatisticEntries = UserStatisticsModel.objects.select_for_update().filter(user=user)
                    for stat in userStatisticEntries:
                        stat.tleCount = stat.tleCount + 1
                        stat.save()
            elif random_result == 3:
                submission.result = SubmissionResultType.MLE
                with transaction.atomic():
                    UserStatisticsModel.createStatIfNotExists(user)
                    userStatisticEntries = UserStatisticsModel.objects.select_for_update().filter(user=user)
                    for stat in userStatisticEntries:
                        stat.mleCount = stat.mleCount + 1
                        stat.save()
            else:
                submission.result = SubmissionResultType.RTE
                with transaction.atomic():
                    UserStatisticsModel.createStatIfNotExists(user)
                    userStatisticEntries = UserStatisticsModel.objects.select_for_update().filter(user=user)
                    for stat in userStatisticEntries:
                        stat.rteCount = stat.rteCount + 1
                        stat.save()
            stopped = True
            submission.status = SubmissionStatusType.Completed
            submission.save()
            break
        submission.save()
        time.sleep(time_sleep_count)
    
    if stopped:
        submission.executed_time = randint(10, 10000)
        submission.memory_usage = randint(10, 11111111)
        submission.save()
        return

    # Làm đúng
    with transaction.atomic():
        problemStatisticsEntries = ProblemStatisticsModel.objects.select_for_update().filter(problem=problem)
        for problemStatistics in problemStatisticsEntries:
            problemStatistics.solvedCount = problemStatistics.solvedCount + 1
            problemStatistics.save()
    
    with transaction.atomic():
        UserStatisticsModel.createStatIfNotExists(user)
        userStatisticEntries = UserStatisticsModel.objects.select_for_update().filter(user=user)
        for stat in userStatisticEntries:
            stat.solvedCount = stat.solvedCount + 1
            stat.save()

    submission.status = SubmissionStatusType.Completed
    submission.result = SubmissionResultType.AC
    submission.executed_time = randint(10, 10000)
    submission.memory_usage = randint(10, 11111111)
    submission.save()

@task(name="sum_two_numbers")
def add(x, y):
    for i in range(0, x, 1):
        print(y)
    


