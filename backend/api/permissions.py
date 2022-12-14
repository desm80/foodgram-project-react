from rest_framework import permissions


class IsAdminAuthorOrReadOnly(permissions.BasePermission):
    """Кастомный пермишен доступ к изменению контента только для
    Администратора или Автора или на чтение
    для неавторизованных пользователей."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_admin
            or obj.author == request.user
        )


class IsAdmin(permissions.BasePermission):
    """Кастомный пермишен доступ только для Администратора."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Кастомный пермишен доступ только для Администратора или на чтение
    для неавторизованных пользователей."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated
                    and request.user.is_admin))
