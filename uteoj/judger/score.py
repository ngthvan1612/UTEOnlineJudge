from django.db import transaction
from backend.models.usersetting import UserProblemStatisticsModel
from backend.models.problem import ProblemStatisticsModel
from backend.models.submission import SubmissionResultType
from judger.scoreabstract import ScoreAbstract

class ACMScore(ScoreAbstract):
    def __init__(self, user, problem) -> None:
        super().__init__(user, problem)
        self._result = SubmissionResultType.AC

    def _check(self):
        if not self._canContinue:
            raise Exception('ACM ICPC SCORE ERROR [canContinue=False but it\'s running!')

    def onCompileError(self):
        self._check()
        self._canContinue = False
        self._result = SubmissionResultType.CE

    def onWrongAnswer(self):
        self._check()
        self._canContinue = False
        self._result = SubmissionResultType.WA

    def onTimeLimitExceeded(self):
        self._check()
        self._canContinue = False
        self._result = SubmissionResultType.TLE

    def onMemoryLimitExceeded(self):
        self._check()
        self._canContinue = False
        self._result = SubmissionResultType.MLE

    def onRunTimeError(self):
        self._check()
        self._canContinue = False
        self._result = SubmissionResultType.RTE

    def onAccept(self, score):
        self._check()
        
    def onCompleted(self):
        with transaction.atomic():
            UserProblemStatisticsModel.createStatIfNotExists(self._user)
            userStatisticEntries = UserProblemStatisticsModel.objects.select_for_update().filter(user=self._user)
            for stat in userStatisticEntries:
                if self._result == SubmissionResultType.AC:
                    stat.solvedCount = stat.solvedCount + 1
                elif self._result == SubmissionResultType.WA:
                    stat.waCount = stat.waCount + 1
                elif self._result == SubmissionResultType.TLE:
                    stat.tleCount = stat.tleCount + 1
                elif self._result == SubmissionResultType.MLE:
                    stat.mleCount = stat.mleCount + 1
                elif self._result == SubmissionResultType.RTE:
                    stat.rteCount = stat.rteCount + 1
                elif self._result == SubmissionResultType.CE:
                    stat.ceCount = stat.ceCount + 1
                else:
                    raise Exception('SYSTEM ERROR')
                stat.save()
        with transaction.atomic():
            problemStatisticsEntries = ProblemStatisticsModel.objects.select_for_update().filter(problem=self._problem)
            print(self._result)
            for problemStatistics in problemStatisticsEntries:
                if self._result == SubmissionResultType.AC:
                    problemStatistics.solvedCount = problemStatistics.solvedCount + 1
                elif self._result == SubmissionResultType.WA:
                    problemStatistics.waCount = problemStatistics.waCount + 1
                elif self._result == SubmissionResultType.TLE:
                    problemStatistics.tleCount = problemStatistics.tleCount + 1
                elif self._result == SubmissionResultType.MLE:
                    problemStatistics.mleCount = problemStatistics.mleCount + 1
                elif self._result == SubmissionResultType.RTE:
                    problemStatistics.rteCount = problemStatistics.rteCount + 1
                elif self._result == SubmissionResultType.CE:
                    problemStatistics.ceCount = problemStatistics.ceCount + 1
                else:
                    raise Exception('SYSTEM ERROR')
                problemStatistics.save()


class OIScore(ScoreAbstract):

    def __init__(self, user, problem) -> None:
        super().__init__(user, problem)
        self._result = SubmissionResultType.AC

    def onCompileError(self):
        self._canContinue = False
        self._result = SubmissionResultType.CE

    def onSYS_ERROR(self):
        raise Exception('SYSTEM ERROR')

    def onAccept(self, score):
        print('up ' + str(score))
        self._totalScore += score

    def onCompleted(self):
        problemScore = self._problem.problemsettingmodel.total_points
        eps = 0.00005
        print('Điểm: {}/{} -> {}'.format(self._totalScore, problemScore, abs(problemScore - self._totalScore) <= eps))

        with transaction.atomic():
            UserProblemStatisticsModel.createStatIfNotExists(self._user)
            userStatisticEntries = UserProblemStatisticsModel.objects.select_for_update().filter(user=self._user)
            for stat in userStatisticEntries:
                if self._result == SubmissionResultType.CE:
                    stat.ceCount = stat.ceCount + 1
                elif abs(problemScore - self._totalScore) <= eps:
                    stat.solvedCount = stat.solvedCount + 1
                else:
                    stat.waCount = stat.waCount + 1
                stat.save()
        
        with transaction.atomic():
            problemStatisticsEntries = ProblemStatisticsModel.objects.select_for_update().filter(problem=self._problem)
            for problemStatistics in problemStatisticsEntries:
                if self._result == SubmissionResultType.CE:
                    problemStatistics.ceCount = problemStatistics.ceCount + 1
                elif abs(problemScore - self._totalScore) <= eps:
                    problemStatistics.solvedCount = problemStatistics.solvedCount + 1
                else:
                    problemStatistics.waCount = problemStatistics.waCount + 1
                problemStatistics.save()


