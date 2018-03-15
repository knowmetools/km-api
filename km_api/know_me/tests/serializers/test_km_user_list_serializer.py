from know_me import serializers


def test_create(serializer_context, user_factory):
    """
    Saving a serializer containing valid data should create a new
    km_user.
    """
    user = user_factory()
    data = {
        'name': "John",
        'quote': "Hi, I'm John",
    }

    serializer = serializers.KMUserListSerializer(
        context=serializer_context,
        data=data)
    assert serializer.is_valid()

    serializer.save(user=user)
    km_user = user.km_user

    assert km_user.user.get_short_name() == data['name']
    assert km_user.quote == data['quote']
    assert km_user.user == user


def test_serialize(api_rf, image, km_user_factory, serialized_time):
    """
    Test serializing a km_user.
    """
    km_user = km_user_factory(image=image)
    api_rf.user = km_user.user
    request = api_rf.get(km_user.get_absolute_url())

    serializer = serializers.KMUserListSerializer(
        km_user,
        context={'request': request})

    image_url = api_rf.get(km_user.image.url).build_absolute_uri()

    categories_request = api_rf.get(
        km_user.get_media_resource_category_list_url())
    categories_url = categories_request.build_absolute_uri()

    media_resources_request = api_rf.get(km_user.get_media_resource_list_url())
    media_resources_url = media_resources_request.build_absolute_uri()

    profiles_request = api_rf.get(km_user.get_profile_list_url())
    profiles_url = profiles_request.build_absolute_uri()

    expected = {
        'id': km_user.id,
        'url': request.build_absolute_uri(),
        'created_at': serialized_time(km_user.created_at),
        'updated_at': serialized_time(km_user.updated_at),
        'image': image_url,
        'media_resource_categories_url': categories_url,
        'media_resources_url': media_resources_url,
        'name': km_user.user.get_short_name(),
        'profiles_url': profiles_url,
        'quote': km_user.quote,
        'permissions': {
            'read': km_user.has_object_read_permission(request),
            'write': km_user.has_object_write_permission(request),
        }
    }

    assert serializer.data == expected
