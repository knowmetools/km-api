"""Views related to authentication.
"""

from django.contrib.auth import get_user_model

from rest_framework import generics

from km_auth import permissions, serializers


class UserRegistrationView(generics.CreateAPIView):
    """
    View for registering new users.
    """
    permission_classes = (permissions.IsAnonymous,)
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserDetailSerializer
