"""Serializers for different types of profile item content.
"""

from rest_framework import serializers

from know_me import models
from know_me.serializers.fields import MediaResourceField
from dry_rest_permissions.generics import DRYPermissionsField


class ImageContentSerializer(serializers.ModelSerializer):
    """
    Serializer for profile item image content.
    """
    image_resource = MediaResourceField(required=False)
    media_resource = MediaResourceField(required=False)
    permissions = DRYPermissionsField()

    class Meta(object):
        fields = (
            'id',
            'description',
            'image_resource',
            'media_resource',
            'permissions')
        model = models.ImageContent


class ListEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for entries in a profile item list.
    """
    permissions = DRYPermissionsField()

    class Meta(object):
        extra_kwargs = {
            'text': {
                'help_text': "The text the list entry contains.",
            },
        }
        fields = (
            'id',
            'text',
            'permissions')
        model = models.ListEntry


class ListContentSerializer(serializers.ModelSerializer):
    """
    Serializer for profile list content.
    """
    entries = ListEntrySerializer(many=True, read_only=True)
    permissions = DRYPermissionsField()

    class Meta(object):
        fields = (
            'id',
            'entries',
            'permissions')
        model = models.ListContent
