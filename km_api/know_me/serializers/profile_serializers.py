"""Serializers for the ``Profile`` model.
"""

from rest_framework import serializers

from know_me import models

from .profile_topic_serializers import ProfileTopicSerializer
from dry_rest_permissions.generics import DRYPermissionsField


EXTRA_FIELD_KWARGS = {
    'is_default': {
        'help_text': ("A boolean indicating if the profile is the user's "
                      "default profile."),
    },
    'name': {
        'help_text': "The name of the profile.",
    },
}


class ProfileListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for multiple ``Profile`` instances.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile-detail')
    permissions = DRYPermissionsField()

    class Meta:
        extra_kwargs = EXTRA_FIELD_KWARGS
        fields = (
            'id',
            'url',
            'name',
            'is_default',
            'permissions')
        model = models.Profile


class ProfileDetailSerializer(ProfileListSerializer):
    """
    Serializer for single ``Profile`` instances.

    Based off ``ProfileListSerializer``.
    """
    topics_url = serializers.SerializerMethodField()
    topics = ProfileTopicSerializer(many=True, read_only=True)
    permissions = DRYPermissionsField()

    class Meta:
        extra_kwargs = EXTRA_FIELD_KWARGS
        fields = (
            'id',
            'url',
            'name',
            'is_default',
            'permissions',
            'topics_url',
            'topics')
        model = models.Profile

    def get_topics_url(self, profile):
        """
        Get the URL of the given profile's topic list.

        Args:
            profile:
                The profile being serialized.

        Returns:
            The URL of the given profile's topic list.
        """
        return profile.get_topic_list_url(self.context['request'])
