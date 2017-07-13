"""Serializers for authentication views.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from account.models import EmailAddress, EmailConfirmation
from km_auth import layer


class LayerIdentitySerializer(serializers.Serializer):
    """
    Serializer for obtaining an identity from Layer.

    This serializer takes a nonce provided by Layer and obtains an
    identity for the user making the request. This identity can then be
    used to participate in conversations.
    """
    identity_token = serializers.CharField(read_only=True)
    nonce = serializers.CharField(write_only=True)

    def save(self):
        """
        Generate an identity for the requesting user.
        """
        self.validated_data['identity_token'] = layer.generate_identity_token(
            self.context['request'].user,
            self.validated_data['nonce'])


class TokenSerializer(AuthTokenSerializer):
    """
    Serializer for obtaining an auth token.

    This builds upon the default serializer provided by DRF and adds a
    check to ensure the user obtaining a token has a verified email.
    """

    def validate(self, data):
        """
        Ensure that the requesting user is allowed to obtain a token.

        Returns:
            dict:
                The validated data.

        Raises:
            ValidationError:
                If the requesting user does not have a verified email
                address.
        """
        data = super().validate(data)

        if not data['user'].email_verified:
            raise serializers.ValidationError(
                _('You must verify your email address before logging in.'))

        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.
    """

    class Meta:
        extra_kwargs = {
            'password': {
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
        user = get_user_model().objects.create_user(**validated_data)

        EmailAddress.objects.create(
            email=self.validated_data['email'],
            user=user)

        confirmation = EmailConfirmation.objects.create(user=user)
        confirmation.send_confirmation()

        return user

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
