from django.urls.conf import re_path
from backend.views.admin.problem import AdminEditProblemTestcasesDeleteView
from backend.views.admin.problem import AdminEditProblemTestcasesEditView
from django.contrib.auth.decorators import user_passes_test
from django.urls import path, include

#media
from django.conf import settings
from django.conf.urls.static import static


#authenticate
from backend.views.auth.login import WhoView
from backend.views.auth.login import LoginView
from backend.views.auth.login import ForgotPasswordView
from backend.views.auth.login import ForgotPasswordResetView
from backend.views.auth.login import LogoutView
from backend.views.auth.signup import SignupView

#user
from backend.views.user.problem import UserProblemView
from backend.views.user.home import UserHomeView

#admin
from backend.views.admin.home import AdminHomeView
from backend.views.admin.home import Error404Page
from backend.views.admin.home import AdminSubmissionStatusView
from backend.views.admin.home import AdminRankingView
from backend.views.admin.home import AdminContactView
from backend.views.admin.home import AdminSettingView

from backend.views.admin.problem import AdminListProblemView
from backend.views.admin.problem import AdminEditProblemDeatailsview
from backend.views.admin.problem import AdminEditProblemProblemSetterview
from backend.views.admin.problem import AdminEditProblemLanguagesview
from backend.views.admin.problem import AdminEditProblemSettingsview
from backend.views.admin.problem import AdminEditProblemTestcasesview
from backend.views.admin.problem import AdminEditProblemCustomCheckerview
from backend.views.admin.problem import AdminEditProblemTestcasesUploadZipView

from backend.views.admin.contest import AdminListContestView
from backend.views.admin.contest import AdminCreateContestView

from backend.views.admin.categories import AdminCategoriesView

from backend.views.admin.usermanage import AdminListAdministratorsView
from backend.views.admin.usermanage import AdminListUsersView
from backend.views.admin.usermanage import AdminEditUserView
from backend.views.admin.usermanage import AdminCreateUserView
from backend.views.admin.usermanage import AdminDeleteUser

from backend.views.admin.tag import AdminEditTagView
from backend.views.admin.tag import AdminListTagView

from backend.views.admin.language import AdminListLanguageView
from backend.views.admin.language import AdminEditLanguageView
from backend.views.admin.language import AdminCreateNewLanguage
from backend.views.admin.language import AdminDeleteLanguage

from django.views.static import serve

url_patterns_admin_sub = [
    path('', AdminHomeView),
    path('problems/', AdminListProblemView),
    #path('problem/create/', AdminCreateProblemView),
    path('problems/edit/<str:problem_short_name>/', AdminEditProblemDeatailsview),
    path('problems/edit/<str:problem_short_name>/details', AdminEditProblemDeatailsview),
    path('problems/edit/<str:problem_short_name>/problemsetter', AdminEditProblemProblemSetterview),
    path('problems/edit/<str:problem_short_name>/testcases', AdminEditProblemTestcasesview),
    path('problems/edit/<str:problem_short_name>/testcases/uploadzip/', AdminEditProblemTestcasesUploadZipView),
    path('problems/edit/<str:problem_short_name>/testcases/edit/<int:testcase_pk>/', AdminEditProblemTestcasesEditView),
    path('problems/edit/<str:problem_short_name>/testcases/delete/<int:testcase_pk>/', AdminEditProblemTestcasesDeleteView),
    path('problems/edit/<str:problem_short_name>/languages', AdminEditProblemLanguagesview),
    path('problems/edit/<str:problem_short_name>/settings', AdminEditProblemSettingsview),
    path('problems/edit/<str:problem_short_name>/customchecker', AdminEditProblemCustomCheckerview),

    path('contests/create/', AdminCreateContestView),
    path('contests/', AdminListContestView),

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

    path('topics/', AdminListTagView),
    path('topics/<str:topic_name>/', AdminEditTagView),
    path('setting/', AdminSettingView),

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
    path('forgotpassword/<uidb64>/<token>/', ForgotPasswordResetView, name='password_reset_confirm'),
    path('logout/', LogoutView),
    path('signup/', SignupView),
]

url_patterns_user = [
    path('', UserHomeView),
    path('problems/<str:problem_id>/', UserProblemView),
]

from backend.views.random.user import CreateRandomUser

url_pattern_random = [
    path('random/user', CreateRandomUser)
]

from django.conf.urls import url
import re

def merge_static(prefix, view=serve, **kwargs):
    return [
        re_path(r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')), view, kwargs=kwargs),
    ]

urlpatterns = [
    path('who/', WhoView),
    #url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}), 
    #url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}), 
] + url_pattern_random + url_patterns_admin + url_patterns_auth + url_patterns_user + merge_static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


