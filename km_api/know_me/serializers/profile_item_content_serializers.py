"""Serializers for different types of profile item content.
"""

from rest_framework import serializers

from know_me import models
from know_me.serializers.fields import MediaResourceField


class ImageContentSerializer(serializers.ModelSerializer):
    """
    Serializer for profile item image content.
    """
    image_resource = MediaResourceField(required=False)
    media_resource = MediaResourceField(required=False)

    class Meta(object):
        fields = ('id', 'description', 'image_resource', 'media_resource')
        model = models.ImageContent


class ListEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for entries in a profile item list.
    """

    class Meta(object):
        fields = ('id', 'text')
        model = models.ListEntry


class ListContentSerializer(serializers.ModelSerializer):
    """
    Serializer for profile list content.
    """
    entries = ListEntrySerializer(many=True, read_only=True)

    class Meta(object):
        fields = ('id', 'entries')
        model = models.ListContent
