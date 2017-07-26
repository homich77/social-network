from rest_framework import permissions


class IsStaffOrAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_staff or obj.author == request.user


class NotAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return not obj.author == request.user
