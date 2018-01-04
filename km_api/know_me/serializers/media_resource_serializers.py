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
        extra_kwargs = {
            'file': {
                'help_text': "The file to upload.",
            },
            'name': {
                'help_text': "The name of the media resource.",
            }
        }
        fields = ('id', 'url', 'name', 'file', 'permissions')
        model = models.MediaResource


class MediaResourceCategorySerializer(
        serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``MediaResourceCategory`` instances.
    """
    permissions = DRYPermissionsField()
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:media-resource-category-list')

    class Meta:
        extra_kwargs = {
            'name': {
                'help_text': "The name of the media resource category.",
            }
        }
        fields = ('id', 'url', 'name', 'permissions')
        model = models.MediaResourceCategory
