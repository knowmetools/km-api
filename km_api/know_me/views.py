"""Views for the ``know_me`` module.
"""

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

from dry_rest_permissions.generics import DRYGlobalPermissions, DRYPermissions

from rest_framework import generics, pagination, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from know_me import models, serializers


class AccessorAcceptView(generics.GenericAPIView):
    """
    post:
    Accept the accessor with the specified ID.

    Only the user granted access by the accessor may accept it.
    """
    action = 'accept'
    permission_classes = (DRYPermissions,)
    queryset = models.KMUserAccessor.objects.all()
    # We need a serializer class because dry-rest-permissions uses the
    # serializer to determine the model used for the view.
    serializer_class = serializers.KMUserAccessorAcceptSerializer

    def post(self, request, *args, **kwargs):
        accessor = self.get_object()

        accessor.is_accepted = True
        accessor.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


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
    permission_classes = (DRYPermissions,)
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
    permission_classes = (DRYPermissions,)
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


class ConfigDetailView(generics.RetrieveUpdateAPIView):
    """
    get:
    Retrieve the configuration for the Know Me app.

    patch:
    Partially update the configuration for Know Me.

    Only staff users may perform this action.

    put:
    Update the configuration for Know Me.

    Only staff users may perform this action.
    """
    permission_classes = (DRYGlobalPermissions,)
    serializer_class = serializers.ConfigSerializer

    def get_object(self):
        """
        Return the config instance singleton.
        """
        config = models.Config.get_solo()

        self.check_object_permissions(self.request, config)

        return config


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
        query &= Q(km_user_accessor__is_accepted=True)

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


class LegacyUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    delete:
    Delete the specified legacy user.

    get:
    Retrieve the specified legacy user's information.

    patch:
    Partially update the specified legacy user's information.

    put:
    Update the specified legacy user's information.
    """
    permission_classes = (DRYGlobalPermissions,)
    queryset = models.LegacyUser.objects.all()
    serializer_class = serializers.LegacyUserSerializer


class LegacyUserListView(generics.ListCreateAPIView):
    """
    get:
    Get a list of all legacy users.

    post:
    Add a new legacy user.
    """
    pagination_class = pagination.PageNumberPagination
    permission_classes = (DRYPermissions,)
    queryset = models.LegacyUser.objects.all()
    serializer_class = serializers.LegacyUserSerializer


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
        return self.request.user.km_user_accessors.filter(is_accepted=False)
