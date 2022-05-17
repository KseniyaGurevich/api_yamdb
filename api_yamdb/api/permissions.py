from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (
                    request.user.role == 'admin'
                    or request.user.is_superuser
            )


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == "POST" and request.user.is_authenticated:
            return (
                    request.user.role == 'admin'
                    or request.user.is_superuser
            )
