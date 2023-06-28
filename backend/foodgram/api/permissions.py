from rest_framework import permissions


class SelfEditUserOnlyPermission(permissions.BasePermission):
    """Обеспечивает доступ к users/me только текущему."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.id == request.user)
