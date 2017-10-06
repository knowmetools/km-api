"""Views for the ``know_me`` module.
"""

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from dry_rest_permissions.generics import DRYPermissions

from rest_framework import generics
from rest_framework.exceptions import ValidationError

from know_me import filters, models, serializers


class AccessorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for modifying a specific Know Me user accessor.
    """
    serializer_class = serializers.KMUserAccessorSerializer

    def get_queryset(self):
        """
        Get the accessors accessible to the requesting user.

        Returns:
            A queryset containing the ``KMUserAccessor`` instances
            belonging to the requesting user.
        """
        km_user = get_object_or_404(
            models.KMUser,
            user=self.request.user)

        return km_user.km_user_accessors.all()


class AccessorListView(generics.ListCreateAPIView):
    """
    View for listing and creating new accessors for a Know Me user.
    """
    serializer_class = serializers.KMUserAccessorSerializer

    def get_queryset(self):
        """
        Get the accessors for the user with the given PK.

        Returns:
            A queryset containing the ``KMUserAccessor`` instances
            belonging to the Know Me user whose PK was passed to the
            view.
        """
        km_user = get_object_or_404(models.KMUser, user=self.request.user)

        return km_user.km_user_accessors.all()

    def perform_create(self, serializer):
        """
        Create a new accessor for the current user.

        Args:
            serializer:
                The serializer containing the received data.

        Returns:
            The newly created ``KMUserAccessor`` instance.
        """
        km_user = get_object_or_404(models.KMUser, user=self.request.user)

        return serializer.save(km_user=km_user)


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
    filter_backends = (filters.KMUserAccessFilterBackend,)
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
    permission_classes = (DRYPermissions,)
    queryset = models.EmergencyItem.objects.all()
    serializer_class = serializers.EmergencyItemSerializer


class EmergencyItemListView(generics.ListCreateAPIView):
    """
    View for listing and creating emergency items.
    """
    filter_backends = (filters.KMUserAccessFilterBackend,)
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
    permission_classes = (DRYPermissions,)
    serializer_class = serializers.KMUserListSerializer

    def get_queryset(self):
        """
        Get the list of Know Me users the requesting user has access to.

        Returns:
            A queryset containing the ``KMUser`` instances accessible to
            the requesting user.
        """
        # User granted access through an accessor
        query = Q(km_user_accessor__user_with_access=self.request.user)
        query &= Q(km_user_accessor__accepted=True)

        # Requesting user is the user
        query |= Q(user=self.request.user)

        return models.KMUser.objects.filter(query)

    def perform_create(self, serializer):
        """
        Create a new Know Me specific user for the requesting user.

        Returns:
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
    permission_classes = (DRYPermissions,)
    serializer_class = serializers.ListEntrySerializer

    def get_queryset(self):
        """
        Get the list entries belonging to the specified list content.

        Returns:
            A queryset containing the ``ListEntry`` instances belonging
            to the ``ListContent`` instance whose ID is given.

        Raises:
            Http404:
                If the requesting user doesn't have access to the
                profile that the parent list content belongs to, or if
                there is no list content with the given ID.
        """
        list_content = get_object_or_404(
            models.ListContent,
            pk=self.kwargs.get('pk'))
        profile = list_content.profile_item.topic.profile

        # Requesting user is profile owner
        if profile.km_user.user == self.request.user:
            return list_content.entries.all()

        # Look for accessor granting access
        accessor = get_object_or_404(
            models.KMUserAccessor,
            accepted=True,
            km_user=profile.km_user,
            user_with_access=self.request.user)

        # Only return the list entries if they belong to a public
        # profile or if the accessor grants private profile access.
        if not profile.is_private or accessor.has_private_profile_access:
            return list_content.entries.all()

        raise Http404()

    def perform_create(self, serializer):
        """
        Create a new list entry for the given list content.

        Args:
            serializer:
                The serializer containing the data used to create the
                new entry.

        Returns:
            The newly created ``ListEntry`` instance.
        """
        list_content = get_object_or_404(
            models.ListContent,
            profile_item__topic__profile__km_user__user=self.request.user,
            pk=self.kwargs.get('pk'))

        return serializer.save(list_content=list_content)


class ListEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
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


class ProfileListView(generics.ListCreateAPIView):
    """
    View for listing and creating profiles.
    """
    filter_backends = (filters.KMUserAccessFilterBackend,)
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
    permission_classes = (DRYPermissions,)
    serializer_class = serializers.ProfileItemSerializer

    def get_queryset(self):
        """
        Get the profile items in the given topic.

        Returns:
            A queryset containing the ``ProfileItem`` instances
            belonging to the ``ProfileTopic`` instance whose ID was
            provided.
        """
        topic = get_object_or_404(
            models.ProfileTopic,
            pk=self.kwargs.get('pk'))
        profile = topic.profile

        # Requesting user is profile owner
        if profile.km_user.user == self.request.user:
            return topic.items.all()

        # Look for accessor granting access
        accessor = get_object_or_404(
            models.KMUserAccessor,
            accepted=True,
            km_user=profile.km_user,
            user_with_access=self.request.user)

        # Only return the items if they belong to a public profile or if
        # the accessor grants private profile access.
        if not profile.is_private or accessor.has_private_profile_access:
            return topic.items.all()

        raise Http404()

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
    permission_classes = (DRYPermissions,)
    serializer_class = serializers.ProfileTopicSerializer

    def get_queryset(self):
        """
        Get the profile topics in the given profile.

        Returns:
            A queryset containing the ``ProfileTopic`` instances that
            belong to the ``Profile`` instance whose ID is specified.
        """
        profile = get_object_or_404(models.Profile, pk=self.kwargs.get('pk'))

        # Requesting user is profile owner
        if profile.km_user.user == self.request.user:
            return profile.topics.all()

        # Look for accessor granting access
        accessor = get_object_or_404(
            models.KMUserAccessor,
            accepted=True,
            km_user=profile.km_user,
            user_with_access=self.request.user)

        # Only return the topics if they belong to a public profile or
        # if the accessor grants private profile access.
        if not profile.is_private or accessor.has_private_profile_access:
            return profile.topics.all()

        raise Http404()

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
