"""Custom serializer fields.
"""

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from know_me import models


class MediaResourceField(serializers.RelatedField):
    """
    Field for representing a media resource.

    The field allows media resources to be written using the resource's
    ID, but read using the resource's serialized form.
    """
    queryset = models.MediaResource.objects.all()

    def get_queryset(self):
        """
        Limit the available resources using the serializer's context.

        The queryset returned includes only the media resources owned by
        the Know Me user given as context to the field.

        Returns:
            A queryset containing the media resources owned by the Know
            Me user given as context to the field.
        """
        assert 'km_user' in self.context, (
            "The serializer class '%s' requires 'km_user' to be provided as "
            "context.") % self.__class__.__name__

        queryset = super(MediaResourceField, self).get_queryset()

        return queryset.filter(km_user=self.context['km_user'])

    def to_internal_value(self, data):
        """
        Retrieve the media resource with the provided ID.

        Args:
            data (int):
                The ID of the media resource to fetch.

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
        # We do a lazy import to avoid circular imports when fields from
        # this module are used in serializers that are imported in this
        # module.
        from know_me.serializers.media_resource_serializers import (
            MediaResourceSerializer
        )

        return MediaResourceSerializer(value, context=self.context).data
