"""Serializers for the ``MediaResource`` model.
"""

from rest_framework import serializers

from know_me import models
from dry_rest_permissions.generics import DRYPermissionsField


class MediaResourceSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``MediaResource`` instances.
    """
    permissions = DRYPermissionsField()
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:media-resource-detail')

    class Meta:
        fields = ('id', 'url', 'name', 'file', 'permissions')
        model = models.MediaResource
