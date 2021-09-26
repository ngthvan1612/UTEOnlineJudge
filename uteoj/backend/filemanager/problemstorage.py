from django.core.files.storage import FileSystemStorage
from backend.models.problem import ProblemModel
from backend.filemanager.filemanager import OverwriteStorage

from django.http import FileResponse, Http404
from django.conf import settings

import os

class ProblemStorage(FileSystemStorage):

    def __init__(self, problem:ProblemModel):
        self.__problem = problem
        self.__problem_dir = problem.hash_problem
        super().__init__(settings.PROBLEM_ROOT)
    
    # STATEMENT

    def __getStatementFilename(self):
        return os.path.join(self.__problem_dir, 'statement.pdf')

    def saveStatement(self, content):
        self.save(self.__getStatementFilename(), content)

    def loadStatement(self):
        return FileResponse(self.open(self.__getStatementFilename()), content_type='application/pdf')

    # TEMP FILE
    def __getTempFilename(self, file_name):
        return os.path.join(self.__problem_dir, 'tmp', file_name)
    
    def saveTempFile(self, file_name, content):
        self.save(self.__getTempFilename(file_name), content)
    
    def loadTempFile(self, file_name):
        return self.open(self.__getTempFilename(file_name))

    def deleteTempFile(self, file_name):
        if self.exists(self.__getTempFilename(file_name)):
            self.delete(self.__getTempFilename(file_name))

    # TEST CASE
    def __getTestcaseFilename(self, test_name, file_name):
        return os.path.join(self.__problem_dir, 'tests', test_name, file_name)

    def saveTestcaseFile(self, test_name, file_name, content):
        self.save(self.__getTestcaseFilename(test_name, file_name), content)

    def loadTestcaseFile(self, test_name, file_name):
        return FileResponse(self.open(self.__getTestcaseFilename(test_name, file_name)), content_type='text/plain')

    # CHECKER
    def __getCheckerFilename(self):
        return os.path.join(self.__problem_dir, 'checker', 'checker.cpp')

    def getCheckerDir(self):
        return os.path.join(self.__problem_dir, 'checker')
    
    def saveCheckerFile(self, content):
        os.system('cp checker/testlib.h ' + os.path.join(settings.PROBLEM_ROOT, self.__problem_dir, 'checker', 'testlib.h'))
        self.save(self.__getCheckerFilename(), content)

    # OVERRIDE FROM BASE CLASS
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.PROBLEM_ROOT, name))
        return name

