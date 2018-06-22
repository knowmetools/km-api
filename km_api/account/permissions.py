from rest_framework import permissions


class IsStaff(permissions.BasePermission):
    """
    Permission that only grants access to staff users.
    """

    def has_permission(self, request, view):
        """
        Determine if the requesting user has permission to access a
        specific view.

        Args:
            request:
                The request being made.
            view:
                The view being accessed.

        Returns:
            A boolean indicating if the request should be permitted to
            access the specified view.
        """
        return request.user.is_staff
