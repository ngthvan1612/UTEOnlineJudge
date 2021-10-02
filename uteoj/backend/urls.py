from django.urls.conf import re_path
from backend.views.admin.problem import AdminEditProblemTestcasesDeleteView
from django.contrib.auth.decorators import user_passes_test
from django.urls import path, include

#media
from django.conf import settings
from django.conf.urls.static import static


#authenticate
from backend.views.auth.login import *
from backend.views.auth.signup import *

#user
from backend.views.user.problem import *
from backend.views.user.rank import *

from backend.views.user.profile import *
from backend.views.user.changepassword import *

from backend.views.user.submission import *

from backend.views.user.problem import *

from backend.views.user.home import *

from backend.views.user.contest import *

#admin
from backend.views.admin.home import *

from backend.views.admin.problem import *

from backend.views.admin.contest import *

from backend.views.admin.categories import *

from backend.views.admin.usermanage import *

from backend.views.admin.tag import *

from backend.views.admin.language import *

from django.views.static import serve

# API ----------------------------------------------------------------

from rest_framework import routers
from backend.serializer.problem import ProblemModelView
from backend.serializer.announcement import AnnouncementView

router = routers.DefaultRouter()
router.register('problem', ProblemModelView, 'problem')
router.register('announcement', AnnouncementView, 'announcement')

url_patterns_api = [
    path('api/', include(router.urls)),
]

# URL ----------------------------------------------------------------

url_patterns_admin_sub = [
    path('', AdminHomeView),
    path('problems/', AdminListProblemView),
    path('problems/create/', AdminCreateProblemView),
    path('problems/edit/<str:problem_short_name>/', AdminEditProblemDeatailsview),
    path('problems/edit/<str:problem_short_name>/details', AdminEditProblemDeatailsview),
    path('problems/edit/<str:problem_short_name>/problemsetter', AdminEditProblemProblemSetterview),
    path('problems/edit/<str:problem_short_name>/testcases', AdminEditProblemTestcasesview),
    path('problems/edit/<str:problem_short_name>/testcases/importsetting', AdminEditProblemTestcasesImportSetting),
    path('problems/edit/<str:problem_short_name>/testcases/exportsetting', AdminEditProblemTestcasesExportSetting),
    path('problems/edit/<str:problem_short_name>/testcases/uploadzip/', AdminEditProblemTestcasesUploadZipView),
    path('problems/edit/<str:shortname>/testcases/uploadtestcase', AdminEditProblemTestcaseUploadTestcase),
    path('problems/edit/<str:problem_short_name>/testcases/delete/<int:testcase_pk>/', AdminEditProblemTestcasesDeleteView),
    path('problems/edit/<str:problem_short_name>/settings', AdminEditProblemSettingsview),
    path('problems/edit/<str:problem_short_name>/customchecker', AdminEditProblemCustomCheckerview),
    path('problems/edit/<str:shortname>/settings/export', AdminExportProblemConfig),
    path('problems/edit/<str:shortname>/settings/import', AdminImportProblemConfig),
    path('problems/<str:id>/testcases/<str:test_name>/<str:io>', AdminViewTestcase),

    path('contests/create', AdminCreateContestView),
    path('contests', AdminListContestView),
    path('contests/edit/<int:id>/', AdminEditContestView),
    path('contests/edit/<int:id>/details', AdminEditContestView),
    path('contests/edit/<int:id>/problems', AdminEditContestProblemsView),
    path('contests/edit/<int:id>/api/problems', AdminContestFilterProblem),
    path('contests/edit/<int:id>/problems/<str:shortname>/remove', AdminEditContestRemoveProblems),
    path('contests/edit/<int:id>/problems/create', AdminEditContestCreateProblem),
    path('contests/edit/<int:id>/import', AdminEditContestImportUser),
    path('contests/edit/<int:id>/export', AdminEditContestExportView),
    path('contests/edit/<int:id>/export/contestants', AdminEditContestExportContestantView),
    path('contests/edit/<int:id>/export/result', AdminEditContestExportResultView),

    path('categories/', AdminCategoriesView),

    path('status/', AdminSubmissionStatusView),
    path('ranks/', AdminRankingView),
    path('contact/', AdminContactView),

    path('users/', AdminListUsersView),
    path('users/administrators/', AdminListAdministratorsView),
    path('users/contestants/', AdminListUsersView),
    path('users/edit/<str:user_name>/', AdminEditUserView),
    path('users/create/', AdminCreateUserView),
    path('users/delete/<str:user_name>/', AdminDeleteUser),
    path('users/import/', AdminImportUser),
    path('users/import/<int:huid>/<str:token>/<str:name>', AdminImportUserResultViewer),

    path('topics/', AdminListTagView),
    path('topics/<str:topic_name>/', AdminEditTagView),
    path('setting/', AdminSettingView),
    path('setting/details', AdminSettingView),
    path('setting/stmp', AdminSettingSTMP),
    path('setting/problemdefault', AdminSettingProblemDetault),

    path('language/', AdminListLanguageView),
    path('language/edit/<int:lang_id>/', AdminEditLanguageView),
    path('language/delete/<int:lang_id>/', AdminDeleteLanguage),
    path('language/create/', AdminCreateNewLanguage),
]

for x in url_patterns_admin_sub:
    x.callback = user_passes_test(lambda u: u.is_staff, login_url='/login/')(x.callback)

url_patterns_admin = [
    path('admin/', include(url_patterns_admin_sub)),
]

url_patterns_auth = [
    path('login/', LoginView),
    path('forgotpassword/', ForgotPasswordView),
    path('verifyEmail/<uidb64>/<token>/', VerifyEmailView, name='verifyEmail'),
    path('forgotpassword/<uidb64>/<token>/', ForgotPasswordResetView, name='password_reset_confirm'),
    path('logout/', LogoutView),
    path('signup/', SignupView),
]

url_patterns_user = [
    path('', UserHomeView),
    path('problem/<str:id>/statement', ProblemStatementViewer),
    path('problems/', UserListProblemView),
    path('problem/<str:shortname>', UserProblemView),
    path('problem/<str:shortname>/submit', UserSubmitSolution),
    path('submissions/', UserListSubmissionView),
    path('submissions/<int:submission_id>', UserSubmissionView),
    path('ranks', UserRankView),
    path('contests', UserContestListView),
    path('contests/<int:id>', UserContestView),
    path('profile',UserEditMyProfile),
    path('changepassword', UserChangePassword),
    path('media/user/<int:token>/<str:sha>/avatar', UserAvatarViewer),
]

from backend.views.random.user import CreateRandomUser
from backend.views.random.problem import CreateRandomProblem
from backend.views.random.category import CreateRandomCate
from backend.views.random.submission import CreateRandomSubmission

url_pattern_random = [
    path('random/user', CreateRandomUser),
    path('random/problem', CreateRandomProblem),
    path('random/categories', CreateRandomCate),
    path('random/submission', CreateRandomSubmission),
]


# MERGE ---------------------------------------------------------------

from django.conf.urls import url
import re

def merge_static(prefix, view=serve, **kwargs):
    return [
        re_path(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs),
    ]

urlpatterns = [
    path('who/', WhoView),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
] + url_patterns_api + url_pattern_random + url_patterns_admin + url_patterns_auth + url_patterns_user + merge_static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


