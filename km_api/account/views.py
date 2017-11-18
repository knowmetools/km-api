"""Views for the ``account`` module.
"""

from django.contrib.auth import update_session_auth_hash
from django.utils.translation import ugettext_lazy as _

from dry_rest_permissions.generics import DRYPermissions

from rest_framework import generics, status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account import models, serializers
import generic_rest_views


class EmailActionListView(views.APIView):
    """
    Endpoint for listing the available actions for when an email address
    is confirmed.

    These actions can be specified when creating a new email address to
    control what happens when the email is confirmed.
    """
    def get(self, request):
        serializer = serializers.EmailVerifiedActionSerializer(
            models.EmailAddress.VERIFIED_ACTION_CHOICES,
            many=True)

        return Response(serializer.data)


class EmailDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    get:
    Endpoint for retrieving the details of a specific email address.

    put:
    Endpoint for updating the details of a specific email address.

    patch:
    Endpoint for partially updating the details of a specific email address.

    delete:
    Endpoint for deleting a specific email address.

    This call will only work if the email address is not the account's
    primary email. To delete the primary email address, the user must
    switch their primary to a different address and then delete the old
    primary.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.EmailAddress.objects.all()
    serializer_class = serializers.EmailSerializer

    generic_messages = {
        'delete_primary': _("This email address cannot be deleted because it "
                            "is the primary email for the account."),
    }

    def destroy(self, request, pk=None):
        """
        Delete the email address with the provided ID.

        Args:
            request:
                The request being made.

            pk (int):
                The primary key of the email address to delete.

        Returns:
            A ``204`` status code if the object was successfully
            deleted. If the email is the user's primary email, a ``409``
            status is returned. If there is no email address with the
            given primary key, a ``404`` status is returned.
        """
        instance = self.get_object()

        if instance.primary:
            return Response(
                {'non_field_errors': self.generic_messages['delete_primary']},
                status=status.HTTP_409_CONFLICT)

        return super().destroy(request, pk=pk)


class EmailListView(generics.ListCreateAPIView):
    """
    get:
    List the email addresses that belong to the current user.

    post:
    Add a new email address owned by the current user.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.EmailAddress.objects.all()
    serializer_class = serializers.EmailSerializer


class EmailVerificationView(generic_rest_views.SerializerSaveView):
    """
    Endpoint for verifying ownership of an email address.

    By providing a token that was sent to the email we can confirm that
    the user actually has access to the account.
    """
    serializer_class = serializers.EmailVerificationSerializer


class PasswordChangeView(generic_rest_views.SerializerSaveView):
    """
    Endpoint for changing a user's password.

    This endpoint allows for using the user's previous password to set a
    new one, or for using a password reset token to reset the user's
    password.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PasswordChangeSerializer

    def post_save(self):
        """
        Update session auth hash after the user's password is changed.
        """
        update_session_auth_hash(self.request, self.request.user)


class PasswordResetView(generic_rest_views.SerializerSaveView):
    """
    Endpoint for requesting a password reset for a user.
    """
    serializer_class = serializers.PasswordResetSerializer


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    get:
    Endpoint for retrieving the current user's information.

    put:
    Endpoint for updating the current user's information.

    patch:
    Endpoint for partially updating the current user's information.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get_object(self):
        """
        Get the user making the request.

        Returns:
            The user making the request.
        """
        return self.request.user
