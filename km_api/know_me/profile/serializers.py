from django.utils.translation import ugettext_lazy as _

from dry_rest_permissions.generics import DRYPermissionsField

from rest_framework import serializers

from know_me.profile import models


class MediaResourceCategorySerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``MediaResourceCategory`` instances.
    """
    km_user_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='km_user')
    permissions = DRYPermissionsField()
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:media-resource-category-detail')

    class Meta:
        fields = (
            'id',
            'url',
            'created_at',
            'updated_at',
            'km_user_id',
            'name',
            'permissions')
        model = models.MediaResourceCategory


class MediaResourceSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``MediaResource`` instances.
    """
    category_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='category')
    permissions = DRYPermissionsField()
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:media-resource-detail')

    class Meta:
        fields = (
            'id',
            'url',
            'created_at',
            'updated_at',
            'category_id',
            'file',
            'name',
            'permissions')
        model = models.MediaResource


#######################
# Profile Serializers #
#######################

# The profile related serializers are declared in hierarchical order so
# that they can be nested under each other.


class ListEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for list entries.
    """
    permissions = DRYPermissionsField()
    profile_item_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='profile_item')

    class Meta:
        fields = (
            'id',
            'created_at',
            'updated_at',
            'permissions',
            'profile_item_id',
            'text')
        model = models.ListEntry


class ProfileItemSerializer(serializers.ModelSerializer):
    """
    Serializer for profile items.
    """
    media_resource = MediaResourceSerializer(read_only=True)
    media_resource_id = serializers.PrimaryKeyRelatedField(
        queryset=models.MediaResource.objects.all(),
        required=False,
        source='media_resource',
        write_only=True)
    permissions = DRYPermissionsField()
    topic_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='topic')
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:profile-item-detail')

    class Meta:
        fields = (
            'id',
            'url',
            'created_at',
            'updated_at',
            'description',
            'image',
            'media_resource',
            'media_resource_id',
            'name',
            'permissions',
            'topic_id')
        model = models.ProfileItem

    def validate_media_resource_id(self, resource):
        """
        Validate the provided media resource ID.

        The media resource must be owned by the same Know Me user who
        owns the item bound to the serializer or the Know Me user given
        to the serializer as context.

        Args:
            resource:
                The media resource corresponding to the provided ID.

        Returns:
            The validated media resource ID.

        Raises:
            AssertionError:
                If the serializer is not bound and no Know Me user is
                provided as context.
            serializers.ValidationError:
                If there is no media resource with the provided ID owned
                by the relevant Know Me user.
        """
        if self.instance is not None:
            km_user = self.instance.topic.profile.km_user
        else:
            assert 'km_user' in self.context, (
                "The serializer class '%s' requires 'km_user' to be provided "
                "as context."
            ) % self.__class__.__name__

            km_user = self.context['km_user']

        if not resource.km_user == km_user:
            raise serializers.ValidationError(
                _('There is no media resource with the provided ID.'))

        return resource


class ProfileTopicSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for profile topics.
    """
    permissions = DRYPermissionsField()
    profile_id = serializers.PrimaryKeyRelatedField(
        read_only=True,
        source='profile')
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:profile-topic-detail')

    class Meta:
        fields = (
            'id',
            'url',
            'created_at',
            'updated_at',
            'is_detailed',
            'name',
            'permissions',
            'profile_id')
        model = models.ProfileTopic


class ProfileListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for multiple profile instances.
    """
    permissions = DRYPermissionsField()
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:profile-detail')

    class Meta:
        fields = (
            'id',
            'url',
            'created_at',
            'updated_at',
            'name',
            'permissions')
        model = models.Profile


class ProfileDetailSerializer(ProfileListSerializer):
    """
    Serializer for a single profile.
    """
    topics = ProfileTopicSerializer(many=True, read_only=True)
    topics_url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:profile-topic-list')

    class Meta(ProfileListSerializer.Meta):
        fields = ProfileListSerializer.Meta.fields + ('topics', 'topics_url')
