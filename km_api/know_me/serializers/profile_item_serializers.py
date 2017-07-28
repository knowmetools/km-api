"""Serializers for the ``ProfileItem`` model.
"""

from rest_framework import serializers

from know_me import models


class ProfileItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``ProfileItem`` instances.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile-item-detail')

    class Meta:
        fields = ('id', 'url', 'name')
        model = models.ProfileItem
