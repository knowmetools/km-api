"""Serializers for the ``ProfileRow`` model.
"""

from rest_framework import serializers
from rest_framework.reverse import reverse

from know_me import models


class RowHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    """
    Field for serializing the detail URL of a profile row.
    """

    def get_url(self, row, view_name, request, *args):
        """
        Get the URL of the given row's detail view.

        Args:
            row:
                The row to get the detail view of.
            view_name (str):
                The name of the profile row detail view.
            request:
                The request being made.

        Returns:
            The URL of the given profile row's detail view.
        """
        return reverse(
            view_name,
            kwargs={
                'group_pk': row.group.pk,
                'profile_pk': row.group.profile.pk,
                'row_pk': row.pk,
            },
            request=request)


class ProfileRowSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``ProfileRow`` instances.
    """
    items_url = serializers.SerializerMethodField()
    url = RowHyperlinkedIdentityField(view_name='know-me:profile-row-detail')

    class Meta:
        fields = ('id', 'url', 'name', 'row_type', 'items_url')
        model = models.ProfileRow

    def get_items_url(self, row):
        """
        Get the URL of the given row's item list view.

        Args:
            row:
                The row being serialized.

        Returns:
            str:
                The URL of the given row's item list view.
        """
        return row.get_item_list_url(self.context['request'])
