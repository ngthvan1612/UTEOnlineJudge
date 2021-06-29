from django.urls import path

#admin
from backend.views.admin.home import AdminHomeView
from backend.views.admin.problem import AdminListProblemView

#authenticate
from backend.views.auth.login import WhoView
from backend.views.auth.login import LoginView
from backend.views.auth.signup import SignupView

#user

urlpatterns = [
    path('admin/', AdminHomeView),
    path('who/', WhoView),
    path('login/', LoginView),
    path('signup/', SignupView),
    path('admin/problems/', AdminListProblemView),
]

