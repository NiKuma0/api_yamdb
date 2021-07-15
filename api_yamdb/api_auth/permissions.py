from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in request.user.roles[1:]


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in request.user.roles[2:]
