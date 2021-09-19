from backend.models.problem import ProblemCategoryModel
from django.contrib.auth.models import User
from backend.models.problem import ProblemModel, ProblemStatisticsModel
from rest_framework import serializers

from rest_framework import viewsets
from rest_framework import serializers
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated

class RequirePermissionForAdminSite(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        print('current user: ' + str(request.user))
        if request.method != 'GET':
            return request.user and request.user.is_staff
        return True


# PROBLEM STATISTICS ---------------------------------------------------
class ProblemStatisticsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemStatisticsModel
        fields = ('id', 'solvedCount')

class ProblemStatisticsModelPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 30

# PROBLEM STATISTICS ---------------------------------------------------
class ProblemCategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemCategoryModel
        fields = ('id', 'name', 'description')

# PROBLEM MODEL ---------------------------------------------------
class ProblemModelSerializer(serializers.ModelSerializer):
    problemstatisticsmodel = ProblemStatisticsModelSerializer()
    class Meta:
        model = ProblemModel
        fields = ('id', 'author', 'publish_date', 'categories', 'shortname', 'fullname', 'problem_type', 'difficult', 'problemstatisticsmodel')

class ProblemModelPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 30

class ProblemModelView(viewsets.ModelViewSet):
    serializer_class=ProblemModelSerializer
    # pagination_class=ProblemModelPagination
    permission_classes=[RequirePermissionForAdminSite]

    def get_queryset(self):
        return ProblemModel.objects.all()


# PROBLEM CATEGORY ---------------------------------------------------

class ProblemCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemCategoryModel
        fields = ('id', 'name', 'description')

class ProblemCategoryView(viewsets.ModelViewSet):
    serializer_class = ProblemCategoryModelSerializer
    permission_classes = [RequirePermissionForAdminSite]

    def get_queryset(self):
        return ProblemCategoryModel.objects.all()    
