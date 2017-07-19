"""Model mixins for the ``know_me`` module.
"""


class IsAuthenticatedMixin:
    """
    Model mixin that requires users to be authenticated.

    Using DRY Rest Permissions' system, this mixin requires users to be
    authenticated to have read or write access.
    """

    @staticmethod
    def has_read_permission(request):
        """
        Check if a request has read permission on the class.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user is authenticated and
                ``False`` otherwise.
        """
        return request.user.is_authenticated()

    @staticmethod
    def has_write_permission(request):
        """
        Check if a request has write permission on the class.

        Args:
            request:
                The request to check permissions for.

        Returns:
            bool:
                ``True`` if the requesting user is authenticated and
                ``False`` otherwise.
        """
        return request.user.is_authenticated()
