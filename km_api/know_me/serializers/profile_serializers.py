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

    class Meta:
        fields = ('id', 'url', 'name', 'quote', 'welcome_message', 'groups')
        model = models.Profile
