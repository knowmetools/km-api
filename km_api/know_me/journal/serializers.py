from dry_rest_permissions.generics import DRYPermissionsField

from rest_framework import serializers

from know_me.journal import models


class EntryListSerializer(serializers.ModelSerializer):
    """
    Serializer for a list of journal entries.
    """

    class Meta:
        fields = (
            'id',
            'created_at',
            'updated_at',
            'km_user_id')
        model = models.Entry


class EntryDetailSerializer(EntryListSerializer):
    """
    Serializer for a single journal entry.
    """
    permissions = DRYPermissionsField()

    class Meta(EntryListSerializer.Meta):
        fields = EntryListSerializer.Meta.fields + ('permissions', 'text')
