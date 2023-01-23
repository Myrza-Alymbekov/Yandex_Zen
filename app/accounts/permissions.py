from rest_framework.permissions import BasePermission


class OwnerOrReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.author)

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_authenticated and
                    obj.user.author == request.user.author)
