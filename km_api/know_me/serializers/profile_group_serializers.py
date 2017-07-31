"""Serializers for the ``ProfileGroup`` model.
"""

from rest_framework import serializers

from know_me import models

from .profile_topic_serializers import ProfileTopicSerializer


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
    topics_url = serializers.SerializerMethodField()
    topics = ProfileTopicSerializer(many=True, read_only=True)

    class Meta:
        fields = ('id', 'url', 'name', 'is_default', 'topics_url', 'topics')
        model = models.ProfileGroup

    def get_topics_url(self, group):
        """
        Get the URL of the given group's topic list.

        Args:
            group:
                The group being serialized.

        Returns:
            The URL of the given group's topic list.
        """
        return group.get_topic_list_url(self.context['request'])
