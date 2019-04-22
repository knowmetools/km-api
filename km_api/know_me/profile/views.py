from dry_rest_permissions.generics import DRYPermissions

from rest_framework import generics

from know_me.filters import KMUserAccessFilterBackend
from know_me.models import KMUser
from know_me.permissions import HasKMUserAccess
from know_me.profile import filters, models, permissions, serializers
from rest_order.generics import SortView
from rest_order.serializers import create_sort_serializer


class ListEntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete:
    Delete a specific list entry.

    get:
    Retrieve a specific list entry's information.

    patch:
    Partially update a specific list entry's information.

    put:
    Update a specific list entry's information.
    """

    permission_classes = (DRYPermissions,)
    queryset = models.ListEntry.objects.all()
    serializer_class = serializers.ListEntrySerializer


class ListEntryListView(SortView, generics.ListCreateAPIView):
    """
    get:
    Get a list of the list entries belonging to a specific profile item.

    post:
    Add a new list entry to a specific profile item.

    put:
    Set the order of the list entries relative to their parent profile
    item.
    """

    permission_classes = (
        DRYPermissions,
        permissions.HasListEntryListPermissions,
    )
    serializer_class = serializers.ListEntrySerializer
    sort_child_name = "list_entries"
    sort_parent = models.ProfileItem
    sort_serializer = create_sort_serializer(models.ListEntry)

    def get_queryset(self):
        """
        Get the list entries for a specific request.

        Most of the complexity here is handled by the
        ``HasListEntryListPermissions`` permission class. Because of it,
        we can assume the profile item with the provided primary key
        exists and is accessible to the requesting user.

        Returns:
            A queryset containing the list entries that belong to the
            profile item whose ID is given in the URL.
        """
        return models.ListEntry.objects.filter(
            profile_item=self.kwargs.get("pk")
        )

    def perform_create(self, serializer):
        """
        Create a new list entry for the given profile item.

        Args:
            serializer:
                An instance of the view's serializer class containing
                the data passed to the view.

        Returns:
            The newly created list entry.
        """
        item = models.ProfileItem.objects.get(pk=self.kwargs.get("pk"))

        return serializer.save(profile_item=item)


class MediaResourceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete:
    Delete a specific media resource.

    get:
    Retrieve information about a specific media resource.

    patch:
    Partially update the information for a specific media resource.

    put:
    Update the information for a specific media resource.
    """

    permission_classes = (DRYPermissions,)
    queryset = models.MediaResource.objects.all()
    serializer_class = serializers.MediaResourceSerializer


class MediaResourceListView(generics.ListCreateAPIView):
    """
    get:
    Get a list of the media resources belonging to a specific Know Me
    user.

    post:
    Create a new media resource owned by the specified Know Me user.
    """

    filter_backends = (KMUserAccessFilterBackend,)
    permission_classes = (DRYPermissions, HasKMUserAccess)
    queryset = models.MediaResource.objects.all()
    serializer_class = serializers.MediaResourceSerializer

    def get_queryset(self):
        """
        Get the media resources for a specific request.

        Returns:
            If a category is given in the URL, only its media resources
            are returned. Otherwise, all media resources are returned.
        """
        queryset = super().get_queryset()

        category_id = self.request.query_params.get("category", None)
        if category_id is not None:
            queryset = queryset.filter(category__id=category_id)

        return queryset

    def perform_create(self, serializer):
        """
        Create a new media resource.

        Args:
            serializer:
                An instance of the view's serializer class containing
                the data passed to the view.

        Returns:
            The newly created media resource.
        """
        km_user = KMUser.objects.get(pk=self.kwargs.get("pk"))

        return serializer.save(km_user=km_user)


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete:
    Delete a specific profile.

    get:
    Retrieve a specific profile's information.

    patch:
    Partially update a specific profile.

    put:
    Update a specific profile.
    """

    permission_classes = (DRYPermissions,)
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileDetailSerializer


class ProfileListView(SortView, generics.ListCreateAPIView):
    """
    get:
    List the profiles of a specific Know Me user.

    post:
    Create a new profile for a specific Know Me user.

    Only team leaders or the Know Me user themself can create a new
    profile.

    put:
    Update the order of the user's profiles.

    Only team leaders or the Know Me user themself can update the order.
    """

    filter_backends = (KMUserAccessFilterBackend, filters.ProfileFilterBackend)
    permission_classes = (DRYPermissions, HasKMUserAccess)
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileListSerializer
    sort_child_name = "profiles"
    sort_parent = KMUser
    sort_serializer = create_sort_serializer(models.Profile)

    def perform_create(self, serializer):
        """
        Create a new profile.

        Args:
            serializer:
                A serializer instance containing the data passed to the
                view.

        Returns:
            The newly created profile.
        """
        km_user = KMUser.objects.get(pk=self.kwargs.get("pk"))

        return serializer.save(km_user=km_user)


class ProfileItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete:
    Delete a specific profile item.

    get:
    Retrieve a specific profile item's information.

    patch:
    Partially update a specific profile item's information.

    put:
    Update a specific profile item's information.
    """

    permission_classes = (DRYPermissions,)
    queryset = models.ProfileItem.objects.all()
    serializer_class = serializers.ProfileItemDetailSerializer


