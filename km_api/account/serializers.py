"""Serializers for account tasks.
"""

import logging

from django.conf import settings
from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import ugettext as _

from django.contrib.auth import authenticate

from rest_framework import serializers

from account import models
import templated_email


logger = logging.getLogger(__name__)


class EmailSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for email addresses.
    """

    class Meta:
        extra_kwargs = {
            'url': {
                'view_name': 'account:email-detail',
            },
        }
        fields = (
            'id', 'url', 'email', 'verified', 'verified_action', 'primary'
        )
        model = models.EmailAddress
        read_only_fields = ('verified',)

    def create(self, data):
        """
        Create a new email address.

        Args:
            data (dict):
                A dictionary containing the data to create the email
                address with.

        Returns:
            The newly created ``EmailAddress`` instance.
        """
        user = self.context['request'].user
        data['user'] = user

        email = super().create(data)

        confirmation = models.EmailConfirmation.objects.create(email=email)
        confirmation.send_confirmation()

        notification_context = {
            'email': email.email,
            'user': user,
        }

        templated_email.send_email(
            context=notification_context,
            subject=_('Email Added to Your Know Me Account'),
            template='account/email/email-added',
            to=user.email)

        return email

    def update(self, instance, data):
        """
        Update an email address with the serializer's data.

        Args:
            instance:
                The email address to update.
            data (dict):
                The data to update the email address with.

        Returns:
            The updated email address.
        """
        primary = data.get('primary')
        if primary and not instance.primary:
            instance.set_primary()

            logger.info(
                'Set %s as primary address for %s',
                instance.email,
                instance.user)

        return instance

    def validate_email(self, email):
        """
        Validate the email given to the serializer.

        Args:
            email (str):
                The email to validate.

        Returns:
            str:
                The validated email.

        Raises:
            ValidationError:
                If the serializer is already bound and the email address
                is different from the bound instance's email.
        """
        if self.instance and email and self.instance.email != email:
            raise serializers.ValidationError(
                _("An email's address cannot be changed. Instead, a new email "
                  "address should be added and swapped with this one."))

        return email

    def validate_primary(self, primary):
        """
        Validate the value passed to the ``primary`` field.

        Args:
            primary (bool):
                A boolean indicating if the email address should be the
                user's primary address.

        Returns:
            bool:
                The validated ``primary`` value.

        Raises:
            ValidationError:
                If ``primary`` was given when creating a new email.
        """
        if not self.instance and primary:
            raise serializers.ValidationError(
                _('An email address cannot be set as the primary when it is '
                  'created.'))

        if primary and not self.instance.verified:
            raise serializers.ValidationError(
                _('The email address must be verified before it can be set as '
                  'the primary address.'))

        return primary

    def validate_verified_action(self, action):
        """
        Validate the provided verification action.

        The validation action of an email may not be changed once the
        email address is created.

        Args:
            action (int):
                An integer representing the action to be performed when
                the email is verified.

        Returns:
            int:
                The validated action.

        Raises:
            ValidationError:
                If the serializer is bound to an instance and the
                provided action does not match the instance's action.
        """
        if self.instance and self.instance.verified_action != action:
            raise serializers.ValidationError(
                _('The verification action of an existing email address may '
                  'not be changed.'))

        return action


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
        confirmation.confirm()

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
            email=confirmation.email.email,
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


class EmailVerifiedActionSerializer(serializers.Serializer):
    """
    Serializer for email verified actions.

    This serializer is used to serialize all the available actions for
    when an email is verified.
    """
    id = serializers.IntegerField(read_only=True)
    label = serializers.CharField(read_only=True)


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer for changing a user's password.
    """
    key = serializers.CharField(
        required=False,
        write_only=True)
    old_password = serializers.CharField(
        style={'input_type': 'password'},
        required=False,
        write_only=True)
    new_password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True)

    def save(self):
        """
        Change the requesting user's password.
        """
        user = self.validated_data['user']

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
        if data.get('key'):
            try:
                reset = models.PasswordReset.objects.get(key=data['key'])
            except models.PasswordReset.DoesNotExist:
                raise serializers.ValidationError(
                    _('The provided password reset key is invalid.'))

            if reset.is_expired():
                raise serializers.ValidationError(
                    _('The provided key has expired. Please request a new '
                      'password reset.'))

            data['user'] = reset.user
            reset.delete()
        else:
            data['user'] = self.context['request'].user

        if data['new_password'] == data.get('old_password'):
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


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset.
    """
    email = serializers.EmailField()

    def save(self):
        """
        Send the password reset email.
        """
        models.PasswordReset.create_and_send(self.validated_data['email'])


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
