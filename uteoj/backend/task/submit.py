from backend.models.language import LanguageModel
from datetime import datetime
from backend.models.usersetting import UserProblemStatisticsModel
from backend.models.problem import ProblemModel, ProblemStatisticsModel, ProblemType
from celery.decorators import task
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from backend.models.submission import SubmissionModel, SubmissionResultType, SubmissionStatusType, SubmissionTestcaseResultModel
from random import randint, random
from django.utils import timezone
import time
import uuid
from judger.judger import Compile
from django.db import transaction

logger = get_task_logger(__name__)

def rnd(upper_bound:int) -> int:
    tmp = str(uuid.uuid4().hex)
    result = 0
    for z in tmp:
        result = (result * 16 + ord(z)) % upper_bound
    return result

@task(name='random_submission')
def RandomSubmission(count) -> None:
    #list all user
    #list all problem
    list_all_user = User.objects.all()
    list_all_problem = ProblemModel.objects.all()
    list_all_language = LanguageModel.objects.all()
    cnt_user = len(list_all_user)
    cnt_problem = len(list_all_problem)
    cnt_language = len(list_all_language)

    for i in range(0, count, 1):
        random_user = list_all_user[randint(1, cnt_user) - 1]
        random_problem = list_all_problem[randint(1, cnt_problem) - 1]
        random_language = list_all_language[randint(1, cnt_language) - 1]
        submission = SubmissionModel.objects.create(
            user=random_user,
            problem=random_problem,
            submission_date=timezone.localtime(timezone.now()),
            source_code = "gi do random",
            language=random_language)
        submission.status = SubmissionStatusType.InQueued
        submission.save()
        SubmitSolution.delay(submission.id, False)

