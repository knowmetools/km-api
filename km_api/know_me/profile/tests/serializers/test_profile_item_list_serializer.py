from know_me.profile import serializers


def test_serialize(api_rf, image, profile_item_factory, serialized_time):
    """
    Test serializing a profile item.
    """
    item = profile_item_factory(image=image)
    api_rf.user = item.topic.profile.km_user.user
    request = api_rf.get(item.get_absolute_url())

    serializer = serializers.ProfileItemListSerializer(
        item,
        context={'request': request})

    list_entries_request = api_rf.get(item.get_list_entries_url())
    list_entries_url = list_entries_request.build_absolute_uri()

    image_url = api_rf.get(item.image.url).build_absolute_uri()

    expected = {
        'id': item.id,
        'url': request.build_absolute_uri(),
        'created_at': serialized_time(item.created_at),
        'updated_at': serialized_time(item.updated_at),
        'description': item.description,
        'image': image_url,
        'list_entries_url': list_entries_url,
        'name': item.name,
        'permissions': {
            'read': item.has_object_read_permission(request),
            'write': item.has_object_write_permission(request),
        },
        'topic_id': item.topic.id,
    }

    assert serializer.data == expected
