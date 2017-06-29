"""Serializers for the ``ProfileRow`` model.
"""

from rest_framework import serializers

from know_me import models


class ProfileRowSerializer(serializers.ModelSerializer):
    """
    Serializer for ``ProfileRow`` instances.
    """

    class Meta:
        fields = ('id', 'name', 'row_type')
        model = models.ProfileRow
