"""Views for the ``know_me`` module.
"""

from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from dry_rest_permissions.generics import DRYPermissions

from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated

from know_me import filters, models, permissions, serializers


class AccessorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Endpoint for retrieving the details of a specific accessor.

    put:
    Endpoint for updating an accessor.

    patch:
    Endpoint for partially updating an accessor.

    delete:
    Endpoint for deleting a specific accessor.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.KMUserAccessorSerializer

    def get_queryset(self):
        """
        Get the accessors accessible to the requesting user.

        Returns:
            A queryset containing the ``KMUserAccessor`` instances
            belonging to the requesting user.
        """
        query = Q(km_user__user=self.request.user)
        query |= Q(user_with_access=self.request.user)

        return models.KMUserAccessor.objects.filter(query)


class AccessorListView(generics.ListCreateAPIView):
    """
    get:
    Endpoint for listing the accessors that grant access to the current
    user's Know Me profiles.

    post:
    Endpoint for creating a new accessor for the current user's
    profiles.
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


class KMUserDetailView(generics.RetrieveUpdateAPIView):
    """
    get:
    Endpoint for retrieving the details of a specific Know Me user.

    put:
    Endpoint for updating the details of a specific Know Me user.

    patch:
    Endpoint for partially updating the details of a specific Know Me
    user.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.KMUser.objects.all()
    serializer_class = serializers.KMUserDetailSerializer


class KMUserListView(generics.ListCreateAPIView):
    """
    get:
    Endpoint for listing the Know Me users that the current user has
    access to.

    post:
    Endpoint for creating a new Know Me user for the current user.

    *__Note__: Users may only create one Know Me app account.*
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
    get:
    Endpoint for listing the list entries associated with a list-type
    profile item.

    post:
    Endpoint for adding a new list entry to a list-type profile item.
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
    get:
    Endpoint for retrieving the details of a specific list entry in a
    list-type profile item.

    put:
    Endpoint for updating the details of a specific list entry in a
    list-type profile item.

    patch:
    Endpoint for partially updating the details of a specific list entry
    in a list-type profile item.

    delete:
    Endpoint for deleting a specific list entry from a list-type profile
    item.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.ListEntry.objects.all()
    serializer_class = serializers.ListEntrySerializer


class MediaResourceDetailView(generics.RetrieveUpdateAPIView):
    """
    get:
    Endpoint for retrieving the details of a specific media resource.

    put:
    Endpoint for updating the details of a specific media resource.

    patch:
    Endpoint for partially updating the details of a specifc media
    resource.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.MediaResource.objects.all()
    serializer_class = serializers.MediaResourceSerializer


class MediaResourceListView(generics.ListCreateAPIView):
    """
    get:
    Retrieve the media resources associated with the specified user's
    account.
    """
    filter_backends = (filters.KMUserAccessFilterBackend,)
    permission_classes = (DRYPermissions, permissions.HasKMUserAccess)
    queryset = models.MediaResource.objects.all()
    serializer_class = serializers.MediaResourceSerializer

    def get_queryset(self):
        """
        Filter the queryset based on the category from the URL.

        Returns:
            The media resources belonging to the specified Know Me user.
            If a category is specified, only the items from that
            category are returned.
        """
        queryset = super().get_queryset()

        category_id = self.request.query_params.get('category', None)
        if category_id is not None:
            queryset = queryset.filter(category__id=category_id)

        return queryset

    def perform_create(self, serializer):
        """
        Create a new media resource for the specified user.

        Args:
            serializer:
                A serializer instance containing the data submitted to
                the view.

        Returns:
            The newly created media resource.
        """
        km_user = get_object_or_404(
            models.KMUser,
            pk=self.kwargs.get('pk'))

        return serializer.save(km_user=km_user)


class PendingAccessorListView(generics.ListAPIView):
    """
    Endpoint for listing the accessors that the current user can accept.
    """
    permission_classes = (DRYPermissions,)
    serializer_class = serializers.KMUserAccessorSerializer

    def get_queryset(self):
        """
        Get the list of pending accessors for the requesting user.

        Returns:
            A queryset containing the ``KMUserAccessor`` instances that
            give access to the requesting user and are not yet accepted.
        """
        return self.request.user.km_user_accessors.filter(accepted=False)


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    get:
    Endpoint for retrieving the details of a specific profile.

    put:
    Endpoint for updating the details of a specific profile.

    patch:
    Endpoint for partially updating the details of a specific profile.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileDetailSerializer


class ProfileListView(generics.ListCreateAPIView):
    """
    get:
    Endpoint for listing the profiles of the specified Know Me user.

    post:
    Endpoint for creating a new profile for the specified Know Me user.
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
    get:
    Endpoint for retrieving the details of a specific profile item.

    put:
    Endpoint for updating the details of a specific profile item.

    patch:
    Endpoint for partially updating the details of a specific profile
    item.
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

        try:
            km_user = models.KMUser.objects.get(
                profile__topic__pk=self.kwargs.get('pk'))
        except models.KMUser.DoesNotExist:
            km_user = None

        context['km_user'] = km_user

        return context


class ProfileItemListView(generics.ListCreateAPIView):
    """
    get:
    Endpoint for listing the profile items in a specific topic.

    post:
    Endpoint for adding a new profile item to a specifc topic.
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

        pk = self.kwargs.get('pk', None)
        if pk is None:
            context['km_user'] = None
        else:
            context['km_user'] = models.KMUser.objects.get(
                profile__topic__pk=pk)

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
    get:
    Endpoint for retrieving the details of a specific profile topic.

    put:
    Endpoint for updating the details of a specific profile topic.

    patch:
    Endpoint for partially updating the details of a specific profile
    topic.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.ProfileTopic.objects.all()
    serializer_class = serializers.ProfileTopicSerializer


class ProfileTopicListView(generics.ListCreateAPIView):
    """
    get:
    Endpoint for listing the topics in a specific profile.

    post:
    Endpoint for adding a new topic to a specific profile.
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
