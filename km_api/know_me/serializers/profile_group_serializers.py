"""Serializers for the ``ProfileGroup`` model.
"""

from rest_framework import serializers
from rest_framework.reverse import reverse

from know_me import models

from .profile_row_serializers import ProfileRowListSerializer


class GroupHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    """
    Field for serializing the detail URL of a profile group.
    """

    def get_url(self, group, view_name, request, *args):
        """
        Get the URL of the given group's detail view.

        Args:
            group:
                The group to get the detail view of.
            view_name (str):
                The name of the profile group detail view.
            request:
                The request being made.

        Returns:
            The URL of the given profile group's detail view.
        """
        return reverse(
            view_name,
            kwargs={
                'group_pk': group.pk,
                'profile_pk': group.profile.pk,
            },
            request=request)


class ProfileGroupListSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for multiple ``ProfileGroup`` instances.
    """
    rows = ProfileRowListSerializer(many=True, read_only=True)
    url = GroupHyperlinkedIdentityField(
        view_name='know-me:profile-group-detail')

    class Meta:
        fields = ('id', 'url', 'name', 'is_default', 'rows')
        model = models.ProfileGroup


class ProfileGroupDetailSerializer(ProfileGroupListSerializer):
    """
    Serializer for single ``ProfileGroup`` instances.

    Based off ``ProfileGroupListSerializer``.
    """

    class Meta:
        fields = ('id', 'url', 'name', 'is_default', 'rows')
        model = models.ProfileGroup
