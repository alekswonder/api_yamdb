from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminOnly(BasePermission):
    """Кастомый допуск"""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsAuthorOrReadOnly(BasePermission):
    """Допуск для автора"""
    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user)


class IsAdminOrAuthorOrModeratorOrReadOnly(BasePermission):
    """Допуск для админа или автора"""
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)


class IsAdminOrReadOnly(BasePermission):
    """Допуск для админа"""
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated and request.user.is_admin
        )


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_superuser
