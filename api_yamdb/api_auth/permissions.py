from django.conf import settings
from rest_framework import permissions

roles = [role[0] for role in settings.USER_ROLES]


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        is_auth = bool(request.user and request.user.is_authenticated)
        return is_auth and request.user.role in roles[1:]


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        is_auth = bool(request.user and request.user.is_authenticated)
        return is_auth and request.user.role in roles[2:]


def is_moderator_role(role):
    return role in roles[1:]


def is_admin_role(role):
    return role in roles[2:]
