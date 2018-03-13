from dry_rest_permissions.generics import DRYPermissions

from rest_framework import generics

from know_me.filters import KMUserAccessFilterBackend
from know_me.journal import models, serializers
from know_me.models import KMUser
from know_me.permissions import HasKMUserAccess


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

    post:
    Create a new journal entry for the specified Know Me user.
    """
    filter_backends = (KMUserAccessFilterBackend,)
    permission_classes = (
        DRYPermissions,
        HasKMUserAccess)
    queryset = models.Entry.objects.all()

    def get_serializer_class(self):
        """
        Get the appropriate serializer for the view's request.

        Returns:
            The entry detail serializer for a POST request and the list
            serializer for any other method.
        """
        if self.request.method == 'POST':
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
        km_user = KMUser.objects.get(pk=self.kwargs.get('pk'))

        return serializer.save(km_user=km_user)
