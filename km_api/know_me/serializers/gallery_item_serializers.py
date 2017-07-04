"""Serializers for the ``GalleryItem`` model.
"""

from rest_framework import serializers
from rest_framework.reverse import reverse

from know_me import models


class GalleryItemHyperlink(serializers.HyperlinkedIdentityField):
    """
    Field for serializing the detail URL of a gallery item.
    """

    def get_url(self, item, view_name, request, *args):
        """
        Get the URL of the given item's detail view.

        Args:
            item:
                The item to get the detail view of.
            view_name (str):
                The name of the item detail view.
            request:
                The request being made.

        Returns:
            The URL of the given item's detail view.
        """
        return reverse(
            view_name,
            kwargs={
                'gallery_item_pk': item.pk,
                'profile_pk': item.profile.pk,
            },
            request=request)


class GalleryItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``GalleryItem`` instances.
    """
    url = GalleryItemHyperlink(view_name='know-me:gallery-item-detail')

    class Meta:
        fields = ('id', 'url', 'name', 'resource')
        model = models.GalleryItem