@task(name="submit_solution")
def SubmitSolution(submission_id:int, allow_sleep=True) -> None:
    submission = SubmissionModel.objects.get(pk=submission_id)
    problem = submission.problem
    user = submission.user
    language = submission.language

    #Update
    with transaction.atomic():
        problemStatisticsEntries = ProblemStatisticsModel.objects.select_for_update().filter(problem=problem)
        for problemStatistics in problemStatisticsEntries:
            problemStatistics.totalSubmission = problemStatistics.totalSubmission + 1
            problemStatistics.save()
    
    with transaction.atomic():
        UserProblemStatisticsModel.createStatIfNotExists(user, problem=problem)
        userStatisticEntries = UserProblemStatisticsModel.objects.select_for_update().filter(user=user, problem=problem)
        for stat in userStatisticEntries:
            stat.totalSubmission = stat.totalSubmission + 1
            stat.save()

    #starting
    #print('Đang chấm bài tập {} của {}, ngon ngu: {}'.format(problem.fullname, user.username, language.name))
    logger.info('Đang chấm bài tập {} của {}, ngon ngu: {}, id = {}'.format(problem.fullname, user.username, language.name, submission))
    submission.submission_judge_date = timezone.localtime(timezone.now())

    #begin compile
    # Compile(submission=submission)
    submission.status = SubmissionStatusType.Compiling
    submission.save()

    if allow_sleep:
        time.sleep(5)

    #endcompile
    if rnd(5) == 1:
        #compile error
        with transaction.atomic():
            UserProblemStatisticsModel.createStatIfNotExists(user, problem=problem)
            userStatisticEntries = UserProblemStatisticsModel.objects.select_for_update().filter(user=user, problem=problem)
            for stat in userStatisticEntries:
                stat.ceCount = stat.ceCount + 1
                stat.save()
        with transaction.atomic():
            problemStatisticsEntries = ProblemStatisticsModel.objects.select_for_update().filter(problem=problem)
            for problemStatistics in problemStatisticsEntries:
                problemStatistics.ceCount = problemStatistics.ceCount + 1
                problemStatistics.save()
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
                SubmissionTestcaseResultModel.objects.create(submission=submission, executed_time=randint(0, 999), memory_usage=randint(0, 999), points=random() * 9, result=SubmissionResultType.WA).save()
                submission.result = SubmissionResultType.WA
                with transaction.atomic():
                    UserProblemStatisticsModel.createStatIfNotExists(user, problem=problem)
                    userStatisticEntries = UserProblemStatisticsModel.objects.select_for_update().filter(user=user, problem=problem)
                    for stat in userStatisticEntries:
                        stat.waCount = stat.waCount + 1
                        stat.save()
                with transaction.atomic():
                    problemStatisticsEntries = ProblemStatisticsModel.objects.select_for_update().filter(problem=problem)
                    for problemStatistics in problemStatisticsEntries:
                        problemStatistics.waCount = problemStatistics.waCount + 1
                        problemStatistics.save()
            elif random_result == 2:
                SubmissionTestcaseResultModel.objects.create(submission=submission, executed_time=randint(0, 999), memory_usage=randint(0, 999), points=random() * 9, result=SubmissionResultType.TLE).save()
                submission.result = SubmissionResultType.TLE
                with transaction.atomic():
                    UserProblemStatisticsModel.createStatIfNotExists(user, problem=problem)
                    userStatisticEntries = UserProblemStatisticsModel.objects.select_for_update().filter(user=user, problem=problem)
                    for stat in userStatisticEntries:
                        stat.tleCount = stat.tleCount + 1
                        stat.save()
                with transaction.atomic():
                    problemStatisticsEntries = ProblemStatisticsModel.objects.select_for_update().filter(problem=problem)
                    for problemStatistics in problemStatisticsEntries:
                        problemStatistics.tleCount = problemStatistics.tleCount + 1
                        problemStatistics.save()
            elif random_result == 3:
                SubmissionTestcaseResultModel.objects.create(submission=submission, executed_time=randint(0, 999), memory_usage=randint(0, 999), points=random() * 9, result=SubmissionResultType.MLE).save()
                submission.result = SubmissionResultType.MLE
                with transaction.atomic():
                    UserProblemStatisticsModel.createStatIfNotExists(user, problem=problem)
                    userStatisticEntries = UserProblemStatisticsModel.objects.select_for_update().filter(user=user, problem=problem)
                    for stat in userStatisticEntries:
                        stat.mleCount = stat.mleCount + 1
                        stat.save()
                with transaction.atomic():
                    problemStatisticsEntries = ProblemStatisticsModel.objects.select_for_update().filter(problem=problem)
                    for problemStatistics in problemStatisticsEntries:
                        problemStatistics.mleCount = problemStatistics.mleCount + 1
                        problemStatistics.save()
            else:
                SubmissionTestcaseResultModel.objects.create(submission=submission, executed_time=randint(0, 999), memory_usage=randint(0, 999), points=random() * 9, result=SubmissionResultType.RTE).save()
                submission.result = SubmissionResultType.RTE
                with transaction.atomic():
                    UserProblemStatisticsModel.createStatIfNotExists(user, problem=problem)
                    userStatisticEntries = UserProblemStatisticsModel.objects.select_for_update().filter(user=user, problem=problem)
                    for stat in userStatisticEntries:
                        stat.rteCount = stat.rteCount + 1
                        stat.save()
                with transaction.atomic():
                    problemStatisticsEntries = ProblemStatisticsModel.objects.select_for_update().filter(problem=problem)
                    for problemStatistics in problemStatisticsEntries:
                        problemStatistics.rteCount = problemStatistics.rteCount + 1
                        problemStatistics.save()

            if submission.problem.problem_type == ProblemType.ACM:
                stopped = True
                submission.status = SubmissionStatusType.Completed
                submission.save()
                break
        else:
            SubmissionTestcaseResultModel.objects.create(submission=submission, executed_time=randint(0, 999), memory_usage=randint(0, 999), points=random() * 9, result=SubmissionResultType.AC).save()
        submission.save()

        if allow_sleep:
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
        UserProblemStatisticsModel.createStatIfNotExists(user, problem=problem)
        userStatisticEntries = UserProblemStatisticsModel.objects.select_for_update().filter(user=user, problem=problem)
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
    


