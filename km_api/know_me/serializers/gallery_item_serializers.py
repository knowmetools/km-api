"""Serializers for the ``GalleryItem`` model.
"""

from rest_framework import serializers

from know_me import models


class GalleryItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``GalleryItem`` instances.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:gallery-item-detail')

    class Meta:
        fields = ('id', 'url', 'name', 'resource')
        model = models.GalleryItem
