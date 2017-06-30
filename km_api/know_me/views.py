"""Views for the ``know_me`` module.
"""

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from know_me import mixins, models, serializers


class ProfileDetailView(mixins.ProfileMixin, generics.RetrieveUpdateAPIView):
    """
    View for retreiving and updating a specific profile.
    """
    lookup_url_kwarg = 'profile_pk'
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileDetailSerializer


class ProfileListView(mixins.ProfileMixin, generics.ListCreateAPIView):
    """
    View for listing and creating profiles.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileListSerializer

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


class ProfileGroupDetailView(
        mixins.ProfileGroupMixin,
        generics.RetrieveUpdateAPIView):
    """
    View for retreiving and updating a specific profile group.
    """
    lookup_url_kwarg = 'group_pk'
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileGroupDetailSerializer


class ProfileGroupListView(
        mixins.ProfileGroupMixin,
        generics.ListCreateAPIView):
    """
    View for listing and creating profile groups.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileGroupListSerializer

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


class ProfileRowDetailView(
        mixins.ProfileRowMixin,
        generics.RetrieveUpdateAPIView):
    """
    View for retreiving and updating a profile row.
    """
    lookup_url_kwarg = 'row_pk'
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileRowSerializer


class ProfileRowListView(mixins.ProfileRowMixin, generics.ListCreateAPIView):
    """
    View for listing and creating rows in a profile group.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileRowSerializer

    def perform_create(self, serializer):
        """
        Create a new profile row for the given profile group.

        Args:
            serializer:
                The serializer containing the received data.

        Returns:
            The newly created ``ProfileRow`` instance.
        """
        group = get_object_or_404(
            models.ProfileGroup,
            pk=self.kwargs.get('group_pk'),
            profile__pk=self.kwargs.get('profile_pk'))

        return serializer.save(group=group)
