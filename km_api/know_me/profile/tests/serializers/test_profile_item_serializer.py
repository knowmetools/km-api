import pytest

from rest_framework.serializers import ValidationError

from know_me.profile import serializers


def test_serialize(
        api_rf,
        image,
        media_resource_factory,
        profile_item_factory,
        serialized_time):
    """
    Test serializing a profile item.
    """
    media_resource = media_resource_factory()
    item = profile_item_factory(
        image=image,
        media_resource=media_resource,
        topic__profile__km_user=media_resource.km_user)

    api_rf.user = media_resource.km_user.user
    request = api_rf.get(item.get_absolute_url())

    serializer = serializers.ProfileItemSerializer(
        item,
        context={'request': request})
    media_resource_serializer = serializers.MediaResourceSerializer(
        media_resource,
        context={'request': request})

    image_url = api_rf.get(item.image.url).build_absolute_uri()

    expected = {
        'id': item.id,
        'url': request.build_absolute_uri(),
        'created_at': serialized_time(item.created_at),
        'updated_at': serialized_time(item.updated_at),
        'description': item.description,
        'image': image_url,
        'media_resource': media_resource_serializer.data,
        'name': item.name,
        'permissions': {
            'read': item.has_object_read_permission(request),
            'write': item.has_object_write_permission(request),
        },
        'topic_id': item.topic.id,
    }

    assert serializer.data == expected


def test_validate(image, media_resource_factory):
    """
    Test validating the data required to create a new profile item.
    """
    media_resource = media_resource_factory()
    data = {
        'description': 'My test profile item.',
        'image': image,
        'media_resource_id': media_resource.id,
        'name': 'Test Item',
    }
    serializer = serializers.ProfileItemSerializer(
        context={'km_user': media_resource.km_user},
        data=data)

    assert serializer.is_valid()


def test_validate_media_resource_id_by_context(media_resource_factory):
    """
    If the serializer is not bound to a profile item instance, it should
    use context to determine the expected owner of the provided media
    resource.
    """
    media_resource = media_resource_factory()
    serializer = serializers.ProfileItemSerializer(
        context={'km_user': media_resource.km_user})

    result = serializer.validate_media_resource_id(media_resource)

    assert result == media_resource


def test_validate_media_resource_id_by_item(
        km_user_factory,
        media_resource_factory,
        profile_item_factory):
    """
    If the serializer is bound to a profile item, it should make sure
    the provided media resource belongs to the same user as the profile
    item.
    """
    km_user = km_user_factory()
    media_resource = media_resource_factory(km_user=km_user)
    profile_item = profile_item_factory(topic__profile__km_user=km_user)

    serializer = serializers.ProfileItemSerializer(profile_item)
    result = serializer.validate_media_resource_id(media_resource)

    assert result == media_resource


def test_validate_media_resource_id_missing_context():
    """
    If the serializer is not bound and a Know Me user isn't provided as
    context, an AssertionError should be raised.
    """
    serializer = serializers.ProfileItemSerializer()

    with pytest.raises(AssertionError):
        serializer.validate_media_resource_id(None)


def test_validate_media_resource_id_other_user(
        media_resource_factory,
        profile_item_factory):
    """
    If the provided media resource is owned by a different user than the
    one given to the serializer, a validation error should be raised.
    """
    item = profile_item_factory()
    media_resource = media_resource_factory()
    serializer = serializers.ProfileItemSerializer(item)

    with pytest.raises(ValidationError):
        serializer.validate_media_resource_id(media_resource)
