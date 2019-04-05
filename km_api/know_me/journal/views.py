from django_filters import rest_framework as filters

from dry_rest_permissions.generics import DRYPermissions

from rest_framework import generics, pagination

from watson import search as watson

from know_me.filters import KMUserAccessFilterBackend
from know_me.journal import models, permissions, serializers
from know_me.models import KMUser
from know_me.permissions import HasKMUserAccess, OwnerHasPremium
from permission_utils.view_mixins import DocumentActionMixin


class EntryCommentDetailView(
    DocumentActionMixin, generics.RetrieveUpdateDestroyAPIView
):
    """
    delete:
    Delete a specific comment on a journal entry.

    The user who made the comment, the journal owner, and any users with
    admin rights on the journal can delete a comment.

    get:
    Retrieve information about a specific comment.

    patch:
    Partially update a comment.

    Only the user who made the comment is allowed to update it.

    put:
    Update a comment.

    Only the user who made the comment is allowed to update it.
    """

    permission_classes = (DRYPermissions, OwnerHasPremium)
    queryset = models.EntryComment.objects.all()
    serializer_class = serializers.EntryCommentSerializer

    @staticmethod
    def get_subscription_owner(request, comment):
        """
        Get the user to check for an active premium subscription.

        Args:
            request:
                The request being made.
            comment:
                The comment being accessed.

        Returns:
            The user who owns the journal that the comment was made in.
        """
        return comment.entry.km_user.user


class EntryCommentListView(generics.ListCreateAPIView):
    """
    get:
    List the comments attached to a journal entry.

    post:
    Add a new comment to a specific journal entry.
    """

    permission_classes = (
        DRYPermissions,
        permissions.HasEntryCommentListPermissions,
    )
    serializer_class = serializers.EntryCommentSerializer

    def get_queryset(self):
        """
        Get the comments attached to the journal entry given in the URL.

        Returns:
            A queryset containing the comments attached to the journal
            entry whose ID is specified in the URL.
        """
        entry = models.Entry.objects.get(pk=self.kwargs.get("pk"))

        return entry.comments.all()

    def perform_create(self, serializer):
        """
        Create a new comment attached to the specified journal entry.

        Args:
            serializer:
                An instance of the view's serializer class containing
                the data passed to the view.

        Returns:
            The newly created comment instance.
        """
        entry = models.Entry.objects.get(pk=self.kwargs.get("pk"))

        return serializer.save(entry=entry, user=self.request.user)


class EntryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete:
    Delete a specific journal entry.

    get:
    Retrieve the information of a specific journal entry.

    patch:
    Partially update a specific journal entry.

    put:
    Update a specific journal entry.
    """

    permission_classes = (DRYPermissions,)
    queryset = models.Entry.objects.all()
    serializer_class = serializers.EntryDetailSerializer


class EntryListView(generics.ListCreateAPIView):
    """
    get:
    List the journal entries of a specific Know Me user.

    In addition to the below filters, a keyword search may also be
    performed by passing the search term as a GET parameter named `q`.

    post:
    Create a new journal entry for the specified Know Me user.
    """

    filter_backends = (KMUserAccessFilterBackend, filters.DjangoFilterBackend)
    filter_fields = {"created_at": ["gte", "lte"]}
    pagination_class = pagination.PageNumberPagination
    permission_classes = (DRYPermissions, HasKMUserAccess)
    queryset = models.Entry.objects.all()

    def filter_queryset(self, queryset):
        """
        Filter the queryset based on the provided parameters.

        Args:
            The queryset to filter.

        Returns:
            The filtered queryset.
        """
        queryset = super().filter_queryset(queryset)

        search_term = self.request.query_params.get("q", None)
        if search_term is not None:
            queryset = watson.filter(queryset, search_term)

        return queryset

    def get_serializer_class(self):
        """
        Get the appropriate serializer for the view's request.

        Returns:
            The entry detail serializer for a POST request and the list
            serializer for any other method.
        """
        if self.request is None or self.request.method == "POST":
            return serializers.EntryDetailSerializer

        return serializers.EntryListSerializer

    def perform_create(self, serializer):
        """
        Create a new Journal Entry.

        The Know Me user referenced in the URL is passed to the
        serializer as the owner of the new entry. We can assume that
        user exists and is accessible due to the permission classes on
        the view.

        Args:
            serializer:
                An instance of the view's serializer class containing
                the data passed to the view.

        Returns:
            The newly created serializer instance.
        """
        km_user = KMUser.objects.get(pk=self.kwargs.get("pk"))

        return serializer.save(km_user=km_user)
