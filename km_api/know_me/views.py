"""Views for the ``know_me`` module.
"""

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from know_me import models, serializers


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retreiving and updating a specific profile.
    """
    lookup_url_kwarg = 'profile_pk'
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileDetailSerializer

    def get_queryset(self):
        """
        Get the profiles that the requesting user has access to.

        Returns:
            The requesting user's profile.
        """
        return models.Profile.objects.filter(user=self.request.user)


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


class ProfileGroupListView(generics.ListCreateAPIView):
    """
    View for listing and creating profile groups.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileGroupListSerializer

    def get_queryset(self):
        """
        Get the profile groups of the specified profile.

        Returns:
            The profile groups associated with the profile whose ID is
            given in the current URL.
        """
        profile = get_object_or_404(
            models.Profile,
            pk=self.kwargs.get('profile_pk'),
            user=self.request.user)

        return profile.groups

    def perform_create(self, serializer):
        """
        Create a new profile group for the given profile.

        Args:
            serializer:
                The serializer containing the data received.

        Returns:
            The newly created ``ProfileGroup`` instance.
        """
        profile = get_object_or_404(
            models.Profile,
            pk=self.kwargs.get('profile_pk'))

        return serializer.save(profile=profile)
