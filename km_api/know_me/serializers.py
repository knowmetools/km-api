"""Serializers for the models in the ``know_me`` module.
"""

from rest_framework import serializers

from know_me import models


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

    class Meta:
        fields = ('id', 'url', 'name', 'quote', 'welcome_message')
        model = models.Profile
