"""Serializers for the ``GalleryItem`` model.
"""

from rest_framework import serializers

from know_me import models


class GalleryItemSerializer(serializers.ModelSerializer):
    """
    Serializer for ``GalleryItem`` instances.
    """

    class Meta:
        fields = ('id', 'name', 'resource')
        model = models.GalleryItem
