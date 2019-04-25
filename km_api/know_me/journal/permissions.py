from django.conf import settings
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
        comment on it as long as the journal owner has an active premium
        subscription.

        Args:
            request:
                The request being made.
            view:
                The view being accessed.

        Returns:
            A boolean indicating if the requesting user should be
            granted access to the view.
        """
        query = {"pk": view.kwargs.get("pk")}
        if settings.KNOW_ME_PREMIUM_ENABLED:
            query["km_user__user__know_me_subscription__is_active"] = True

        entry = get_object_or_404(models.Entry, **query)

        return entry.has_object_read_permission(request)
