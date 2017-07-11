"""Serializers for account tasks.
"""

import logging

from django.contrib.auth import password_validation
from django.utils.translation import ugettext as _

from rest_framework import serializers


logger = logging.getLogger(__name__)


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password.
    """
    new_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True)
    old_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True)

    class Meta:
        fields = ('old_password', 'new_password')

    def save(self):
        """
        Change the requesting user's password.
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.send_password_changed_email()

        logger.info('Set new password for %s.', user)

    def validate(self, data):
        """
        Validate the serializer as a whole.

        Args:
            data (dict):
                The data to validate.

        Returns:
            dict:
                A dictionary containing validated data.

        Raises:
            ValidationError:
                If the user's new password is the same as their old
                password.
        """
        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError(
                _('The new password must be different from the current '
                  'password.'))

        return data

    def validate_new_password(self, password):
        """
        Validate the user's new password.

        We validate the password by running it through Django's password
        validation system.

        Args:
            password (str):
                The password to validate.

        Returns:
            str:
                The validated password.

        Raises:
            ValidationError:
                If the password is not valid.
        """
        password_validation.validate_password(password)

        return password

    def validate_old_password(self, password):
        """
        Validate the user's old password.

        Args:
            password (str):
                The password to validate.

        Returns:
            str:
                The validated password.

        Raises:
            ValidationError:
                If the provided password is not the user's current
                password.
        """
        if not self.context['request'].user.check_password(password):
            raise serializers.ValidationError(
                _("Authentication failed. The provided password does not "
                  "match your current password."))

        return password
