"""Serializers for authentication views.
"""

from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


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