class ProfileItemListView(SortView, generics.ListCreateAPIView):
    """
    get:
    List the profile items that belong to the specified topic.

    post:
    Create a new profile item for the specified topic.

    put:
    Set the order of the items in the specified topic.
    """

    permission_classes = (
        DRYPermissions,
        permissions.HasProfileItemListPermissions,
    )
    serializer_class = serializers.ProfileItemDetailSerializer
    sort_child_name = "items"
    sort_parent = models.ProfileTopic
    sort_serializer = create_sort_serializer(models.ProfileItem)

    def get_queryset(self):
        """
        Get the items that belong to the specified topic.

        Much of the complexity here is handled by the
        ``HasProfileItemListPermissions`` class. Because of it, we can
        assume that the topic exists and is accessible by the requesting
        user.

        Returns:
            A queryset containing the items belonging to the topic whose
            ID is given in the URL.
        """
        return models.ProfileItem.objects.filter(topic=self.kwargs.get("pk"))

    def get_serializer_class(self):
        """
        Get the appropriate serializer class for the current request.

        Returns:
            The profile item detail serializer if the request is missing
            or it is a POST request. The profile item list serializer is
            used otherwise.
        """
        if self.request is None or self.request.method == "POST":
            return serializers.ProfileItemDetailSerializer

        return serializers.ProfileItemListSerializer

    def get_serializer_context(self):
        """
        Get additional context for the view's serializer.

        Returns:
            A dictionary containing the context used to instantiate the
            view's serializer.
        """
        context = super().get_serializer_context()

        pk = self.kwargs.get("pk")
        if pk is not None:
            context["km_user"] = KMUser.objects.get(profile__topic__pk=pk)
        else:
            context["km_user"] = None

        return context

    def perform_create(self, serializer):
        """
        Create a new item associated with the specified topic.

        Args:
            serializer:
                An instance of the view's serializer class containing
                the data passed to the view.

        Returns:
            The newly created profile item instance.
        """
        topic = models.ProfileTopic.objects.get(pk=self.kwargs.get("pk"))

        return serializer.save(topic=topic)


class ProfileTopicDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete:
    Delete a specific profile topic.

    get:
    Retrieve a specific profile topic's information.

    patch:
    Partially update a specific profile topic's information.

    put:
    Update a specific profile topic's information.
    """

    permission_classes = (DRYPermissions,)
    queryset = models.ProfileTopic.objects.all()
    serializer_class = serializers.ProfileTopicListSerializer


class ProfileTopicListView(SortView, generics.ListCreateAPIView):
    """
    get:
    List the topics that belong to the specified profile.

    post:
    Create a new topic in the specified profile.

    put:
    Set the order of the topics in the specified profile.
    """

    permission_classes = (
        DRYPermissions,
        permissions.HasProfileTopicListPermissions,
    )
    sort_child_name = "topics"
    sort_parent = models.Profile
    sort_serializer = create_sort_serializer(models.ProfileTopic)

    def get_queryset(self):
        """
        Get the topics that belong to the specified profile.

        Much of the complexity here is handled by the
        ``HasProfileTopicListPermissions`` class. Because of it, we can
        assume that the profile exists and is accessible by the
        requesting user.

        Returns:
            A queryset containing the topics belonging to the profile
            whose ID is given in the URL.
        """
        return models.ProfileTopic.objects.filter(
            profile__pk=self.kwargs.get("pk")
        )

    def get_serializer_class(self):
        """
        Get the correct serializer class for the given request.

        Returns:
            The profile topic detail serializer if there is no request
            or it is a POST request and the list serializer otherwise.
        """
        if self.request is None or self.request.method == "POST":
            return serializers.ProfileTopicDetailSerializer

        return serializers.ProfileTopicListSerializer

    def perform_create(self, serializer):
        """
        Create a new topic associated with the specified profile.

        Args:
            serializer:
                An instance of the view's serializer class containing
                the data passed to the view.

        Returns:
            The newly created profile topic instance.
        """
        profile = models.Profile.objects.get(pk=self.kwargs.get("pk"))

        return serializer.save(profile=profile)
