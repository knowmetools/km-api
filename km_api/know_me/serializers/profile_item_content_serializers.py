"""Serializers for different types of profile item content.
"""

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from know_me import models
from know_me.serializers.media_resource_serializers import (
    MediaResourceSerializer
)


class MediaResourceField(serializers.RelatedField):
    """
    Field for representing a media resource.

    The field allows the media resource to be specified using the
    resource's ID, but the resource is returned using it's full
    serialized form.
    """
    queryset = models.MediaResource.objects.all()

    def to_internal_value(self, data):
        """
        Map the ID given to a :class:`.MediaResource` instance.

        Args:
            data (int):
                The ID of a media resource.

        Returns:
            :class:`.MediaResource`:
                The media resource with the given ID.
        """
        try:
            return self.get_queryset().get(pk=data)
        except models.MediaResource.DoesNotExist:
            raise serializers.ValidationError(
                _('There is no media resource with the given ID.'))

    def to_representation(self, value):
        """
        Get the serialized representation of the provided resource.

        Args:
            value (:class:`.MediaResource`):
                The media resource to represent.

        Returns:
            dict:
                The media resource's serialized representation.
        """
        return MediaResourceSerializer(value, context=self.context).data


class ImageContentSerializer(serializers.ModelSerializer):
    """
    Serializer for profile item image content.
    """
    image_resource = MediaResourceField(required=False)
    media_resource = MediaResourceField(required=False)

    class Meta(object):
        fields = ('id', 'description', 'image_resource', 'media_resource')
        model = models.ImageContent
