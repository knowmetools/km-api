"""Serializers for the ``know_me`` module.
"""

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from dry_rest_permissions.generics import DRYPermissionsField

from rest_framework import serializers
from rest_framework.settings import api_settings

from account.serializers import UserInfoSerializer
from know_me import models
from know_me.profile.serializers import ProfileListSerializer


class ConfigSerializer(serializers.ModelSerializer):
    """
    Serializer for the Know Me config object.
    """

    permissions = DRYPermissionsField(global_only=True)

    class Meta:
        fields = ("minimum_app_version_ios", "permissions")
        model = models.Config


class KMUserInfoSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying basic information about a Know Me user.

    This serializer is used when we only need to display basic user
    information, such as alongside an accessor.
    """

    class Meta:
        fields = ("image", "name")
        model = models.KMUser


class KMUserListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for multiple ``KMUser`` instances.
    """

    is_premium_user = serializers.BooleanField(read_only=True)
    is_owned_by_current_user = serializers.SerializerMethodField()
    journal_entries_url = serializers.HyperlinkedIdentityField(
        view_name="know-me:journal:entry-list"
    )
    media_resources_url = serializers.HyperlinkedIdentityField(
        view_name="know-me:profile:media-resource-list"
    )
    permissions = DRYPermissionsField()
    profiles_url = serializers.HyperlinkedIdentityField(
        view_name="know-me:profile:profile-list"
    )
    url = serializers.HyperlinkedIdentityField(
        view_name="know-me:km-user-detail"
    )
    user_image = serializers.ImageField(read_only=True, source="user.image")

    class Meta:
        extra_kwargs = {
            "image": {
                "help_text": "An image that represents the Know Me user."
            },
            "quote": {
                "help_text": (
                    "A quote for the Know Me user to introduce themself."
                )
            },
        }
        fields = (
            "id",
            "url",
            "created_at",
            "updated_at",
            "is_legacy_user",
            "is_premium_user",
            "is_owned_by_current_user",
            "image",
            "journal_entries_url",
            "media_resources_url",
            "name",
            "permissions",
            "profiles_url",
            "quote",
            "user_image",
        )
        model = models.KMUser
        read_only_fields = ("is_legacy_user",)

    def get_is_owned_by_current_user(self, km_user):
        """
        Determine if the instance bound to the serializer is owned by
        the requesting user.

        Args:
            km_user:
                The Know Me user bound to the serializer.

        Returns:
            A boolean indicating if the requesting user owns the Know Me
            user bound to the serializer.
        """
        return self.context["request"].user == km_user.user


class KMUserDetailSerializer(KMUserListSerializer):
    """
    Serializer for single ``KMUser`` instances.

    This serializer builds off of the ``KMUserListSerializer``.
    """

    profiles = ProfileListSerializer(many=True, read_only=True)

    class Meta(KMUserListSerializer.Meta):
        fields = KMUserListSerializer.Meta.fields + ("permissions", "profiles")


class KMUserAccessorAcceptSerializer(serializers.ModelSerializer):
    """
    Serializer for accepting an accessor.
    """

    class Meta:
        fields = tuple()
        model = models.KMUserAccessor


class KMUserAccessorSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``KMUserAccessor`` instances.
    """

    accept_url = serializers.HyperlinkedIdentityField(
        view_name="know-me:accessor-accept"
    )
    km_user = KMUserInfoSerializer(read_only=True)
    permissions = DRYPermissionsField(additional_actions=["accept"])
    url = serializers.HyperlinkedIdentityField(
        view_name="know-me:accessor-detail"
    )
    user_with_access = UserInfoSerializer(read_only=True)

    class Meta:
        fields = (
            "id",
            "url",
            "created_at",
            "updated_at",
            "accept_url",
            "email",
            "is_accepted",
            "is_admin",
            "km_user",
            "permissions",
            "user_with_access",
        )
        model = models.KMUserAccessor
        read_only_fields = ("is_accepted",)

    def create(self, validated_data):
        """
        Create a new accessor for a Know Me user.

        Args:
            validated_data (dict):
                The data to create the accessor from.

        Returns:
            The newly created ``KMUserAccessor`` instance.
        """
        km_user = validated_data.pop("km_user")
        email = validated_data.pop("email")

        # If sharing fails (already shared, can't share with self, etc.)
        # we capture the error and echo it as a serializer error which
        # will get handled by the DRF middleware.
        try:
            return km_user.share(email, **validated_data)
        except ValidationError as e:
            raise serializers.ValidationError(
                {api_settings.NON_FIELD_ERRORS_KEY: e.message}
            )

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
                _("The email of an existing share may not be changed.")
            )

        return email


class LegacyUserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for legacy users.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="know-me:legacy-user-detail"
    )

    class Meta:
        fields = ("id", "url", "created_at", "updated_at", "email")
        model = models.LegacyUser
