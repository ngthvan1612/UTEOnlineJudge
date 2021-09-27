from abc import ABC, abstractclassmethod
from django.conf import settings

class ScoreAbstract(ABC):
    
    def __init__(self, user, problem) -> None:
        self._user = user
        self._problem = problem
        self._canContinue = True
        self._totalScore = 0.0
        self._result = -9999

    def canContinue(self) -> bool:
        return self._canContinue
    
    def getTotalScore(self) -> float:
        return round(self._totalScore, settings.NUMBER_OF_DECIMAL)

    def getSubmissionResult(self) -> int:
        return self._result
    
    @abstractclassmethod
    def onCompileError(self):
        pass

    @abstractclassmethod
    def onCompleted(self):
        pass
    
    def onWrongAnswer(self):
        pass

    def onTimeLimitExceeded(self):
        pass

    def onMemoryLimitExceeded(self):
        pass

    def onRunTimeError(self):
        pass

    def onSystemError(self):
        raise Exception('SYSTEM ERROR')
    
    def onAccept(self, score):
        pass

