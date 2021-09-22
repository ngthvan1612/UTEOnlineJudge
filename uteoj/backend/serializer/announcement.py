from backend.models.problem import ProblemCategoryModel
from rest_framework import serializers

from rest_framework import viewsets
from rest_framework import serializers

from backend.serializer.permission import RequirePermissionForAdminSite
from backend.models.announcement import AnnouncementModel

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementModel
        fields = ('id', 'author', 'title', 'content')

class AnnouncementView(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    permission_classes = []

    def get_queryset(self):
        return AnnouncementModel.objects.all()    


