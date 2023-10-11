from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrSuperuser(BasePermission):
    """Доступен только админу или суперпользователю.
    """
    def has_permission(self, request, view):
        return (
            request.user.role == 'admin'
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.role == 'admin'
            or request.user.is_superuser
        )


class AdminOrReadOnly(IsAdminOrSuperuser):
    """Редактировать может только админ. Чтение -- любой.

    Суперюзер == админ.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or super().has_permission(self, request, view)
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or super().has_object_permission(self, request, view, obj)
        )


class OwnerOrStaff(AdminOrReadOnly):
    """Редактировать может либо автор, либо админ/модератор.

    Суперюзер == админ.
    """
    def has_permission(self, request, view):
        return (
            super().has_permission(self, request, view)
            or request.user.is_authenticated()
            or request.user.role == 'moderator'
        )

    def has_object_permission(self, request, view, obj):
        return (
            super().has_permission(self, request, view)
            or request.user == obj.author
            or request.user.role == 'moderator'
        )
