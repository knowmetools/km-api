from know_me import serializers


def test_create(
        media_resource_factory,
        profile_row_factory,
        serializer_context):
    """
    Saving a serializer with valid data should create a new profile
    item.
    """
    row = profile_row_factory()
    media_resource = media_resource_factory(profile=row.group.profile)

    serializer_context['profile'] = row.group.profile

    data = {
        'media_resource': media_resource.pk,
        'name': 'My Profile Item',
        'text': 'Some sample text.',
    }

    serializer = serializers.ProfileItemSerializer(
        context=serializer_context,
        data=data)
    assert serializer.is_valid(), serializer.errors

    item = serializer.save(row=row)

    assert item.name == data['name']
    assert item.text == data['text']

    assert item.media_resource == media_resource
    assert item.row == row


def test_create_other_user_media_resource(
        media_resource_factory,
        profile_factory,
        serializer_context):
    """
    Users should not be able to attach a media resource from a different
    profile to their profile item.
    """
    media_resource = media_resource_factory()
    profile = profile_factory()

    serializer_context['profile'] = profile

    data = {
        'media_resource': media_resource.pk,
        'name': 'My Profile Item',
        'text': 'I tried to attach a media resource from another profile.',
    }

    serializer = serializers.ProfileItemSerializer(
        context=serializer_context,
        data=data)

    assert not serializer.is_valid()


def test_serialize(
        api_rf,
        media_resource_factory,
        profile_item_factory,
        serializer_context):
    """
    Test serializing a profile item.
    """
    media_resource = media_resource_factory()
    item = profile_item_factory(media_resource=media_resource)

    serializer = serializers.ProfileItemSerializer(
        item,
        context=serializer_context)
    media_resource_serializer = serializers.MediaResourceSerializer(
        media_resource,
        context=serializer_context)

    url_request = api_rf.get(item.get_absolute_url())

    expected = {
        'id': item.id,
        'url': url_request.build_absolute_uri(),
        'name': item.name,
        'text': item.text,
        'media_resource': media_resource.pk,
        'media_resource_info': media_resource_serializer.data,
    }

    assert serializer.data == expected


def test_update(profile_item_factory, serializer_context):
    """
    Saving a bound serializer with additional data should update the
    profile item bound to the serializer.
    """
    item = profile_item_factory(name='Old Name')
    data = {
        'name': 'New Name',
    }

    serializer = serializers.ProfileItemSerializer(
        item,
        context=serializer_context,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    item.refresh_from_db()

    assert item.name == data['name']
