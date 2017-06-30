"""Serializers for the ``ProfileItem`` model.
"""

from rest_framework import serializers

from know_me import models


class ProfileItemSerializer(serializers.ModelSerializer):
    """
    Serializer for ``ProfileItem`` instances.
    """

    class Meta:
        fields = ('id', 'name', 'text')
        model = models.ProfileItem
