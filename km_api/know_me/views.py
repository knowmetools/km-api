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


class MediaResourceDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating a specific media resource.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.MediaResource.objects.all()
    serializer_class = serializers.MediaResourceSerializer


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
        Create a new km_user for the requesting user.

        Returns:
            A new ``KMUser`` instance.

        Raises:
            ValidationError:
                If the user making the request already has a km_user.
        """
        if hasattr(self.request.user, 'km_user'):
            raise ValidationError(
                code='duplicate_km_user',
                detail=_('Users may not have more than one km_user.'))

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
        Create a new profile group for the given km_user.

        Args:
            serializer:
                The serializer containing the data received.

        Returns:
            The newly created ``ProfileGroup`` instance.
        """
        km_user = get_object_or_404(
            models.KMUser,
            pk=self.kwargs.get('pk'),
            user=self.request.user)

        return serializer.save(km_user=km_user)


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
            group__topic__pk=self.kwargs.get('pk'))

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
            group__topic__pk=self.kwargs.get('pk'))

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
            group__km_user__user=self.request.user,
            pk=self.kwargs.get('pk'))

        return serializer.save(topic=topic)


class ProfileTopicDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retreiving and updating a profile topic.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.ProfileTopic.objects.all()
    serializer_class = serializers.ProfileTopicSerializer


class ProfileTopicListView(generics.ListCreateAPIView):
    """
    View for listing and creating topics in a profile group.
    """
    filter_backends = (filters.ProfileTopicFilterBackend,)
    permission_classes = (DRYPermissions,)
    queryset = models.ProfileTopic.objects.all()
    serializer_class = serializers.ProfileTopicSerializer

    def perform_create(self, serializer):
        """
        Create a new profile topic for the given profile group.

        Args:
            serializer:
                The serializer containing the received data.

        Returns:
            The newly created ``ProfileTopic`` instance.
        """
        group = get_object_or_404(
            models.ProfileGroup,
            pk=self.kwargs.get('pk'),
            km_user__user=self.request.user)

        return serializer.save(group=group)
