from django.contrib import admin
from django.contrib.auth.models import User

from backend.models.language import LanguageModel

from backend.models.problem import ProblemCategoryModel
from backend.models.problem import ProblemModel
from backend.models.problem import ProblemTestCaseModel

from backend.models.submission import SubmissionModel
from backend.models.submission import SubmissionTestcaseResultModel

#from backend.models.usersetting import ??

admin.site.register(LanguageModel)
admin.site.register(ProblemCategoryModel)
admin.site.register(ProblemModel)
admin.site.register(ProblemTestCaseModel)
admin.site.register(SubmissionModel)
admin.site.register(SubmissionTestcaseResultModel)


