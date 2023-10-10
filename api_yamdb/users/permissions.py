from rest_framework.permissions import BasePermission, SAFE_METHODS


class AdminOrReadOnly(BasePermission):
    """Редактировать может только админ. Чтение -- любой.
    
    Суперюзер == админ.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_staff
            or request.user.is_superuser
        )
    
    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_staff
            or request.user.is_superuser
        )


class OwnerOrStaff(AdminOrReadOnly):
    """Редактировать может либо автор, либо админ/модератор.
    
    Суперюзер == админ.
    """
    def has_permission(self, request, view):
        return (
            super().has_permission(self, request, view)
            or request.user.is_authenticated
            or request.user.role == 'moderator'
        )
    
    def has_object_permission(self, request, view, obj):
        return (
            super().has_permission(self, request, view)
            or request.user == obj.author
            or request.user.role == 'moderator'
        )
