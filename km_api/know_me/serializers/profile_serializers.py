"""Serializers for the ``Profile`` model.
"""

from rest_framework import serializers

from know_me import models

from .profile_group_serializers import ProfileGroupListSerializer


class ProfileListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for multiple ``Profile`` instances.
    """
    url = serializers.HyperlinkedIdentityField(
        lookup_url_kwarg='profile_pk',
        view_name='know-me:profile-detail')

    class Meta:
        fields = ('id', 'url', 'name', 'quote', 'welcome_message')
        model = models.Profile


class ProfileDetailSerializer(ProfileListSerializer):
    """
    Serializer for single ``Profile`` instances.

    This serializer builds off of the ``ProfileListSerializer``.
    """
    groups = ProfileGroupListSerializer(many=True, read_only=True)
    groups_url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'url', 'name', 'quote', 'welcome_message', 'groups_url',
            'groups',
        )
        model = models.Profile

    def get_groups_url(self, profile):
        """
        Get the URL for the group list view of the profile being
        serialized.

        Args:
            profile:
                The ``Profile`` instance being serialized.

        Returns:
            The URL of the profile's group list view.
        """
        return profile.get_group_list_url(self.context['request'])
