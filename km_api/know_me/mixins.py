"""View mixins for the ``know_me`` module.
"""

from django.shortcuts import get_object_or_404

from know_me import models


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
