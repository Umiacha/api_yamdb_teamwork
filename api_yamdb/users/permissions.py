from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrSuperuser(BasePermission):
    """Доступен только админу или суперпользователю."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == "admin"
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class AdminOrReadOnly(IsAdminOrSuperuser):
    """Редактировать может только админ. Чтение -- любой.

    Суперюзер == админ.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or super().has_permission(
            request, view
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class OwnerOrStaff(AdminOrReadOnly):
    """Редактировать может либо автор, либо админ/модератор.

    Суперюзер == админ.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.role == "moderator"
        ) or super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        return (
            (request.user.is_authenticated and request.user == obj.author)
            or (
                request.user.is_authenticated
                and request.user.role == "moderator"
            )
            or super().has_object_permission(request, view, obj)
        )


class OwnerOrStaffOrReadOnly(BasePermission):
    """Редактировать может либо автор, либо админ/модератор. Чтение - любой

    Суперюзер == админ.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.role == "moderator"
            or request.user.role == "admin"
        )
