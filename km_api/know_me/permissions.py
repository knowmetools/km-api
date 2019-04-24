from django.conf import settings
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import permissions

from know_me import models


class HasKMUserAccess(permissions.IsAuthenticated):
    """
    Permission for allowing access to a Know Me user.
    """

    def has_permission(self, request, view):
        """
        Determine if the requesting user has access to the given view.

        If the requesting user is the Know Me user or has an accessor
        granting access, then they are given permission.

        Args:
            request:
                The request being made.
            view:
                The view being accessed.

        Returns:
            A boolean indicating if the requesting user has access to
            the specified view.
        """
        if not super().has_permission(request, view):
            return False

        km_user = get_object_or_404(models.KMUser, pk=view.kwargs.get("pk"))

        if km_user.user == request.user:
            return True

        try:
            accessor = km_user.km_user_accessors.get(
                is_accepted=True, user_with_access=request.user
            )
        except models.KMUserAccessor.DoesNotExist:
            raise Http404()

        if accessor.is_admin:
            return True

        return request.method in permissions.SAFE_METHODS


class HasPremium(permissions.IsAuthenticated):
    """
    Permission class to ensure the requesting user has an active Know Me
    premium subscription.
    """

    def has_permission(self, request, view):
        """
        Determine if the requesting user has an active premium
        subscription.

        Args:
            request:
                The request being made.
            view:
                The view being accessed.

        Returns:
            A boolean indicating if the requesting user has an active
            premium subscription.
        """
        # If premium is not required, bail out of the permission check.
        if not settings.KNOW_ME_PREMIUM_ENABLED:
            return True

        if not super().has_permission(request, view):
            return False

        return models.Subscription.objects.filter(
            is_active=True, user=request.user
        ).exists()


class OwnerHasPremium(permissions.BasePermission):
    """
    Permission class to ensure the owner of some object or collection
    has a premium subscription.
    """

    def has_object_permission(self, request, view, obj):
        """
        Determine if the requesting user has permission to access the
        given object.

        Args:
            request:
                The request being made.
            view:
                The view being accessed.
            obj:
                The object being accessed.

        Returns:
            A boolean indicating if the request should be allowed to
            continue.
        """
        # If premium is not required, bail out of the permission check.
        if not settings.KNOW_ME_PREMIUM_ENABLED:
            return True

        assert hasattr(view, "get_subscription_owner"), (
            "In order to use the `OwnerHasPremium` permission, the view must "
            "have a `get_subscription_owner(request, obj)` method that "
            "returns the user who owns the subscription that should be "
            "checked for the given object."
        )

        user = view.get_subscription_owner(request, obj)

        if not models.Subscription.objects.filter(
            is_active=True, user=user
        ).exists():
            raise Http404

        return True
