from rest_framework.permissions import BasePermission
from rest_framework import permissions

from reviews.models import Review, User


# class AdminChangeOnly(BasePermission):
#     """Только Админ может добавлять/редактироать/удалять."""

#     def has_permission(self, request, view):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return bool(request.user and request.user.is_staff)

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         return bool(request.user and request.user.is_staff)


class OnlyAdminPermission(BasePermission):
    """Разрешение для admin."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
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
        elif obj.author == request.user or isinstance(obj, User):
            return True
        elif request.user.role == 'moderator' and isinstance(obj, Review):
            # как появится модель comments, то тоже добавим её сюда,
            # т.к. модератор имет доступ как к Review так и к comments
            return True
        elif request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False
