"""Serializers for the ``ProfileGroup`` model.
"""

from rest_framework import serializers

from know_me import models


class ProfileGroupListSerializer(serializers.ModelSerializer):
    """
    Serializer for multiple ``ProfileGroup`` instances.
    """

    class Meta:
        fields = ('id', 'name', 'profile', 'is_default')
        model = models.ProfileGroup
