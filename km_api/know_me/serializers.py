"""Serializers for the ``know_me`` module.
"""

from django.utils.translation import ugettext_lazy as _

from dry_rest_permissions.generics import DRYPermissionsField

from rest_framework import serializers

from know_me import models
from know_me.profile.serializers import ProfileListSerializer


class KMUserListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for multiple ``KMUser`` instances.
    """
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


class KMUserAccessorSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``KMUserAccessor`` instances.
    """
    km_user = KMUserListSerializer(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:accessor-detail')

    class Meta:
        fields = (
            'id',
            'url',
            'created_at',
            'updated_at',
            'email',
            'is_accepted',
            'is_admin',
            'km_user')
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

        # Remove 'is_accepted' from the arguments so it's not passed to the
        # 'share' method.
        validated_data.pop('is_accepted', None)

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

    def validate_is_accepted(self, is_accepted):
        """
        Validate the provided 'is_accepted' value.

        Args:
            accepted (boolean):
                A boolean indicating if the accessor has been accepted.

        Returns:
            boolean:
                The validated 'is_accepted' value.

        Raises:
            serializers.ValidationError:
                If the user doesn't have permission to change the
                'is_accepted' attribute.
        """
        accessor = self.instance

        if not accessor and is_accepted:
            raise serializers.ValidationError(
                _("An accessor can't be marked as accepted until after it has "
                  "been created."))
        elif (accessor
                and accessor.is_accepted != is_accepted
                and accessor.user_with_access != self.context['request'].user):
            raise serializers.ValidationError(
                _("Only the user granted access by the accessor may accept "
                  "the accessor."))

        return is_accepted
