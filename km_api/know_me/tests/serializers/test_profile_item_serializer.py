from know_me import serializers


def test_create(gallery_item_factory, profile_row_factory, serializer_context):
    """
    Saving a serializer with valid data should create a new profile
    item.
    """
    row = profile_row_factory()
    gallery_item = gallery_item_factory(profile=row.group.profile)

    serializer_context['profile'] = row.group.profile

    data = {
        'gallery_item': gallery_item.pk,
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

    assert item.gallery_item == gallery_item
    assert item.row == row


def test_create_other_user_gallery_item(
        gallery_item_factory,
        profile_factory,
        serializer_context):
    """
    Users should not be able to attach a gallery item from a different
    profile to their profile item.
    """
    gallery_item = gallery_item_factory()
    profile = profile_factory()

    serializer_context['profile'] = profile

    data = {
        'gallery_item': gallery_item.pk,
        'name': 'My Profile Item',
        'text': 'I tried to attach a gallery item from another profile.',
    }

    serializer = serializers.ProfileItemSerializer(
        context=serializer_context,
        data=data)

    assert not serializer.is_valid()


def test_serialize(
        api_rf,
        gallery_item_factory,
        profile_item_factory,
        serializer_context):
    """
    Test serializing a profile item.
    """
    gallery_item = gallery_item_factory()
    item = profile_item_factory(gallery_item=gallery_item)

    serializer = serializers.ProfileItemSerializer(
        item,
        context=serializer_context)
    gallery_item_serializer = serializers.GalleryItemSerializer(
        gallery_item,
        context=serializer_context)

    url_request = api_rf.get(item.get_absolute_url())

    expected = {
        'id': item.id,
        'url': url_request.build_absolute_uri(),
        'name': item.name,
        'text': item.text,
        'gallery_item': gallery_item.pk,
        'gallery_item_info': gallery_item_serializer.data,
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
