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
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:list-entry-detail')

    class Meta:
        fields = (
            'id',
            'url',
            'created_at',
            'updated_at',
            'permissions',
            'profile_item_id',
            'text')
        model = models.ListEntry


class ProfileItemListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for a list of profile items.
    """
    list_entries_url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:list-entry-list')
    permissions = DRYPermissionsField()
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
            'list_entries_url',
            'name',
            'permissions',
            'topic_id')
        model = models.ProfileItem


class ProfileItemDetailSerializer(ProfileItemListSerializer):
    """
    Serializer for profile items.
    """
    list_entries = ListEntrySerializer(many=True, read_only=True)
    media_resource = MediaResourceSerializer(read_only=True)
    media_resource_id = serializers.PrimaryKeyRelatedField(
        help_text=_('The ID of the media resource to attach to the item.'),
        queryset=models.MediaResource.objects.all(),
        required=False,
        write_only=True)

    class Meta(ProfileItemListSerializer.Meta):
        fields = ProfileItemListSerializer.Meta.fields + (
            'list_entries',
            'media_resource',
            'media_resource_id')

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


class ProfileTopicListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for a list of profile topics.
    """
    items_url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:profile-item-list')
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
            'items_url',
            'name',
            'permissions',
            'profile_id')
        model = models.ProfileTopic


class ProfileTopicDetailSerializer(ProfileTopicListSerializer):
    """
    Serializer for a single profile topic.
    """
    items = ProfileItemListSerializer(many=True, read_only=True)

    class Meta(ProfileTopicListSerializer.Meta):
        fields = ProfileTopicListSerializer.Meta.fields + ('items',)


class ProfileListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for multiple profile instances.
    """
    permissions = DRYPermissionsField()
    topics_url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:profile-topic-list')
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:profile:profile-detail')

    class Meta:
        fields = (
            'id',
            'url',
            'created_at',
            'updated_at',
            'name',
            'permissions',
            'topics_url')
        model = models.Profile


class ProfileDetailSerializer(ProfileListSerializer):
    """
    Serializer for a single profile.
    """
    topics = ProfileTopicListSerializer(many=True, read_only=True)

    class Meta(ProfileListSerializer.Meta):
        fields = ProfileListSerializer.Meta.fields + ('topics',)
