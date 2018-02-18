from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import permissions

from know_me import models


class HasKMUserAccess(permissions.IsAuthenticated):
    """
    Permission for allowing access to a Know Me user.
    """

    def has_permission(self, request, view):
        """
        Determine if the requesting user has access to the given view.

        If the requesting user is the Know Me user or has an accessor
        granting access, then they are given permission.

        Args:
            request:
                The request being made.
            view:
                The view being accessed.

        Returns:
            A boolean indicating if the requesting user has access to
            the specified view.
        """
        if not super().has_permission(request, view):
            return False

        km_user = get_object_or_404(models.KMUser, pk=view.kwargs.get('pk'))

        if km_user.user == request.user:
            return True

        try:
            accessor = km_user.km_user_accessors.get(
                accepted=True,
                user_with_access=request.user)
        except models.KMUserAccessor.DoesNotExist:
            raise Http404()

        if accessor.can_write:
            return True

        return request.method in permissions.SAFE_METHODS
