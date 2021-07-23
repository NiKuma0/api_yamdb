from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        is_auth = bool(request.user and request.user.is_authenticated)
        return is_auth and request.user.is_moderator


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        is_auth = bool(request.user and request.user.is_authenticated)
        return is_auth and request.user.is_admin
