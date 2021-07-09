from django.urls import path

#admin
from backend.views.admin.home import AdminHomeView
from backend.views.admin.home import AdminSubmissionStatusView
from backend.views.admin.home import AdminRankingView
from backend.views.admin.home import AdminContactView
from backend.views.admin.home import AdminSettingView

from backend.views.admin.problem import AdminListProblemView
from backend.views.admin.problem import AdminCreateProblemView

from backend.views.admin.contest import AdminListContestView
from backend.views.admin.contest import AdminCreateContestView

from backend.views.admin.categories import AdminCategoriesView

from backend.views.admin.usermanage import AdminListAdministratorsView
from backend.views.admin.usermanage import AdminListUsersView
from backend.views.admin.usermanage import AdminEditUserView


from backend.views.admin.tag import AdminEditTagView
from backend.views.admin.tag import AdminListTagView

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


url_patterns_admin = [
    path('admin/', AdminHomeView),
    path('admin/problems/', AdminListProblemView),
    path('admin/problem/create/', AdminCreateProblemView),
    path('admin/contest/create/', AdminCreateContestView),
    path('admin/contests/', AdminListContestView),
    path('admin/categories/', AdminCategoriesView),
    path('admin/status/', AdminSubmissionStatusView),
    path('admin/ranks/', AdminRankingView),
    path('admin/contact/', AdminContactView),
    path('admin/users/administrators/', AdminListAdministratorsView),
    path('admin/users/contestants/', AdminListUsersView),
    path('admin/users/<str:user_name>/', AdminEditUserView),
    path('admin/topics/', AdminListTagView),
    path('admin/topics/<str:topic_name>/', AdminEditTagView),
    path('admin/setting/', AdminSettingView),
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

urlpatterns = [
    path('who/', WhoView),
] + url_patterns_admin + url_patterns_auth + url_patterns_user


