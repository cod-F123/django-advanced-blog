from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Is owner or author can update or delete their own posts"""

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:

            return True

        return obj.author.user.id == request.user.id
