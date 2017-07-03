"""Serializers for the ``ProfileItem`` model.
"""

from rest_framework import serializers
from rest_framework.reverse import reverse

from know_me import models


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
    url = ItemHyperlinkedIdentityField(view_name='know-me:profile-item-detail')

    class Meta:
        fields = ('id', 'url', 'name', 'text')
        model = models.ProfileItem
