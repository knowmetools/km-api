"""Filter backends for the ``know_me`` module.
"""

from django.shortcuts import get_object_or_404

from dry_rest_permissions.generics import DRYPermissionFiltersBase

from know_me import models


class EmergencyContactFilterBackend(DRYPermissionFiltersBase):
    """
    Filter for listing ``EmergencyContact`` instances.
    """

    def filter_list_queryset(self, request, queryset, view):
        """
        Filter emergency items for a list action.
        Args:
            request:
                The request being made.
            queryset:
                A queryset containing the objects to filter.
            view:
                The view being accessed.
        Returns:
            The provided queryset filtered to only include items owned
            by the user specified in the provided views arguments.
        """
        km_user = get_object_or_404(
            models.KMUser,
            pk=view.kwargs.get('pk'),
            user=request.user)

        return queryset.filter(km_user=km_user)


class EmergencyItemFilterBackend(DRYPermissionFiltersBase):
    """
    Filter for listing emergency items for a user.
    """

    def filter_list_queryset(self, request, queryset, view):
        """
        Filter emergency items for a list action.
        Args:
            request:
                The request being made.
            queryset:
                A queryset containing the objects to filter.
            view:
                The view being accessed.
        Returns:
            The provided queryset filtered to only include items owned
            by the user specified in the provided views arguments.
        """
        km_user = get_object_or_404(
            models.KMUser,
            pk=view.kwargs.get('pk'),
            user=request.user)

        return queryset.filter(km_user=km_user)


class KMUserFilterBackend(DRYPermissionFiltersBase):
    """
    Filter for listing ``KMUser`` instances.
    """

    def filter_list_queryset(self, request, queryset, view):
        """
        Filter km_users for a ``list`` action.

        Args:
            request:
                The request being made.
            queryset:
                A queryset containing the objects to filter.
            view:
                The view being accessed.

        Returns:
            A queryset containing the km_users accessible to the user
            making the request.
        """
        return queryset.filter(user=request.user)


class ListEntryFilterBackend(DRYPermissionFiltersBase):
    """
    Filter for listing ``ListEntry`` instances.
    """

    def filter_list_queryset(self, request, queryset, view):
        """
        Filter list entries for a ``list`` action.

        Args:
            request:
                The request being made:
            queryset:
                A queryset containing the objects to filter.
            view:
                The view being accessed.

        Returns:
            A queryset containing the list entries accessible to the
            user making the request.
        """
        content = get_object_or_404(
            models.ListContent,
            pk=view.kwargs.get('pk'),
            profile_item__topic__profile__km_user__user=request.user)

        return queryset.filter(list_content=content)


class MediaResourceFilterBackend(DRYPermissionFiltersBase):
    """
    Filter for listing media resources.
    """

    def filter_list_queryset(self, request, queryset, view):
        """
        Filter media resources for a 'list' action.
        Args:
            request:
                The request being made.
            queryset:
                The queryset containing the objects to filter.
            view:
                The view being accessed.
        Returns:
            The provided queryset filtered to contain only the media
            resources belonging to the requesting user.
        Raises:
            Http404:
                If there is no Know Me user with the primary key
                specified in the view or if the requesting user does not
                have access the the media resources for that user.
        """
        km_user = get_object_or_404(
            models.KMUser,
            pk=view.kwargs.get('pk'),
            user=request.user)

        return queryset.filter(km_user=km_user)


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
            A queryset containing the profiles belonging to the
            km_user whose primary key is specified in the view.
        """
        km_user = get_object_or_404(
            models.KMUser,
            pk=view.kwargs.get('pk'),
            user=request.user)

        return queryset.filter(km_user__pk=km_user.pk)


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
            profile__km_user__user=request.user,
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
            profile whose primary key is specified in the view.
        """
        profile = get_object_or_404(
            models.Profile,
            pk=view.kwargs.get('pk'),
            km_user__user=request.user)

        return queryset.filter(profile__pk=profile.pk)
