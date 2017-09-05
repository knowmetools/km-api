"""Serializers for the ``KMUserAccessor`` model.
"""

from rest_framework import serializers

from know_me import models
from .km_user_serializers import KMUserDetailSerializer


class KMUserAccessorSerializer(serializers.ModelSerializer):
    """
    Serializer for multiple ``KMUserAccessor`` instances.
    """
    km_user = KMUserDetailSerializer(read_only=True)
    user_with_access_email = serializers.EmailField(
            source='user_with_access.email',
            read_only=True)

    class Meta:
        fields = (
            'accepted',
            'can_write',
            'has_private_profile_access',
            'km_user',
            'user_with_access_email',)
        model = models.KMUserAccessor
