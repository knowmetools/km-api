"""View mixins for the ``know_me`` module.
"""

from know_me import models


class ProfileMixin:
    """
    Mixin for retreiving and creating profiles.

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
