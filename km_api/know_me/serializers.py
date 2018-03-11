"""Serializers for the ``know_me`` module.
"""

from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from know_me import models
from know_me.profile.serializers import ProfileListSerializer


EXTRA_FIELD_KWARGS = {
    'image': {
        'help_text': 'An image that represents the Know Me user.',
    },
    'quote': {
        'help_text': "A quote for the Know Me user to introduce themself.",
    },
}


class KMUserListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for multiple ``KMUser`` instances.
    """
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:km-user-detail')

    class Meta:
        extra_kwargs = EXTRA_FIELD_KWARGS
        fields = ('id', 'url', 'name', 'image', 'quote')
        model = models.KMUser


class KMUserDetailSerializer(KMUserListSerializer):
    """
    Serializer for single ``KMUser`` instances.

    This serializer builds off of the ``KMUserListSerializer``.
    """
    media_resource_categories_url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:media-resource-category-list')
    media_resources_url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:media-resource-list')
    profiles = ProfileListSerializer(many=True, read_only=True)
    profiles_url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:profile-list')

    class Meta:
        extra_kwargs = EXTRA_FIELD_KWARGS
        fields = (
            'id',
            'url',
            'name',
            'image',
            'quote',
            'media_resource_categories_url',
            'media_resources_url',
            'profiles_url',
            'profiles',
        )
        model = models.KMUser


class KMUserAccessorSerializer(serializers.ModelSerializer):
    """
    Serializer for ``KMUserAccessor`` instances.
    """
    km_user = KMUserListSerializer(read_only=True)
    url = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'url',
            'email',
            'is_accepted',
            'is_admin',
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

        # Remove 'is_accepted' from the arguments so it's not passed to the
        # 'share' method.
        validated_data.pop('is_accepted', None)

        return km_user.share(email, **validated_data)

    def get_url(self, accessor):
        """
        Get the URL of the provided accessor's detail view.

        Args:
            accessor:
                The accessor being serialized.

        Returns:
            The full URL of the accessor's detail view.
        """
        return accessor.get_absolute_url(self.context['request'])

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
