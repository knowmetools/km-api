import pytest

from rest_framework.serializers import ValidationError

from know_me.profile import serializers


def test_serialize(
        api_rf,
        image,
        list_entry_factory,
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

    list_entry_factory(profile_item=item)
    list_entry_factory(profile_item=item)

    serializer = serializers.ProfileItemDetailSerializer(
        item,
        context={'request': request})
    list_serializer = serializers.ProfileItemListSerializer(
        item,
        context={'request': request})

    list_entry_serializer = serializers.ListEntrySerializer(
        item.list_entries.all(),
        context={'request': request},
        many=True)
    media_resource_serializer = serializers.MediaResourceSerializer(
        media_resource,
        context={'request': request})

    additional = {
        'list_entries': list_entry_serializer.data,
        'media_resource': media_resource_serializer.data,
    }

    expected = dict(list_serializer.data.items())
    expected.update(additional)

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
    serializer = serializers.ProfileItemDetailSerializer(
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
    serializer = serializers.ProfileItemDetailSerializer(
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

    serializer = serializers.ProfileItemDetailSerializer(profile_item)
    result = serializer.validate_media_resource_id(media_resource)

    assert result == media_resource


def test_validate_media_resource_id_missing_context(media_resource_factory):
    """
    If the serializer is not bound and a Know Me user isn't provided as
    context, an AssertionError should be raised.
    """
    resource = media_resource_factory()
    serializer = serializers.ProfileItemDetailSerializer()

    with pytest.raises(AssertionError):
        serializer.validate_media_resource_id(resource)


def test_validate_media_resource_id_null(
        km_user_factory,
        media_resource_factory,
        profile_item_factory):
    """
    Setting ``media_resource_id`` to ``None`` should detach the media resource
    from the profile item.

    Regression test for #321
    """
    km_user = km_user_factory()
    resource = media_resource_factory(km_user=km_user)
    item = profile_item_factory(
        media_resource=resource,
        topic__profile__km_user=km_user)

    data = {
        'media_resource_id': None,
    }
    serializer = serializers.ProfileItemDetailSerializer(
        item,
        data=data,
        partial=True)

    assert serializer.is_valid()


def test_validate_media_resource_id_other_user(
        media_resource_factory,
        profile_item_factory):
    """
    If the provided media resource is owned by a different user than the
    one given to the serializer, a validation error should be raised.
    """
    item = profile_item_factory()
    media_resource = media_resource_factory()
    serializer = serializers.ProfileItemDetailSerializer(item)

    with pytest.raises(ValidationError):
        serializer.validate_media_resource_id(media_resource)
