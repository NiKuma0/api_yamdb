from rest_framework import permissions


class ReviewAndCommentPermissions(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.author == request.user
                or request.user.role
                in ('moderator', 'admin'))
