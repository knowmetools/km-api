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
    media_resource = MediaResourceField(
        help_text="The ID of the media resource to attach to this item.",
        required=False)
    permissions = DRYPermissionsField()
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:emergency-item-detail')

    class Meta(object):
        extra_kwargs = {
            'description': {
                'help_text': 'A description of the emergency item.',
            },
            'name': {
                'help_text': "The name of the item.",
            }
        }
        fields = (
            'id',
            'url',
            'name',
            'description',
            'media_resource',
            'permissions')
        model = models.EmergencyItem
