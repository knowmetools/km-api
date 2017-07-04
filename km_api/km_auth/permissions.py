"""Permissions for authentication views.
"""

from django.utils.translation import ugettext_lazy as _

from rest_framework.permissions import BasePermission


class IsAnonymous(BasePermission):
    """
    Permission that only gives anonymous users access.
    """
    message = _('This view requires the user to NOT be authenticated.')

    def has_permission(self, request, view):
        """
        Determine if the user is allowed to access the current view.

        Args:
            request:
                The request being made.
            view:
                The view being accessed.

        Returns:
            bool:
                ``True`` if the user making the request is anonymous,
                and ``False`` otherwise.
        """
        return request.user.is_anonymous()
