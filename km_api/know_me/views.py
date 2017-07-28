"""Views for the ``know_me`` module.
"""

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from dry_rest_permissions.generics import DRYPermissions

from rest_framework import generics
from rest_framework.exceptions import ValidationError

from know_me import filters, models, serializers


class GalleryView(generics.CreateAPIView):
    """
    View for creating media resources.
    """
    serializer_class = serializers.MediaResourceSerializer

    def perform_create(self, serializer):
        """
        Create a new media resource for the given profile.

        Args:
            serializer:
                A serializer instance containing the submitted data.

        Returns:
            The newly created ``MediaResource`` instance.
        """
        profile = models.Profile.objects.get(
            pk=self.kwargs.get('pk'))

        return serializer.save(profile=profile)


class MediaResourceDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating a specific media resource.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.MediaResource.objects.all()
    serializer_class = serializers.MediaResourceSerializer


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retreiving and updating a specific profile.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileDetailSerializer


class ProfileListView(generics.ListCreateAPIView):
    """
    View for listing and creating profiles.
    """
    filter_backends = (filters.ProfileFilterBackend,)
    permission_classes = (DRYPermissions,)
    queryset = models.Profile.objects.all()
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


class ProfileGroupDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retreiving and updating a specific profile group.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.ProfileGroup.objects.all()
    serializer_class = serializers.ProfileGroupDetailSerializer


class ProfileGroupListView(generics.ListCreateAPIView):
    """
    View for listing and creating profile groups.
    """
    filter_backends = (filters.ProfileGroupFilterBackend,)
    permission_classes = (DRYPermissions,)
    queryset = models.ProfileGroup.objects.all()
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
            pk=self.kwargs.get('pk'),
            user=self.request.user)

        return serializer.save(profile=profile)


class ProfileItemDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating a specific profile item.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.ProfileItem.objects.all()
    serializer_class = serializers.ProfileItemSerializer

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
            group__row__pk=self.kwargs.get('pk'))

        return context


class ProfileItemListView(generics.ListCreateAPIView):
    """
    View for listing and creating profile items.
    """
    filter_backends = (filters.ProfileItemFilterBackend,)
    permission_classes = (DRYPermissions,)
    queryset = models.ProfileItem.objects.all()
    serializer_class = serializers.ProfileItemSerializer

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
            group__row__pk=self.kwargs.get('pk'))

        return context

    def perform_create(self, serializer):
        """
        Create a new profile item for the given row.

        Args:
            serializer:
                The serializer containing the data used to create the
                new item.

        Returns:
            The newly created ``ProfileItem`` instance.
        """
        row = get_object_or_404(
            models.ProfileRow,
            group__profile__user=self.request.user,
            pk=self.kwargs.get('pk'))

        return serializer.save(row=row)


class ProfileRowDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retreiving and updating a profile row.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.ProfileRow.objects.all()
    serializer_class = serializers.ProfileRowSerializer


class ProfileRowListView(generics.ListCreateAPIView):
    """
    View for listing and creating rows in a profile group.
    """
    filter_backends = (filters.ProfileRowFilterBackend,)
    permission_classes = (DRYPermissions,)
    queryset = models.ProfileRow.objects.all()
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
            pk=self.kwargs.get('pk'),
            profile__user=self.request.user)

        return serializer.save(group=group)
