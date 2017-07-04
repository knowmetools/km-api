"""View mixins for the ``know_me`` module.
"""

from django.shortcuts import get_object_or_404

from know_me import models


class GalleryItemMixin:
    """
    Mixin for retrieving gallery items.

    This mixin limits the retrieved gallery items to those belonging to
    the specified profile.
    """

    def get_queryset(self):
        """
        Get the gallery items that belong to the given profile.

        Returns:
            A list of ``GalleryItem`` instances belonging to the profile
            whose primary key is given.
        """
        profile = get_object_or_404(
            models.Profile,
            pk=self.kwargs.get('profile_pk'),
            user=self.request.user)

        return profile.gallery_items.all()


class ProfileMixin:
    """
    Mixin for retrieving profiles.

    This mixin restricts the retrieved profiles to those accessible by
    the user making the request.
    """

    def get_queryset(self):
        """
        Get the profiles that the requesting user has access to.

        Returns:
            The profiles owned by the requesting user.
        """
        return models.Profile.objects.filter(user=self.request.user)


class ProfileGroupMixin:
    """
    Mixin for retrieving profile groups.

    This mixin restricts the retrieved profile groups to those
    accessible by the user making the request.
    """

    def get_queryset(self):
        """
        Get the profile groups that the requesting user has access to.

        Returns:
            The profile groups that the requesting user has access to
            and belong to the profile with the ID given.
        """
        profile = get_object_or_404(
            models.Profile,
            pk=self.kwargs.get('profile_pk'),
            user=self.request.user)

        return profile.groups.all()


class ProfileItemMixin:
    """
    Mixin for retrieving profile items.

    This mixin determines which items to retrieve based on paramters
    given in the URL and the user making the request.
    """

    def get_queryset(self):
        """
        Get the profile items corresponding to the given parameters.

        The fetched items must match the given profile, profile group,
        and profile row. They must also be accessible to the current
        user.

        Returns:
            The profile items belonging to the profile group with the
            given primary key.

        Raises:
            Http404:
                If the profile, group, or row whose primary keys are
                given do not exist.
        """
        row = get_object_or_404(
            models.ProfileRow,
            group__pk=self.kwargs.get('group_pk'),
            group__profile__pk=self.kwargs.get('profile_pk'),
            group__profile__user=self.request.user,
            pk=self.kwargs.get('row_pk'))

        return row.items.all()

    def get_serializer_context(self):
        """
        Get additional context to pass to serializers.

        Returns:
            dict:
                The superclass' serialzer context with the profile whose
                primary key is passed to the view appended.
        """
        context = super().get_serializer_context()

        context['profile'] = models.Profile.objects.get(
            pk=self.kwargs.get('profile_pk'))

        return context


class ProfileRowMixin:
    """
    Mixin for retrieving profile rows.

    This mixin restricts the retrieved profile rows to those accessible
    by the user making the request.
    """

    def get_queryset(self):
        """
        Get the profile rows matching the criteria specified.

        The URL contains additional information that the profile rows
        are constrained by such as profile ID and profile group ID.

        Returns:
            The profile rows that are in the profile group whose ID
            is given in the URL. The profile group must also be in a
            profile whose ID matches the one in the URL and must be
            accessible to the requesting user.
        """
        group = get_object_or_404(
            models.ProfileGroup,
            pk=self.kwargs.get('group_pk'),
            profile__pk=self.kwargs.get('profile_pk'),
            profile__user=self.request.user)

        return group.rows.all()
