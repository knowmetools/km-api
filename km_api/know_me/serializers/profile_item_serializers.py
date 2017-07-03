"""Serializers for the ``ProfileItem`` model.
"""

from rest_framework import serializers
from rest_framework.reverse import reverse

from know_me import models

from .gallery_item_serializers import GalleryItemSerializer


class GalleryItemField(serializers.PrimaryKeyRelatedField):
    """
    Field for serializing a ``GalleryItem`` instance.
    """

    def get_queryset(self):
        """
        Get a list of accessible gallery items.

        Returns:
            A list of ``GalleryItem`` instances that belong to the
            current profile.
        """
        assert 'profile' in self.context, (
            "The field '%(class)s' requires a 'profile' as context."
        ) % {
            'class': self.__class__.__name__,
        }

        return models.GalleryItem.objects.filter(
            profile=self.context['profile'])


class ItemHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    """
    Field for serializing the detail URL of a profile item.
    """

    def get_url(self, item, view_name, request, *args):
        """
        Get the URL of the given item's detail view.

        Args:
            item:
                The item to get the detail view of.
            view_name (str):
                The name of the profile item detail view.
            request:
                The request being made.

        Returns:
            The URL of the given profile item's detail view.
        """
        return reverse(
            view_name,
            kwargs={
                'group_pk': item.row.group.pk,
                'item_pk': item.pk,
                'profile_pk': item.row.group.profile.pk,
                'row_pk': item.row.pk,
            },
            request=request)


class ProfileItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``ProfileItem`` instances.
    """
    gallery_item = GalleryItemField(required=False)
    gallery_item_info = GalleryItemSerializer(
        read_only=True,
        source='gallery_item')
    url = ItemHyperlinkedIdentityField(view_name='know-me:profile-item-detail')

    class Meta:
        fields = (
            'id', 'url', 'name', 'text', 'gallery_item', 'gallery_item_info'
        )
        model = models.ProfileItem
