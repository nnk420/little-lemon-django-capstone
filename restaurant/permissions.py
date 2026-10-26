from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOnlyOrTokenAuthenticated(BasePermission):
    """
    Allow public GET/HEAD/OPTIONS requests; require authentication for writes.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or bool(
            request.user and request.user.is_authenticated
        )
