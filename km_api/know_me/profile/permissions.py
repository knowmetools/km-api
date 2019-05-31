from django.conf import settings
from django.shortcuts import get_object_or_404

from rest_framework import permissions

from know_me.profile import models


class HasListEntryListPermissions(permissions.BasePermission):
    """
    Permission for checking if a user has access to the list entries of
    a profile item.
    """

    def has_permission(self, request, view):
        """
        Determine if the requesting user has access to the view.

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
            # fmt: off
            query["topic__profile__km_user__user__know_me_subscription__is_active"] = True  # noqa
            # fmt: on

        item = get_object_or_404(models.ProfileItem, **query)

        if request.method in permissions.SAFE_METHODS:
            return item.has_object_read_permission(request)

        return item.has_object_write_permission(request)


class HasProfileItemListPermissions(permissions.BasePermission):
    """
    Permission for checking if a user has access to the item list of a
    profile topic.
    """

    def has_permission(self, request, view):
        """
        Determine if the requesting user has access to the view.

        Args:
            request:
                The request being made.
            view:
                The view being accessed.

        Returns:
            A boolean indicating if the requesting user should be
            granted access to the view.
        """
        topic = get_object_or_404(
            models.ProfileTopic, pk=view.kwargs.get("pk")
        )

        if request.method in permissions.SAFE_METHODS:
            return topic.has_object_read_permission(request)

        return topic.has_object_write_permission(request)


class HasProfileTopicListPermissions(permissions.BasePermission):
    """
    Permission for checking if a user has access to the topic list of a
    profile.
    """

    def has_permission(self, request, view):
        """
        Determine if the requesting user has access to the view.

        Args:
            request:
                The request being made.
            view:
                The view being accessed.

        Returns:
            A boolean indicating if the requesting user should be
            granted access to the view.
        """
        profile = get_object_or_404(models.Profile, pk=view.kwargs.get("pk"))

        if request.method in permissions.SAFE_METHODS:
            return profile.has_object_read_permission(request)

        return profile.has_object_write_permission(request)
