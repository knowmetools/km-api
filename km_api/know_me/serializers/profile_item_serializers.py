"""Serializers for the ``ProfileItem`` model.
"""

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from know_me import models
from know_me.serializers.profile_item_content_serializers import (
    ImageContentSerializer,
    ListContentSerializer,
)
from dry_rest_permissions.generics import DRYPermissionsField


class ProfileItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``ProfileItem`` instances.
    """
    image_content = ImageContentSerializer(required=False)
    list_content = ListContentSerializer(required=False)
    permissions = DRYPermissionsField()
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile-item-detail')

    class Meta:
        fields = (
            'id',
            'url',
            'name',
            'image_content',
            'list_content',
            'permissions')
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
        list_content_data = data.pop('list_content', None)

        item = super(ProfileItemSerializer, self).create(data)

        if image_content_data is not None:
            models.ImageContent.objects.create(
                profile_item=item,
                **image_content_data)

        if list_content_data is not None:
            models.ListContent.objects.create(
                profile_item=item,
                **list_content_data)

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

    def validate(self, data):
        """
        Validate the data provided to the serializer.

        Args:
            data (dict):
                The data provided to the serializer.

        Returns:
            dict:
                The validated data.

        Raises:
            :class:`serializers.ValidationError`:
                If multiple content types are provided.
        """
        if 'image_content' in data and 'list_content' in data:
            raise serializers.ValidationError(
                _("Only one of 'image_content' and 'list_content' may be "
                  "provided."))

        # If we are creating a new instance, some content must be
        # provided.
        if not self.instance:
            if 'image_content' not in data and 'list_content' not in data:
                raise serializers.ValidationError(
                    _("One of 'image_content' or 'list_content' must be "
                      "provided."))

        # If an existing instance is being edited, the type of content
        # may not be changed.
        else:
            for attr in ('image_content', 'list_content'):
                if attr in data and not hasattr(self.instance, attr):
                    raise serializers.ValidationError(
                        _('The type of content attached to a profile item may '
                          'not change.'))

        return data
