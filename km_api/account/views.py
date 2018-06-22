"""Views for the ``account`` module.
"""

from django.contrib.auth import get_user_model

from rest_framework import generics, pagination
from rest_framework.permissions import IsAuthenticated

from account import permissions, serializers


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


class UserListView(generics.ListAPIView):
    """
    get:
    List all users.
    """
    pagination_class = pagination.PageNumberPagination
    permission_classes = (permissions.IsStaff,)
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserListSerializer
