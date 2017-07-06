"""Serializers for the ``ProfileRow`` model.
"""

from rest_framework import serializers

from know_me import models

from .profile_item_serializers import ProfileItemSerializer


class ProfileRowSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``ProfileRow`` instances.
    """
    items = ProfileItemSerializer(many=True, read_only=True)
    items_url = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile-row-detail')

    class Meta:
        fields = ('id', 'url', 'name', 'row_type', 'items_url', 'items')
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
