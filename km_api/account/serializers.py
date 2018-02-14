"""Serializers for account tasks.
"""

from django.contrib.auth import get_user_model

from rest_email_auth.serializers import (
    RegistrationSerializer as BaseRegistrationSerializer)

from rest_framework import serializers


class RegistrationSerializer(BaseRegistrationSerializer):
    """
    Serializer for registering a new user.
    """

    class Meta:
        extra_kwargs = {
            'password': {
                'style': {
                    'input_type': 'password',
                },
                'write_only': True,
            }
        }
        fields = ('email', 'password', 'first_name', 'last_name')
        model = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for ``User`` instances.

    The serializer allows for updating of basic information like email
    or name. It does **not** allow for changing the user's password.
    """

    class Meta:
        extra_kwargs = {
            'first_name': {
                'help_text': "The user's first name.",
            },
            'last_name': {
                'help_text': "The user's last name.",
            },
        }
        fields = ('id', 'first_name', 'last_name')
        model = get_user_model()
