"""Serializers for the ``ProfileItem`` model.
"""

from rest_framework import serializers

from know_me import models
from know_me.serializers.profile_item_content_serializers import (
    ImageContentSerializer
)


class ProfileItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``ProfileItem`` instances.
    """
    image_content = ImageContentSerializer(required=False)
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile-item-detail')

    class Meta:
        fields = ('id', 'url', 'name', 'image_content')
        model = models.ProfileItem

    def create(self, data):
        """
        Create a new profile item.

        Since we can have different types of content for a profile item,
        we have to split the data and create models separately.

        Args:
            data (dict):
                The data to create the profile item from.

        Returns:
            :class:`.ProfileItem`:
                A new profile item with the provided content.
        """
        image_content_data = data.pop('image_content', None)

        item = super(ProfileItemSerializer, self).create(data)

        if image_content_data is not None:
            models.ImageContent.objects.create(
                profile_item=item,
                **image_content_data)

        return item

    def update(self, profile_item, data):
        """
        Update an existing profile item.

        Updates to the item's content are handled by a content-specific
        serializer.

        Args:
            profile_item (:class:`.ProfileItem`):
                The profile item being updated.
            data (dict):
                The data to update the profile item with.

        Returns:
            :class:`.ProfileItem`:
                The updated profile item instance.
        """
        image_content_data = data.pop('image_content', None)

        item = super(ProfileItemSerializer, self).update(profile_item, data)

        if image_content_data is not None:
            image_content_serializer = ImageContentSerializer(
                item.image_content,
                context=self.context,
                data=image_content_data)

            image_content_serializer.is_valid(raise_exception=True)
            image_content_serializer.save()

        return item
