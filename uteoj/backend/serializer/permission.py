from rest_framework.permissions import BasePermission

class RequirePermissionForAdminSite(BasePermission):
    def has_permission(self, request, view):
        print('current user: ' + str(request.user))
        if request.method != 'GET':
            return request.user and request.user.is_staff
        return True
