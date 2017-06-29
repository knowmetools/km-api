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
    url = RowHyperlinkedIdentityField(view_name='know-me:profile-row-detail')

    class Meta:
        fields = ('id', 'url', 'name', 'row_type')
        model = models.ProfileRow
