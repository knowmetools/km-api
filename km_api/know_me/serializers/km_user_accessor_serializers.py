"""Serializers for the ``KMUserAccessor`` model.
"""

from rest_framework import serializers

from know_me import models
from .km_user_serializers import KMUserDetailSerializer


class KMUserAccessorSerializer(serializers.ModelSerializer):
    """
    Serializer for ``KMUserAccessor`` instances.
    """
    km_user = KMUserDetailSerializer(read_only=True)

    class Meta:
        fields = (
            'accepted',
            'can_write',
            'email',
            'has_private_profile_access',
            'km_user',
        )
        model = models.KMUserAccessor
        read_only_fields = ('accepted',)

    def create(self, validated_data):
        """
        Create a new accessor for a Know Me user.

        Args:
            validated_data (dict):
                The data to create the accessor from.

        Returns:
            The newly created ``KMUserAccessor`` instance.
        """
        km_user = validated_data.pop('km_user')
        email = validated_data.pop('email')

        return km_user.share(email, **validated_data)
