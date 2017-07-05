"""Views for the ``know_me`` module.
"""

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from dry_rest_permissions.generics import DRYPermissions

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from know_me import filters, mixins, models, serializers


class GalleryView(generics.CreateAPIView):
    """
    View for creating gallery items.
    """
    serializer_class = serializers.GalleryItemSerializer

    def perform_create(self, serializer):
        """
        Create a new gallery item for the given profile.

        Args:
            serializer:
                A serializer instance containing the submitted data.

        Returns:
            The newly created ``GalleryItem`` instance.
        """
        profile = models.Profile.objects.get(
            pk=self.kwargs.get('profile_pk'))

        return serializer.save(profile=profile)


class GalleryItemDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating a specific gallery item.
    """
    lookup_url_kwarg = 'gallery_item_pk'
    permission_classes = (DRYPermissions,)
    queryset = models.GalleryItem.objects.all()
    serializer_class = serializers.GalleryItemSerializer


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retreiving and updating a specific profile.
    """
    lookup_url_kwarg = 'profile_pk'
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
    lookup_url_kwarg = 'group_pk'
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
            pk=self.kwargs.get('profile_pk'))

        return serializer.save(profile=profile)


class ProfileItemDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating a specific profile item.
    """
    lookup_url_kwarg = 'item_pk'
    permission_classes = (DRYPermissions,)
    queryset = models.ProfileItem.objects.all()
    serializer_class = serializers.ProfileItemSerializer


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
            pk=self.kwargs.get('profile_pk'))

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
            group__pk=self.kwargs.get('group_pk'),
            group__profile__pk=self.kwargs.get('profile_pk'),
            group__profile__user=self.request.user,
            pk=self.kwargs.get('row_pk'))

        return serializer.save(row=row)


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
