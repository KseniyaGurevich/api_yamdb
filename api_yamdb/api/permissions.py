from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "PATCH"]:
            return obj.author == request.user
        elif request.method == "POST":
            return request.user.is_authenticated
        else:
            return obj.author == request.user