"""Serializers for authentication views.
"""

from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.
    """

    class Meta:
        extra_kwargs = {
            'password': {
                'style': {'input_type': 'password'},
                'write_only': True,
            },
        }
        fields = ('email', 'first_name', 'last_name', 'password')
        model = get_user_model()

    def create(self, validated_data):
        """
        Create a new user from the serializer's validated data.

        Args:
            validated_data:
                The data to create the new user from.

        Returns:
            The newly created ``User`` instance.
        """
        return get_user_model().objects.create_user(**validated_data)
