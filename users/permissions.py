from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """ Проверяет, является ли пользователь модератором."""

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()

class IsNotModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.groups.filter(name="Moderator").exists()


class IsOwner(permissions.BasePermission):
    """ Проверяет, является ли пользователь владельцем."""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
