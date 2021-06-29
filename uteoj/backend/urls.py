from django.urls import path
from backend.views.admin.home import AdminHomeView
from backend.views.auth.login import WhoView
from backend.views.auth.login import LoginView
from backend.views.auth.signup import SignupView

urlpatterns = [
    path('admin/', AdminHomeView),
    path('who/', WhoView),
    path('login/', LoginView),
    path('signup/', SignupView),
]
