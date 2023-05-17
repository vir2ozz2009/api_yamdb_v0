from rest_framework.permissions import IsAdminUser, BasePermission
from rest_framework import permissions


class AdminChangeOnly(BasePermission):
    """Только Админ может добавлять/редактироать/удалять."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)
