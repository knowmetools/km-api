"""Serializers for the ``KMUser`` model.
"""

from rest_framework import serializers

from know_me import models

from .profile_serializers import ProfileListSerializer


class KMUserListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for multiple ``KMUser`` instances.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:km-user-detail')

    class Meta:
        fields = ('id', 'url', 'name', 'quote')
        model = models.KMUser


class KMUserDetailSerializer(KMUserListSerializer):
    """
    Serializer for single ``KMUser`` instances.

    This serializer builds off of the ``KMUserListSerializer``.
    """
    gallery_url = serializers.SerializerMethodField()
    profiles = ProfileListSerializer(many=True, read_only=True)
    profiles_url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'url', 'name', 'quote', 'gallery_url',
            'profiles_url', 'profiles'
        )
        model = models.KMUser

    def get_gallery_url(self, profile):
        """
        Get the URL for the gallery view of the profile being
        serialized.

        Args:
            profile:
                The ``KMUser`` instance being serialized.

        Returns:
            str:
                The URL of the profile's gallery view.
        """
        return profile.get_gallery_url(self.context['request'])

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
