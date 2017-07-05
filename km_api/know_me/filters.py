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
            pk=view.kwargs.get('profile_pk'),
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
            profile row whose primary key is specified in the view.
        """
        row = get_object_or_404(
            models.ProfileRow,
            group__profile__user=request.user,
            pk=view.kwargs.get('row_pk'))

        return queryset.filter(row__pk=row.pk)
