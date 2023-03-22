from rest_framework.permissions import BasePermission

from users.models import User


class CustomAdminPermission(BasePermission):
    """Кастомый допуск"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == User.ADMIN
                     or request.user.is_superuser))
