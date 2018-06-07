"""Filter backends for the ``know_me`` module.
"""

from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import filters

from know_me import models


class KMUserAccessFilterBackend(filters.BaseFilterBackend):
    """
    Filter for listing items owned by a Know Me user.

    Access to items is only granted if one of the following is true:
      1. The user ID provided is that of the requesting user
      2. There is an accessor granting the requesting user access to the
         user whose ID is provided in the request.
    """

    def filter_queryset(self, request, queryset, view):
        """
        Filter items for a list action.

        Args:
            request:
                The request being made.
            queryset:
                A queryset containing the objects to filter.
            view:
                The view being accessed.
        Returns:
            The provided queryset filtered to only include items owned
            by the user specified in the provided views arguments.
        """
        # Requesting user has access to KMUser
        query = Q(km_user_accessor__user_with_access=request.user)
        query &= Q(km_user_accessor__is_accepted=True)

        # Requesting user is KMUser
        query |= Q(user=request.user)

        # In rare cases, this query will return duplicate rows. See #343
        # for details.
        km_user_query = models.KMUser.objects.filter(query).distinct()

        km_user = get_object_or_404(
            km_user_query,
            pk=view.kwargs.get('pk'),
        )

        return queryset.filter(km_user=km_user)
