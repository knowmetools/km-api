"""Serializers for the ``ProfileItem`` model.
"""

from rest_framework import serializers
from rest_framework.reverse import reverse

from know_me import models

from .media_resource_serializers import MediaResourceSerializer


class MediaResourceField(serializers.PrimaryKeyRelatedField):
    """
    Field for serializing a ``MediaResource`` instance.
    """

    def get_queryset(self):
        """
        Get a list of accessible media resources.

        Returns:
            A list of ``MediaResource`` instances that belong to the
            current profile.
        """
        assert 'profile' in self.context, (
            "The field '%(class)s' requires a 'profile' as context."
        ) % {
            'class': self.__class__.__name__,
        }

        return models.MediaResource.objects.filter(
            profile=self.context['profile'])


class ItemHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    """
    Field for serializing the detail URL of a profile item.
    """

    def get_url(self, item, view_name, request, *args):
        """
        Get the URL of the given item's detail view.

        Args:
            item:
                The item to get the detail view of.
            view_name (str):
                The name of the profile item detail view.
            request:
                The request being made.

        Returns:
            The URL of the given profile item's detail view.
        """
        return reverse(view_name, kwargs={'pk': item.pk}, request=request)


class ProfileItemSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for ``ProfileItem`` instances.
    """
    media_resource = MediaResourceField(required=False)
    media_resource_info = MediaResourceSerializer(
        read_only=True,
        source='media_resource')
    url = ItemHyperlinkedIdentityField(view_name='know-me:profile-item-detail')

    class Meta:
        fields = (
            'id', 'url', 'name', 'text', 'media_resource',
            'media_resource_info'
        )
        model = models.ProfileItem
