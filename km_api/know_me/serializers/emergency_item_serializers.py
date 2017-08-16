"""Serializers for the :class:`.EmergencyItem` model.
"""

from rest_framework import serializers

from know_me import models
from know_me.serializers.fields import MediaResourceField
from dry_rest_permissions.generics import DRYPermissionsField


class EmergencyItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for emergency items.
    """
    media_resource = MediaResourceField(required=False)
    permissions = DRYPermissionsField()
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:emergency-item-detail')

    class Meta(object):
        fields = (
            'id',
            'url',
            'name',
            'description',
            'media_resource',
            'permissions')
        model = models.EmergencyItem
