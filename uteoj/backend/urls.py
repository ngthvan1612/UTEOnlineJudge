from django.urls import path

#admin
from backend.views.admin.home import AdminHomeView
from backend.views.admin.problem import AdminListProblemView

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


urlpatterns = [
    path('admin/', AdminHomeView),
    path('who/', WhoView),
    path('', UserHomeView),
    path('login/', LoginView),
    path('forgotpassword/', ForgotPasswordView),
    path('forgotpassword/<uidb64>/<token>/', ForgotPasswordResetView, name='password_reset_confirm'),
    path('logout/', LogoutView),
    path('signup/', SignupView),
    path('admin/problems/', AdminListProblemView),
    path('problems/<str:problem_id>/', UserProblemView),
]



