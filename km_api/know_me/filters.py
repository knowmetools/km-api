"""Filter backends for the ``know_me`` module.
"""

from django.shortcuts import get_object_or_404

from dry_rest_permissions.generics import DRYPermissionFiltersBase

from know_me import models


class ProfileFilterBackend(DRYPermissionFiltersBase):
    """
    Filter for listing ``Profile`` instances.
    """

    def filter_list_queryset(self, request, queryset, view):
        """
        Filter profiles for a ``list`` action.

        Args:
            request:
                The request being made.
            queryset:
                A queryset containing the objects to filter.
            view:
                The view being accessed.

        Returns:
            A queryset containing the profiles accessible to the user
            making the request.
        """
        return queryset.filter(user=request.user)


class ProfileGroupFilterBackend(DRYPermissionFiltersBase):
    """
    Filter for listing ``ProfileGroup`` instances.
    """

    def filter_list_queryset(self, request, queryset, view):
        """
        Filter profile groups for a ``list`` action.

        Args:
            request:
                The request being made.
            queryset:
                A queryset containing the objects to filter.
            view:
                The view being accessed.

        Returns:
            A queryset containing the profile groups belonging to the
            profile whose primary key is specified in the view.
        """
        profile = get_object_or_404(
            models.Profile,
            pk=view.kwargs.get('pk'),
            user=request.user)

        return queryset.filter(profile__pk=profile.pk)


class ProfileItemFilterBackend(DRYPermissionFiltersBase):
    """
    Filter for listing profile items.
    """

    def filter_list_queryset(self, request, queryset, view):
        """
        Filter profile items for a ``list`` action.

        Args:
            request:
                The request being made.
            queryset:
                A queryset containing the objects to filter.
            view:
                The view being accessed.

        Returns:
            A queryset containing the profile items belonging to the
            profile topic whose primary key is specified in the view.
        """
        topic = get_object_or_404(
            models.ProfileTopic,
            group__profile__user=request.user,
            pk=view.kwargs.get('pk'))

        return queryset.filter(topic__pk=topic.pk)


class ProfileTopicFilterBackend(DRYPermissionFiltersBase):
    """
    Filter for listing profile topics.
    """

    def filter_list_queryset(self, request, queryset, view):
        """
        Filter profile topics for a ``list`` action.

        Args:
            request:
                The request being made.
            queryset:
                The queryset containing the objects to filter.
            view:
                The view being accessed.

        Returns:
            A queryset containing the profile topics belonging to the
            profile group whose primary key is specified in the view.
        """
        group = get_object_or_404(
            models.ProfileGroup,
            pk=view.kwargs.get('pk'),
            profile__user=request.user)

        return queryset.filter(group__pk=group.pk)
