from django.shortcuts import get_object_or_404

from rest_framework import permissions

from know_me.journal import models


class HasEntryCommentListPermissions(permissions.BasePermission):
    """
    Permission for checking if a user has access to the comments of a
    journal entry.
    """

    def has_permission(self, request, view):
        """
        Determine if the requesting user has access to the view.

        Anyone with read access to a journal entry should be able to
        comment on it.

        Args:
            request:
                The request being made.
            view:
                The view being accessed.

        Returns:
            A boolean inidicating if the requesting user should be
            granted access to the view.
        """
        entry = get_object_or_404(models.Entry, pk=view.kwargs.get('pk'))

        return entry.has_object_read_permission(request)
