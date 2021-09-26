from django.core.files.storage import FileSystemStorage
from backend.models.problem import ProblemModel
from backend.filemanager.filemanager import OverwriteStorage

from django.http import FileResponse, Http404
from django.conf import settings

import os

class ImportUserStorage(FileSystemStorage):

    def __init__(self):
        super().__init__(settings.IMPORT_USER_ROOT)
    
    def saveImportUser(self, file_name, content):
        self.save(file_name, content)

    def loadImportUser(self, file_name):
        return FileResponse(self.open(file_name))

    # OVERRIDE FROM BASE CLASS
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.IMPORT_USER_ROOT, name))
        return name

