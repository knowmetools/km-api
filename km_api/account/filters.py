"""Filter backends for the ``account`` module.
"""

from dry_rest_permissions.generics import DRYPermissionFiltersBase


class EmailFilterBackend(DRYPermissionFiltersBase):
    """
    Filtering backend for listing email addresses.
    """

    def filter_list_queryset(self, request, queryset, view):
        """
        Filter emails for a list action.

        Args:
            request:
                The request being made.
            queryset:
                The base queryset to filter from.
            view:
                The view being accessed.

        Returns:
            The provided queryset filtered to only include email's
            associated with the requesting user.
        """
        return queryset.filter(user=request.user)
