"""Serializers for the ``EmergencyContact`` model.
"""

from rest_framework import serializers

from know_me import models


class EmergencyContactSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``EmergencyContact`` instances.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:emergency-contact-detail')

    class Meta:
        fields = (
            'id', 'url', 'name', 'relation', 'phone_number',
            'alt_phone_number', 'email'
        )
        model = models.EmergencyContact
