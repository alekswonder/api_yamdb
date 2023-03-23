from rest_framework.permissions import BasePermission, SAFE_METHODS

from users.models import User


class CustomAdminPermission(BasePermission):
    """Кастомый допуск"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == User.ADMIN
                     or request.user.is_superuser))


class AuthorOrReadOnly(BasePermission):
    """Допуск для автора"""

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)


class AdminOrAuthorOrReadOnly(BasePermission):
    """Допуск для админа или автора"""

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_superuser
                or request.user.is_staff)


class SafeMethodAdminPermission(BasePermission):
    """Допуск для админа"""
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_superuser))

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or (request.user.is_authenticated
                    and (request.user.role == User.ADMIN
                         or request.user.is_superuser)))
