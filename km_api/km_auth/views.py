"""Views related to authentication.
"""

from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from km_auth import permissions, serializers


class UserDetailView(generics.RetrieveUpdateAPIView):
    """
    View for retrieving and updating a user's details.
    """
    permission_classes = (IsAuthenticated,)
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserDetailSerializer

    def get_object(self):
        """
        Get the user we're displaying the details of.

        Returns:
            The user making the current request.
        """
        return self.request.user


class UserRegistrationView(generics.CreateAPIView):
    """
    View for registering new users.
    """
    permission_classes = (permissions.IsAnonymous,)
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserDetailSerializer
