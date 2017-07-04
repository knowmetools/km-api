"""Serializers for the ``know_me.teamtalk`` module.
"""

from rest_framework import serializers

from know_me.teamtalk import layer


class IdentitySerializer(serializers.Serializer):
    """
    Serializer for obtaining an identity from Layer.

    This serializer takes a nonce provided by Layer and obtains an
    identity for the user making the request. This identity can then be
    used to participate in conversations.
    """
    identity_token = serializers.CharField(read_only=True)
    nonce = serializers.CharField(write_only=True)

    def save(self):
        """
        Generate an identity for the requesting user.
        """
        self.validated_data['identity_token'] = layer.generate_identity_token(
            self.context['request'].user,
            self.validated_data['nonce'])
