"""Serializers for the ``know_me`` module.
"""

from django.utils.translation import ugettext_lazy as _

from dry_rest_permissions.generics import DRYPermissionsField

from rest_framework import serializers

from account.serializers import UserInfoSerializer
from know_me import models
from know_me.profile.serializers import ProfileListSerializer


class ConfigSerializer(serializers.ModelSerializer):
    """
    Serializer for the Know Me config object.
    """
    permissions = DRYPermissionsField(global_only=True)

    class Meta:
        fields = ('minimum_app_version_ios', 'permissions')
        model = models.Config


class KMUserListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for multiple ``KMUser`` instances.
    """
    journal_entries_url = serializers.HyperlinkedIdentityField(
        view_name='know-me:journal:entry-list')
    media_resource_categories_url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:media-resource-category-list')
    media_resources_url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:media-resource-list')
    permissions = DRYPermissionsField()
    profiles_url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:profile-list')
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:km-user-detail')

    class Meta:
        extra_kwargs = {
            'image': {
                'help_text': 'An image that represents the Know Me user.',
            },
            'quote': {
                'help_text': ("A quote for the Know Me user to introduce "
                              "themself."),
            },
        }
        fields = (
            'id',
            'url',
            'created_at',
            'updated_at',
            'image',
            'journal_entries_url',
            'media_resource_categories_url',
            'media_resources_url',
            'name',
            'permissions',
            'profiles_url',
            'quote')
        model = models.KMUser


class KMUserDetailSerializer(KMUserListSerializer):
    """
    Serializer for single ``KMUser`` instances.

    This serializer builds off of the ``KMUserListSerializer``.
    """
    profiles = ProfileListSerializer(many=True, read_only=True)

    class Meta(KMUserListSerializer.Meta):
        fields = KMUserListSerializer.Meta.fields + ('permissions', 'profiles')


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
        view_name='know-me:accessor-accept')
    permissions = DRYPermissionsField(additional_actions=['accept'])
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:accessor-detail')
    user_with_access = UserInfoSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'url',
            'created_at',
            'updated_at',
            'accept_url',
            'email',
            'is_accepted',
            'is_admin',
            'km_user_id',
            'permissions',
            'user_with_access')
        model = models.KMUserAccessor
        read_only_fields = ('is_accepted',)

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
