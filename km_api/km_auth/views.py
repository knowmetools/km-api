"""Views related to authentication.
"""

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken

from km_auth import serializers


# We extend from 'GenericAPIView' so that the generated docs can access
# the view's serializer fields.
class ObtainTokenView(ObtainAuthToken, generics.GenericAPIView):
    """
    Endpoint for obtaining an authentication token.

    The user provides their email and password and a token that can be
    used to authenticate further requests is returned.
    """
    serializer_class = serializers.TokenSerializer
