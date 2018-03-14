from dry_rest_permissions.generics import DRYPermissionsField

from rest_framework import serializers

from account.serializers import UserInfoSerializer
from know_me.journal import models


class EntryCommentSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for comments on journal entries.
    """
    permissions = DRYPermissionsField()
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:journal:entry-comment-detail')
    user = UserInfoSerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'url',
            'created_at',
            'updated_at',
            'permissions',
            'text',
            'user')
        model = models.EntryComment


class EntryListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for a list of journal entries.
    """
    comments_url = serializers.HyperlinkedIdentityField(
        view_name='know-me:journal:entry-comment-list')
    url = serializers.HyperlinkedIdentityField(
        view_name='know-me:journal:entry-detail')

    class Meta:
        fields = (
            'id',
            'url',
            'created_at',
            'updated_at',
            'comments_url',
            'km_user_id')
        model = models.Entry


class EntryDetailSerializer(EntryListSerializer):
    """
    Serializer for a single journal entry.
    """
    comments = EntryCommentSerializer(many=True, read_only=True)
    permissions = DRYPermissionsField()

    class Meta(EntryListSerializer.Meta):
        fields = EntryListSerializer.Meta.fields + (
            'comments',
            'permissions',
            'text')
