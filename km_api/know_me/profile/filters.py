from rest_framework import filters

from know_me.models import KMUser


class ProfileFilterBackend(filters.BaseFilterBackend):
    """
    Filter for listing profile items.

    This filter depends on ``KMUserAccessFilterBackend`` already being
    applied.
    """

    def filter_queryset(self, request, queryset, view):
        """
        Get the profiles accessible by the requesting user.

        If the profile is marked as private, only the owner or account
        admins can view it. Otherwise, the owner or any shared user can
        access the profile.

        Args:
            request:
                The request to filter for.
            queryset:
                The queryset to filter.
            view:
                The view being accessed.

        Returns:
            A queryset containing the profiles accessible to the
            requesting user.
        """
        km_user = KMUser.objects.get(pk=view.kwargs.get("pk"))

        if request.user == km_user.user:
            return queryset

        if km_user.km_user_accessors.filter(
            is_admin=True, user_with_access=request.user
        ).exists():
            return queryset

        return queryset.filter(is_private=False)
