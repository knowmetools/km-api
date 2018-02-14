"""Serializers for authentication views.
"""

import logging

from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from km_auth import layer


logger = logging.getLogger(__name__)


class LayerIdentitySerializer(serializers.Serializer):
    """
    Serializer for obtaining an identity from Layer.

    This serializer takes a nonce provided by Layer and obtains an
    identity for the user making the request. This identity can then be
    used to participate in conversations.
    """
    identity_token = serializers.CharField(read_only=True)
    nonce = serializers.CharField(
        help_text=("The nonce provided by Layer. See the following URL for "
                   "more information: https://docs.layer.com/reference/"
                   "client_api/authentication.out#introduction"),
        write_only=True)

    def save(self):
        """
        Generate an identity for the requesting user.
        """
        self.validated_data['identity_token'] = layer.generate_identity_token(
            self.context['request'].user,
            self.validated_data['nonce'])


class TokenSerializer(serializers.Serializer):
    """
    Serializer for obtaining an auth token.

    The actual generation of the auth token is intended to be handled by
    the view that utilizes this serializer.
    """
    email = serializers.EmailField(help_text="The user's email address.")
    password = serializers.CharField(
        help_text="The user's password",
        style={'input_type': 'password'})

    def validate(self, data):
        """
        Ensure that the requesting user is allowed to obtain a token.

        Returns:
            dict:
                The validated data.

        Raises:
            ValidationError:
                If the provided credentials are invalid.
            ValidationError:
                If the requesting user does not have a verified email
                address.
        """
        user = authenticate(**data)

        if not user:
            raise serializers.ValidationError(
                _('Invalid credentials. Check your email and password and try'
                  'again.'))

        data['user'] = user

        return data
