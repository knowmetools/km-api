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
        extra_kwargs = {
            'alt_phone_number': {
                'help_text': "The contact's alternate phone number.",
            },
            'email': {
                'help_text': "The contact's email address.",
            },
            'name': {
                'help_text': "The contact's name.",
            },
            'phone_number': {
                'help_text': "The contact's primary phone number.",
            },
            'relation': {
                'help_text': "The contact's relation to the user.",
            },
        }
        fields = (
            'id', 'url', 'name', 'relation', 'phone_number',
            'alt_phone_number', 'email', 'permissions'
        )
        model = models.EmergencyContact
