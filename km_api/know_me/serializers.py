"""Serializers for the models in the ``know_me`` module.
"""

from rest_framework import serializers

from know_me import models


class ProfileDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for single ``Profile`` instances.
    """

    class Meta:
        fields = ('id', 'name', 'quote', 'welcome_message')
        model = models.Profile


class ProfileListSerializer(serializers.ModelSerializer):
    """
    Serializer for multiple ``Profile`` instances.
    """

    class Meta:
        fields = ('id', 'name', 'quote', 'welcome_message')
        model = models.Profile
