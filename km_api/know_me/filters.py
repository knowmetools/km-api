"""Filter backends for the ``know_me`` module.
"""

from dry_rest_permissions.generics import DRYPermissionFiltersBase


class ProfileFilterBackend(DRYPermissionFiltersBase):
    """
    Filter for listing ``Profile`` instances.
    """

    def filter_list_queryset(self, request, queryset, view):
        """
        Filter profiles for a ``list`` action.

        Args:
            request:
                The request being made.
            queryset:
                A queryset containing the objects to filter.
            view:
                The view being accessed.

        Returns:
            A queryset containing the profiles accessible to the user
            making the request.
        """
        return queryset.filter(user=request.user)
