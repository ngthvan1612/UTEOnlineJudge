from backend.models.problem import ProblemCategoryModel
from backend.models.problem import ProblemModel
from rest_framework import serializers

from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.pagination import PageNumberPagination

from rest_framework.response import Response

from backend.serializer.permission import RequirePermissionForAdminSite


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProblemModel
        fields = ('id', 'author', 'publish_date',
                'categories', 'shortname', 'fullname',
                'problem_type', 'difficult', 'points_per_test',
                'total_points', 'statement', 'submission_visible_mode',
                'input_filename', 'output_filename', 'use_stdin',
                'use_stdout', 'time_limit', 'memory_limit',
                'use_checker', 'checker', 'totalSubmission',
                'solvedCount', 'ceCount', 'tleCount', 'mleCount', 'rteCount')


class ProblemModelView(viewsets.ModelViewSet):
    serializer_class=ProblemSerializer
    #permission_classes=[RequirePermissionForAdminSite]

    def get_queryset(self):
        return ProblemModel.objects.all()

    def list(self, request, *args, **kwargs):
        return Response(ProblemModel.objects.values('id', 'shortname', 'fullname'))

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

