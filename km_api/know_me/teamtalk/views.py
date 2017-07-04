"""Views for the ``know_me.teamtalk`` module.
"""

from rest_framework import generics

from know_me.teamtalk import serializers


class LayerIdentityView(generics.CreateAPIView):
    """
    View for getting a Layer identity.
    """
    serializer_class = serializers.IdentitySerializer
