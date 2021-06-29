from django.urls import path
from backend.views.admin.home import AdminHomeView


urlpatterns = [
    path('admin/', AdminHomeView),
]
