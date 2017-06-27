"""Serializers for authentication views.
"""

from django.contrib.auth import get_user_model

from rest_framework import serializers


class UserDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving, creating, and updating ``User`` objects.
    """

    class Meta:
        extra_kwargs = {
            'password': {
                'style': {'input_type': 'password'},
                'write_only': True,
            },
        }
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
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

    def update(self, user, validated_data):
        """
        Update a user's details.

        Args:
            user:
                The user being updated.
            validated_data:
                The data to update the user with.

        Returns:
            The edited ``User`` instance.
        """
        user.email = validated_data.get('email', user.email)
        user.first_name = validated_data.get('first_name', user.first_name)
        user.last_name = validated_data.get('last_name', user.last_name)

        password = validated_data.get('password', None)
        if password is not None:
            user.set_password(password)

        user.save()

        return user
