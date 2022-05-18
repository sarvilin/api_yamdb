from rest_framework import permissions


class AdminOnly(permissions.BasePermission):
    """Разрешения только для администратора. """

    def has_permission(self, request, view):
        return(
            request.user.is_admin
            or request.user.is_staff
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_admin
            or request.user.is_staff
        )


class IsAdminUserOrReadOnly(permissions.BasePermission):
    """Разрешения для администратора или только чтения."""

    def has_permission(self, request, view):
        return (
            request.method
            in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin
        )


class AdminModeratorAuthorPermission(permissions.BasePermission):
    """Разрешения для администратора, модератора, автора."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or (obj.author == request.user)
            or request.user.is_moderator
            or request.user.is_admin
        )
