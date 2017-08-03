"""Views for the ``know_me`` module.
"""

from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from dry_rest_permissions.generics import DRYPermissions

from rest_framework import generics
from rest_framework.exceptions import ValidationError

from know_me import filters, models, serializers


class EmergencyContactDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving and updating a specific emergency contact.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.EmergencyContact.objects.all()
    serializer_class = serializers.EmergencyContactSerializer


class EmergencyContactListView(generics.ListCreateAPIView):
    """
    View for listing and creating a specific emergency contact.
    """
    filter_backends = (filters.EmergencyContactFilterBackend,)
    permission_classes = (DRYPermissions,)
    queryset = models.EmergencyContact.objects.all()
    serializer_class = serializers.EmergencyContactSerializer

    def perform_create(self, serializer):
        """
        Create a new emergency contact for the given km_user.

        Args:
            serializer:
                A serializer instance containing the submitted data.

        Returns:
            The newly created ``EmergencyContact`` instance.
        """
        km_user = models.KMUser.objects.get(
            pk=self.kwargs.get('pk'))

        return serializer.save(km_user=km_user)


class EmergencyItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for updating and deleting a specific emergency item.
    """
    filter_backends = (filters.EmergencyItemFilterBackend,)
    permission_classes = (DRYPermissions,)
    queryset = models.EmergencyItem.objects.all()
    serializer_class = serializers.EmergencyItemSerializer


class EmergencyItemListView(generics.ListCreateAPIView):
    """
    View for listing and creating emergency items.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.EmergencyItem.objects.all()
    serializer_class = serializers.EmergencyItemSerializer

    def perform_create(self, serializer):
        """
        Create a new emergency item from the provided data.

        Args:
            serializer:
                A serializer instance containing the data given to the
                view.

        Returns:
            :class:`.EmergencyItem`:
                The emergency item that was created from the provided
                data.
        """
        km_user = models.KMUser.objects.get(pk=self.kwargs.get('pk'))

        return serializer.save(km_user=km_user)


class GalleryView(generics.CreateAPIView):
    """
    View for creating media resources.
    """
    filter_backends = (filters.MediaResourceFilterBackend,)
    serializer_class = serializers.MediaResourceSerializer

    def perform_create(self, serializer):
        """
        Create a new media resource for the given km_user.

        Args:
            serializer:
                A serializer instance containing the submitted data.

        Returns:
            The newly created ``MediaResource`` instance.
        """
        km_user = models.KMUser.objects.get(
            pk=self.kwargs.get('pk'))

        return serializer.save(km_user=km_user)


class KMUserDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retreiving and updating a specific km_user.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.KMUser.objects.all()
    serializer_class = serializers.KMUserDetailSerializer


class KMUserListView(generics.ListCreateAPIView):
    """
    View for listing and creating km_users.
    """
    filter_backends = (filters.KMUserFilterBackend,)
    permission_classes = (DRYPermissions,)
    queryset = models.KMUser.objects.all()
    serializer_class = serializers.KMUserListSerializer

    def perform_create(self, serializer):
        """
        Create a new Know Me specific user for the requesting user.

        Returns:
            :class:`.KMUser`:
                A new Know Me user.

        Raises:
            ValidationError:
                If the user making the request already has a Know Me
                specific account.
        """
        if hasattr(self.request.user, 'km_user'):
            raise ValidationError(
                _('Users may not have more than one Know Me account.'))

        return serializer.save(user=self.request.user)


class ListEntryListView(generics.ListCreateAPIView):
    """
    View for listing and creating list entries.
    """
    filter_backends = (filters.ListEntryFilterBackend,)
    permission_classes = (DRYPermissions,)
    queryset = models.ListEntry.objects.all()
    serializer_class = serializers.ListEntrySerializer


class ListEntryDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating a specific list entry.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.ListEntry.objects.all()
    serializer_class = serializers.ListEntrySerializer


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
                The superclass' serialzer context with the km_user whose
                primary key is passed to the view appended.
        """
        context = super().get_serializer_context()

        context['km_user'] = models.KMUser.objects.get(
            profile__topic__pk=self.kwargs.get('pk'))

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
                The superclass' serialzer context with the km_user whose
                primary key is passed to the view appended.
        """
        context = super().get_serializer_context()

        context['km_user'] = models.KMUser.objects.get(
            profile__topic__pk=self.kwargs.get('pk'))

        return context

    def perform_create(self, serializer):
        """
        Create a new profile item for the given topic.

        Args:
            serializer:
                The serializer containing the data used to create the
                new item.

        Returns:
            The newly created ``ProfileItem`` instance.
        """
        topic = get_object_or_404(
            models.ProfileTopic,
            profile__km_user__user=self.request.user,
            pk=self.kwargs.get('pk'))

        return serializer.save(topic=topic)


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
        Create a new profile for the given km_user.

        Args:
            serializer:
                The serializer containing the data received.

        Returns:
            The newly created ``Profile`` instance.
        """
        km_user = get_object_or_404(
            models.KMUser,
            pk=self.kwargs.get('pk'),
            user=self.request.user)

        return serializer.save(km_user=km_user)


class ProfileTopicDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retreiving and updating a profile topic.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.ProfileTopic.objects.all()
    serializer_class = serializers.ProfileTopicSerializer


class ProfileTopicListView(generics.ListCreateAPIView):
    """
    View for listing and creating topics in a profile.
    """
    filter_backends = (filters.ProfileTopicFilterBackend,)
    permission_classes = (DRYPermissions,)
    queryset = models.ProfileTopic.objects.all()
    serializer_class = serializers.ProfileTopicSerializer

    def perform_create(self, serializer):
        """
        Create a new profile topic for the given profile.

        Args:
            serializer:
                The serializer containing the received data.

        Returns:
            The newly created ``ProfileTopic`` instance.
        """
        profile = get_object_or_404(
            models.Profile,
            pk=self.kwargs.get('pk'),
            km_user__user=self.request.user)

        return serializer.save(profile=profile)
