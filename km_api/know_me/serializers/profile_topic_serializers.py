"""Serializers for the ``ProfileTopic`` model.
"""

from rest_framework import serializers

from know_me import models

from .profile_item_serializers import ProfileItemSerializer


class ProfileTopicSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``ProfileTopic`` instances.
    """
    items = ProfileItemSerializer(many=True, read_only=True)
    items_url = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile-topic-detail')

    class Meta:
        fields = ('id', 'url', 'name', 'topic_type', 'items_url', 'items')
        model = models.ProfileTopic

    def get_items_url(self, topic):
        """
        Get the URL of the given topic's item list view.

        Args:
            topic:
                The topic being serialized.

        Returns:
            str:
                The URL of the given topic's item list view.
        """
        return topic.get_item_list_url(self.context['request'])
