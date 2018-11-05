"""Views for the ``know_me`` module.
"""

from django.db.models import Case, Q, PositiveSmallIntegerField, Value, When
from django.shortcuts import get_object_or_404
from dry_rest_permissions.generics import DRYGlobalPermissions, DRYPermissions
from rest_framework import generics, pagination, status
from rest_framework.response import Response

from know_me import models, serializers
from know_me.serializers import subscription_serializers
from permission_utils.view_mixins import DocumentActionMixin


class AppleSubscriptionView(generics.RetrieveAPIView):
    """
    get:
    Retrieve the current user's Apple subscription. If the user does not
    have an Apple subscription, a 404 response is returned.

    put:
    Set the Apple subscription for the current user by providing the
    receipt from Apple for the purchase.
    """
    permission_classes = (DRYPermissions,)
    serializer_class = subscription_serializers.AppleSubscriptionSerializer

    def get_object(self):
        """
        Get the Apple subscription data instance that belongs to the
        requesting user.

        Returns:
            The ``SubscriptionDataApple`` instance that belongs to the
            requesting user.
        """
        return get_object_or_404(
            models.SubscriptionAppleData,
            subscription__user=self.request.user,
        )

    def put(self, request, *args, **kwargs):
        # If the user has an existing Apple subscription, update it
        try:
            instance = models.SubscriptionAppleData.objects.get(
                subscription__user=self.request.user,
            )
        except models.SubscriptionAppleData.DoesNotExist:
            instance = None

        # Validate the data provided to the serializer before we create
        # the base subscription (if necessary).
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        base_subscription, _ = models.Subscription.objects.get_or_create(
            user=self.request.user,
            defaults={'is_active': True},
        )
        serializer.save(subscription=base_subscription)

        return Response(serializer.data)


class AccessorAcceptView(generics.GenericAPIView):
    """
    post:
    Accept the accessor with the specified ID.

    Only the user granted access by the accessor may accept it.
    """
    # We use the global permissions check because the normal check
    # assumes we're checking write permissions for a POST request.
    permission_classes = (DRYGlobalPermissions,)
    queryset = models.KMUserAccessor.objects.all()
    # We need a serializer class because dry-rest-permissions uses the
    # serializer to determine the model used for the view.
    serializer_class = serializers.KMUserAccessorAcceptSerializer

    def check_object_permissions(self, request, obj):
        """
        Check permissions on the accessor being accessed.

        Only the user granted access by the accessor has permission to
        accept the accessor.

        Args:
            request:
                The request being made.
            obj:
                The ``KMUserAccessor`` instance being accepted.
        """
        super().check_object_permissions(request, obj)

        if not obj.has_object_accept_permission(request):
            self.permission_denied(request)

    def post(self, request, *args, **kwargs):
        accessor = self.get_object()

        accessor.is_accepted = True
        accessor.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class AcceptedAccessorListView(generics.ListAPIView):
    """
    get:
    Retrieve the accessors granting the requesting user access to other
    users' accounts that have been accepted.
    """
    permission_classes = (DRYPermissions,)
    serializer_class = serializers.KMUserAccessorSerializer

    def get_queryset(self):
        """
        Get the accessors accepted by the requesting user.

        Returns:
            A queryset containing the accessors accepted by the
            requesting user.
        """
        return self.request.user.km_user_accessors.filter(is_accepted=True)


class AccessorDetailView(
        DocumentActionMixin,
        generics.RetrieveUpdateDestroyAPIView):
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


class KMUserListView(generics.ListAPIView):
    """
    get:
    Endpoint for listing the Know Me users that the current user has
    access to.

    The Know Me user owned by the requesting user is guaranteed to be
    the first element returned.
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
        filter_args = Q(km_user_accessor__user_with_access=self.request.user)
        filter_args &= Q(km_user_accessor__is_accepted=True)

        # Requesting user is the user
        filter_args |= Q(user=self.request.user)

        query = models.KMUser.objects.filter(filter_args).distinct()

        # Allow us to sort the query with the requesting user's Know Me
        # user first. See conditional expression documentation:
        # https://docs.djangoproject.com/en/dev/ref/models/conditional-expressions/
        query = query.annotate(
            owned_by_user=Case(
                When(
                    user=self.request.user,
                    then=Value(1)
                ),
                default=Value(0),
                output_field=PositiveSmallIntegerField(),
            ),
        )

        return query.order_by('-owned_by_user', 'created_at')


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
