"""Serializers for the ``KMUser`` model.
"""

from rest_framework import serializers

from know_me import models

from .profile_serializers import ProfileListSerializer


EXTRA_FIELD_KWARGS = {
    'image': {
        'help_text': 'An image that represents the Know Me user.',
    },
    'quote': {
        'help_text': "A quote for the Know Me user to introduce themself.",
    },
}


class KMUserListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for multiple ``KMUser`` instances.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:km-user-detail')

    class Meta:
        extra_kwargs = EXTRA_FIELD_KWARGS
        fields = ('id', 'url', 'name', 'image', 'quote')
        model = models.KMUser


class KMUserDetailSerializer(KMUserListSerializer):
    """
    Serializer for single ``KMUser`` instances.

    This serializer builds off of the ``KMUserListSerializer``.
    """
    profiles = ProfileListSerializer(many=True, read_only=True)
    profiles_url = serializers.SerializerMethodField()

    class Meta:
        extra_kwargs = EXTRA_FIELD_KWARGS
        fields = (
            'id',
            'url',
            'name',
            'image',
            'quote',
            'profiles_url',
            'profiles',
        )
        model = models.KMUser

    def get_profiles_url(self, profile):
        """
        Get the URL for the profile list view of the profile being
        serialized.

        Args:
            profile:
                The ``KMUser`` instance being serialized.

        Returns:
            The URL of the profile's profile list view.
        """
        return profile.get_profile_list_url(self.context['request'])
