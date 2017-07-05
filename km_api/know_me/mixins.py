"""View mixins for the ``know_me`` module.
"""

from django.shortcuts import get_object_or_404

from know_me import models


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
