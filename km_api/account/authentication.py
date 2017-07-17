"""Authentication backends provided by the ``account`` module.
"""

from django.contrib.auth import get_user_model

from account import models


class AuthenticationBackend:
    """
    Log in users with multiple email addresses.

    This backend allows a user to authenticate with any verified email
    attached to their account.
    """

    def authenticate(self, request, email=None, password=None, username=None):
        """
        Authenticate a user's credentials.

        .. note::

            The email and password fields are optional to allow for
            multiple authentication backends with conflicting parameters
            to be used.

        Args:
            request:
                The request being made.
            email (:obj:`str`, optional):
                The user's email address.
            password (:obj:`str`, optional):
                The user's password.
            username (:obj:`str`, optional):
                An alias for the ``email`` field. This allows us to
                continue using Django's authentication views since they
                provide a ``username`` instead of an email.

        Returns:
            The user instance corresponding to the provided credentials,
            or ``None`` if the credentials are invalid.
        """
        email = email or username

        try:
            email_instance = models.EmailAddress.objects.get(email=email)
        except models.EmailAddress.DoesNotExist:
            return None

        user = email_instance.user

        if user.check_password(password) and user.is_active:
            return user

        return None

    def get_user(self, id):
        """
        Get the user with the given ID.

        Args:
            id (int):
                The ID of the user to get.

        Returns:
            The user with the given ID if they exist and ``None``
            otherwise.
        """
        try:
            return get_user_model().objects.get(id=id)
        except get_user_model().DoesNotExist:
            return None
