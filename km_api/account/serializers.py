"""Serializers for account tasks.
"""

import logging

from django.conf import settings
from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import ugettext as _

from django.contrib.auth import authenticate

from rest_framework import serializers

from account import models


logger = logging.getLogger(__name__)


class EmailVerificationSerializer(serializers.Serializer):
    """
    Serializer for verifying a user's email address.
    """
    key = serializers.CharField(
        max_length=settings.EMAIL_CONFIRMATION_KEY_LENGTH,
        write_only=True)
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True)

    def save(self):
        """
        Verify the email with the provided key.
        """
        confirmation = self.validated_data['confirmation']

        confirmation.email.verified = True
        confirmation.email.save()

        confirmation.delete()

    def validate(self, data):
        """
        Validate the serializer's data as a whole.

        Args:
            data (dict):
                The data to validate.

        Returns:
            dict:
                The validated data.

        Raises:
            ValidationError:
                If the provided password does not match the user
                associated with the confirmation.
        """
        confirmation = models.EmailConfirmation.objects.get(key=data['key'])
        user = authenticate(
            email=confirmation.email.user,
            password=data['password'])

        if not user:
            raise serializers.ValidationError(
                _('The provided credentials were invalid.'))

        data['confirmation'] = confirmation

        return data

    def validate_key(self, key):
        """
        Validate the key passed to the serializer.

        Args:
            key (str):
                The key given to the serializer.

        Returns:
            str:
                The validated key.

        Raises:
            ValidationError:
                If there is no email confirmation with the given key.
        """
        try:
            confirmation = models.EmailConfirmation.objects.get(key=key)
        except models.EmailConfirmation.DoesNotExist:
            raise serializers.ValidationError(
                _('This key is invalid.'))

        if confirmation.is_expired():
            raise serializers.ValidationError(
                _('This key has expired. Please send a new verification email '
                  'and try again.'))

        return key


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password.
    """
    old_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True)
    new_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True)

    def save(self):
        """
        Change the requesting user's password.
        """
        user = self.context['request'].user

        user.set_password(self.validated_data['new_password'])
        user.save()

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


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for ``User`` instances.

    The serializer allows for updating of basic information like email
    or name. It does **not** allow for changing the user's password.
    """

    class Meta:
        fields = ('id', 'email', 'first_name', 'last_name')
        model = get_user_model()
        read_only_fields = ('email',)
