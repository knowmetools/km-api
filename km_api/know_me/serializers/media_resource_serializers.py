"""Serializers for the ``MediaResource`` model.
"""

from rest_framework import serializers

from know_me import models


class MediaResourceSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``MediaResource`` instances.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:media-resource-detail')

    class Meta:
        fields = ('id', 'url', 'name', 'file')
        model = models.MediaResource
