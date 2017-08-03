import pytest

from rest_framework.exceptions import ValidationError

from know_me.serializers import fields
from know_me.serializers.media_resource_serializers import (
    MediaResourceSerializer
)


def test_get_queryset(km_user_factory, media_resource_factory):
    """
    The queryset should return all the items owned by the Know Me user
    that is provided as context.
    """
    km_user = km_user_factory()
    media_resource_factory(km_user=km_user)

    media_resource_factory()

    field = fields.MediaResourceField()
    field.context = {
        'km_user': km_user,
    }

    assert list(field.get_queryset()) == list(km_user.media_resources.all())


def test_get_queryset_invalid_context():
    """
    If there is no 'km_user' in the field's context, an
    ``AssertionError`` should be raised.
    """
    field = fields.MediaResourceField()

    with pytest.raises(AssertionError):
        field.get_queryset()


def test_to_internal_value(media_resource_factory):
    """
    ``.to_internal_value()`` should return the media resource that has
    the provided ID.
    """
    resource = media_resource_factory()
    field = fields.MediaResourceField()
    field.context = {
        'km_user': resource.km_user,
    }

    assert field.to_internal_value(resource.id) == resource


def test_to_internal_value_non_existent(km_user_factory):
    """
    If there is no media resource matching the provided ID, a
    ``ValidationError`` should be raised.
    """
    field = fields.MediaResourceField()
    field.context = {
        'km_user': km_user_factory(),
    }

    with pytest.raises(ValidationError):
        field.to_internal_value(1)


def test_to_representation(media_resource_factory, serializer_context):
    """
    ``.to_representation()`` should return the serialized version of the
    provided media resource.
    """
    resource = media_resource_factory()
    serializer = MediaResourceSerializer(resource, context=serializer_context)

    field = fields.MediaResourceField()
    field.context = serializer_context

    assert field.to_representation(resource) == serializer.data