"""Пермишены."""


from rest_framework import permissions
from rest_framework.permissions import BasePermission

from reviews.models import Comment, Review, User


class OnlyAdminPermission(BasePermission):
    """Полное разрешение для admin и GET запросы для anon."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return ((request.user.is_authenticated
                and request.user.role == 'admin')
                or request.user.is_superuser)


class CustomPermission(BasePermission):
    """Разрешение на всё views, кроме 'только для admin'"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.author == request.user or isinstance(obj, User):
            return True
        if request.user.role == 'moderator' and isinstance(
            obj,
            (Review, Comment)
        ):
            return True
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False


class AdminPermission(BasePermission):
    """Полное разрешение для admin."""

    def has_permission(self, request, view):
        return ((request.user.is_authenticated
                and request.user.role == 'admin')
                or request.user.is_superuser)
