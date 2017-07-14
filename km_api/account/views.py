"""Views for the ``account`` module.
"""

from django.contrib.auth import update_session_auth_hash
from django.utils.translation import ugettext_lazy as _

from dry_rest_permissions.generics import DRYPermissions

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from account import models, serializers


class EmailDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View for retrieving, updating, or deleting a specific email address.
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
    View for listing the requesting user's email addresses.
    """
    permission_classes = (DRYPermissions,)
    queryset = models.EmailAddress.objects.all()
    serializer_class = serializers.EmailSerializer


class EmailVerificationView(generics.GenericAPIView):
    """
    View for verifying an email address.
    """
    serializer_class = serializers.EmailVerificationSerializer

    def post(self, request):
        """
        Verify an email with a verification key.

        Args:
            request:
                The request being made.

        Returns:
            A response with a status code indicating if the request was
            successful.
        """
        serializer = self.get_serializer(data=request.POST)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(generics.GenericAPIView):
    """
    View for changing the user's password.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PasswordChangeSerializer

    def post(self, request):
        """
        Change the requesting user's password.

        Args:
            request:
                The request being made.

        Returns:
            A response with a status code indicating if the request was
            successful.
        """
        serializer = self.get_serializer(data=request.POST)

        if serializer.is_valid():
            serializer.save()

            update_session_auth_hash(request, request.user)

            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating a user's information.

    This view is only able to update account information such as email
    address or name. To change a user's password, see
    :class:`.PasswordChangeView`.
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
