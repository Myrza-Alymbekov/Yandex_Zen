from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsStaffOrOwnerPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or
                    (request.user and request.user.is_authenticated and request.user.author) or
                    request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS or
                    (request.user and request.user.is_authenticated and
                     obj.author == request.user.author) or
                    request.user.is_staff)


class StatusOrReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or
                    (request.user and request.user.is_authenticated and request.user.author))

    def has_object_permission(self, request, view, obj):
        return bool(request.method in SAFE_METHODS or (request.user and request.user.is_authenticated and
                    obj.author == request.user.author))
