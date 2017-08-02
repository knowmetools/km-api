"""Serializers for the ``Profile`` model.
"""

from rest_framework import serializers

from know_me import models

from .profile_topic_serializers import ProfileTopicSerializer


class ProfileListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for multiple ``Profile`` instances.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile-detail')

    class Meta:
        fields = ('id', 'url', 'name', 'is_default')
        model = models.Profile


class ProfileDetailSerializer(ProfileListSerializer):
    """
    Serializer for single ``Profile`` instances.

    Based off ``ProfileListSerializer``.
    """
    topics_url = serializers.SerializerMethodField()
    topics = ProfileTopicSerializer(many=True, read_only=True)

    class Meta:
        fields = ('id', 'url', 'name', 'is_default', 'topics_url', 'topics')
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
