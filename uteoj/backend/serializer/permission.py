from rest_framework.permissions import BasePermission

class RequirePermissionForAdminSite(BasePermission):
    def has_permission(self, request, view):
        if request.method != 'GET':
            return request.user and request.user.is_staff
        return True
