"""Serializers for the :class:`.EmergencyItem` model.
"""

from rest_framework import serializers

from know_me import models
from know_me.serializers.fields import MediaResourceField


class EmergencyItemSerializer(serializers.ModelSerializer):
    """
    Serializer for emergency items.
    """
    media_resource = MediaResourceField()

    class Meta(object):
        fields = ('id', 'name', 'description', 'media_resource')
        model = models.EmergencyItem
