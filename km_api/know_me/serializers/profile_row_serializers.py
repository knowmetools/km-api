"""Serializers for the ``ProfileRow`` model.
"""

from rest_framework import serializers

from know_me import models


class ProfileRowListSerializer(serializers.ModelSerializer):
    """
    Serializer for multiple ``ProfileRow`` instances.
    """

    class Meta:
        fields = ('id', 'name', 'row_type')
        model = models.ProfileRow
