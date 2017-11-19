"""Serializers for authentication views.
"""

import logging

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import password_validation
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from account.models import EmailAddress, EmailConfirmation, User
from km_auth import layer


logger = logging.getLogger(__name__)


class LayerIdentitySerializer(serializers.Serializer):
    """
    Serializer for obtaining an identity from Layer.

    This serializer takes a nonce provided by Layer and obtains an
    identity for the user making the request. This identity can then be
    used to participate in conversations.
    """
    identity_token = serializers.CharField(read_only=True)
    nonce = serializers.CharField(
        help_text=("The nonce provided by Layer. See the following URL for "
                   "more information: https://docs.layer.com/reference/"
                   "client_api/authentication.out#introduction"),
        write_only=True)

    def save(self):
        """
        Generate an identity for the requesting user.
        """
        self.validated_data['identity_token'] = layer.generate_identity_token(
            self.context['request'].user,
            self.validated_data['nonce'])


class TokenSerializer(serializers.Serializer):
    """
    Serializer for obtaining an auth token.

    The actual generation of the auth token is intended to be handled by
    the view that utilizes this serializer.
    """
    email = serializers.EmailField(help_text="The user's email address.")
    password = serializers.CharField(
        help_text="The user's password",
        style={'input_type': 'password'})

    def validate(self, data):
        """
        Ensure that the requesting user is allowed to obtain a token.

        Returns:
            dict:
                The validated data.

        Raises:
            ValidationError:
                If the provided credentials are invalid.
            ValidationError:
                If the requesting user does not have a verified email
                address.
        """
        user = authenticate(**data)

        if not user:
            raise serializers.ValidationError(
                _('Invalid credentials. Check your email and password and try'
                  'again.'))

        if not user.email_addresses.get(email=data['email']).verified:
            raise serializers.ValidationError(
                _('You must verify this email address before logging in.'))

        data['user'] = user

        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.
    """

    class Meta:
        extra_kwargs = {
            'email': {
                'help_text': "The user's email address.",
            },
            'first_name': {
                'help_text': "The user's first name.",
            },
            'last_name': {
                'help_text': "The user's last name.",
            },
            'password': {
                'help_text': "The user's password.",
                'style': {'input_type': 'password'},
                'write_only': True,
            },
        }
        fields = ('id', 'email', 'first_name', 'last_name', 'password')
        model = get_user_model()

    def create(self, validated_data):
        """
        Create a new user from the serializer's validated data.

        This also sends out an email to the user confirming their email
        address.

        Args:
            validated_data:
                The data to create the new user from.

        Returns:
            The newly created ``User`` instance.
        """
        logger.info(
            'Registering new user with email: %s',
            validated_data['email'])

        user = User.objects.create_user(**validated_data)
        email = EmailAddress.objects.create(
            email=self.validated_data['email'],
            user=user)

        confirmation = EmailConfirmation.objects.create(email=email)
        confirmation.send_confirmation()

        return user

    def validate_email(self, email):
        """
        Validate the provided email address.

        Returns:
            str:
                The validated email address.

        Raises:
            ValidationError:
                If that email exists and is verified already.
        """
        if EmailAddress.objects.filter(email=email, verified=True).exists():
            raise serializers.ValidationError(
                _('An account with that email address already exists.'))

        return email

    def validate_password(self, password):
        """
        Validate the provided password.

        This runs the password through Django's password validation
        system.

        Args:
            password (str):
                The password to validate.

        Returns:
            str:
                The validated password.

        Raises:
            ValidationError:
                If the provided password does not pass Django's password
                validation checks.
        """
        password_validation.validate_password(password, self.instance)

        return password
