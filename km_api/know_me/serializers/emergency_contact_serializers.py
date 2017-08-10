"""Serializers for the ``EmergencyContact`` model.
"""

from rest_framework import serializers

from know_me import models
from dry_rest_permissions.generics import DRYPermissionsField


class EmergencyContactSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``EmergencyContact`` instances.
    """
    permissions = DRYPermissionsField()
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:emergency-contact-detail')

    class Meta:
        fields = (
            'id', 'url', 'name', 'relation', 'phone_number',
            'alt_phone_number', 'email', 'permissions'
        )
        model = models.EmergencyContact
