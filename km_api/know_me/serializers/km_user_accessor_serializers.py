"""Serializers for the ``KMUserAccessor`` model.
"""

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from know_me import models
from .km_user_serializers import KMUserDetailSerializer


class KMUserAccessorSerializer(serializers.ModelSerializer):
    """
    Serializer for ``KMUserAccessor`` instances.
    """
    km_user = KMUserDetailSerializer(read_only=True)

    class Meta:
        fields = (
            'accepted',
            'can_write',
            'email',
            'has_private_profile_access',
            'km_user',
        )
        model = models.KMUserAccessor
        read_only_fields = ('accepted',)

    def create(self, validated_data):
        """
        Create a new accessor for a Know Me user.

        Args:
            validated_data (dict):
                The data to create the accessor from.

        Returns:
            The newly created ``KMUserAccessor`` instance.
        """
        km_user = validated_data.pop('km_user')
        email = validated_data.pop('email')

        return km_user.share(email, **validated_data)

    def validate_email(self, email):
        """
        Validate the provided email address.

        Args:
            email (str):
                The email address to validate.

        Returns:
            str:
                The validated email address.

        Raises:
            serializers.ValidationError:
                If an accessor is being updated and the provided email
                address does not match the accessor's current email.
        """
        if self.instance and email != self.instance.email:
            raise serializers.ValidationError(
                _('The email of an existing share may not be changed.'))

        return email
