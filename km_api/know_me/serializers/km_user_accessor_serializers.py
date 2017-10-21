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

        # Remove 'accepted' from the arguments so it's not passed to the
        # 'share' method.
        validated_data.pop('accepted', None)

        return km_user.share(email, **validated_data)

    def validate_accepted(self, accepted):
        """
        Validate the provided 'accepted' value.

        Args:
            accepted (boolean):
                A boolean indicating if the accessor has been accepted.

        Returns:
            boolean:
                The validated 'accepted' value.

        Raises:
            serializers.ValidationError:
                If the user doesn't have permission to change the
                'accepted' attribute.
        """
        accessor = self.instance

        if not accessor and accepted:
            raise serializers.ValidationError(
                _("An accessor can't be marked as accepted until after it has "
                  "been created."))
        elif accessor \
                and accessor.accepted != accepted \
                and accessor.user_with_access != self.context['request'].user:
            raise serializers.ValidationError(
                _("Only the user granted access by the accessor may accept "
                  "the accessor."))

        return accepted

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
