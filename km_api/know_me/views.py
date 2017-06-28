"""Views for the ``know_me`` module.
"""

from django.utils.translation import ugettext as _

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from know_me import models, serializers


class ProfileListView(generics.ListCreateAPIView):
    """
    View for listing and creating profiles.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileListSerializer

    def get_queryset(self):
        """
        Get the profiles that the requesting user has access to.

        Returns:
            The requesting user's profile.
        """
        return models.Profile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Create a new profile for the requesting user.

        Returns:
            A new ``Profile`` instance.

        Raises:
            ValidationError:
                If the user making the request already has a profile.
        """
        if hasattr(self.request.user, 'profile'):
            raise ValidationError(
                code='duplicate_profile',
                detail=_('Users may not have more than one profile.'))

        return serializer.save(user=self.request.user)
