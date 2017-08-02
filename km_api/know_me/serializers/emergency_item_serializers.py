"""Serializers for the :class:`.EmergencyItem` model.
"""

from rest_framework import serializers

from know_me import models
from know_me.serializers.fields import MediaResourceField


class EmergencyItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for emergency items.
    """
    media_resource = MediaResourceField(required=False)
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:emergency-item-detail')

    class Meta(object):
        fields = ('id', 'url', 'name', 'description', 'media_resource')
        model = models.EmergencyItem
