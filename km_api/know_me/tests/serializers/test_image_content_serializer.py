import pytest

from know_me import serializers
from know_me.serializers.profile_item_content_serializers import (
    ImageContentSerializer
)


def test_create(
        image,
        image_content_factory,
        media_resource_factory,
        profile_item_factory,
        serializer_context):
    """
    Saving a serializer with valid data should create a new
    ``ImageContent`` instance.
    """
    profile_item = profile_item_factory()
    km_user = profile_item.topic.profile.km_user

    serializer_context['km_user'] = km_user

    image_resource = media_resource_factory(file=image, km_user=km_user)
    media_resource = media_resource_factory(km_user=km_user)

    data = {
        'description': 'Test image content description.',
        'image_resource': image_resource.id,
        'media_resource': media_resource.id,
    }

    serializer = ImageContentSerializer(context=serializer_context, data=data)
    assert serializer.is_valid(), serializer.errors

    img_content = serializer.save(profile_item=profile_item)

    assert img_content.description == data['description']
    assert img_content.image_resource == image_resource
    assert img_content.media_resource == media_resource

    assert img_content.profile_item == profile_item


def test_serialize(
        image,
        image_content_factory,
        media_resource_factory,
        serializer_context):
    """
    Test serializing an ``ImageContent`` instance.
    """
    img_content = image_content_factory(
        image_resource=media_resource_factory(file=image),
        media_resource=media_resource_factory())

    serializer = ImageContentSerializer(
        img_content,
        context=serializer_context)
    request = serializer_context['request']

    image_serializer = serializers.MediaResourceSerializer(
        img_content.image_resource,
        context=serializer_context)
    media_serializer = serializers.MediaResourceSerializer(
        img_content.media_resource,
        context=serializer_context)

    expected = {
        'id': img_content.id,
        'description': img_content.description,
        'image_resource': image_serializer.data,
        'media_resource': media_serializer.data,
        'permissions': {
            'read': img_content.has_object_read_permission(request),
            'write': img_content.has_object_write_permission(request),
        }
    }

    assert serializer.data == expected


def test_update(
        image_content_factory,
        media_resource_factory,
        serializer_context):
    """
    Saving a bound serializer with valid data should update the image
    content the serializer is bound to.
    """
    content = image_content_factory()
    km_user = content.profile_item.topic.profile.km_user

    serializer_context['km_user'] = km_user

    media_resource = media_resource_factory(km_user=km_user)

    data = {
        'media_resource': media_resource.id,
    }

    serializer = ImageContentSerializer(
        content,
        context=serializer_context,
        data=data)
    assert serializer.is_valid()

    serializer.save()
    content.refresh_from_db()

    assert content.media_resource == media_resource


@pytest.mark.django_db
def test_validate_invalid_resource_pk(km_user_factory, serializer_context):
    """
    If there is no media resource corresponding to the ID given to the
    serializer, the serializer should not be valid.
    """
    serializer_context['km_user'] = km_user_factory()

    data = {
        'media_resource': 1,
    }

    serializer = ImageContentSerializer(context=serializer_context, data=data)

    assert not serializer.is_valid()
