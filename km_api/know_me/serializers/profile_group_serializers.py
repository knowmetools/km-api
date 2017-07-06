"""Serializers for the ``ProfileGroup`` model.
"""

from rest_framework import serializers

from know_me import models

from .profile_row_serializers import ProfileRowSerializer


class ProfileGroupListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for multiple ``ProfileGroup`` instances.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile-group-detail')

    class Meta:
        fields = ('id', 'url', 'name', 'is_default')
        model = models.ProfileGroup


class ProfileGroupDetailSerializer(ProfileGroupListSerializer):
    """
    Serializer for single ``ProfileGroup`` instances.

    Based off ``ProfileGroupListSerializer``.
    """
    rows_url = serializers.SerializerMethodField()
    rows = ProfileRowSerializer(many=True, read_only=True)

    class Meta:
        fields = ('id', 'url', 'name', 'is_default', 'rows_url', 'rows')
        model = models.ProfileGroup

    def get_rows_url(self, group):
        """
        Get the URL of the given group's row list.

        Args:
            group:
                The group being serialized.

        Returns:
            The URL of the given group's row list.
        """
        return group.get_row_list_url(self.context['request'])
