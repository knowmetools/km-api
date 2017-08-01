import pytest

from rest_framework.exceptions import ValidationError

from know_me.serializers import fields
from know_me.serializers.media_resource_serializers import (
    MediaResourceSerializer
)


def test_to_internal_value(media_resource_factory):
    """
    ``.to_internal_value()`` should return the media resource that has
    the provided ID.
    """
    resource = media_resource_factory()
    field = fields.MediaResourceField()

    assert field.to_internal_value(resource.id) == resource


@pytest.mark.django_db
def test_to_internal_value_non_existent():
    """
    If there is no media resource matching the provided ID, a
    ``ValidationError`` should be raised.
    """
    field = fields.MediaResourceField()

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
