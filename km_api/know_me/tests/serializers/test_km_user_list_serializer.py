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


def test_serialize(
        api_rf,
        image,
        km_user_factory,
        serializer_context):
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
    url_request = api_rf.get(km_user.get_absolute_url())

    expected = {
        'id': km_user.id,
        'image': image_url,
        'url': url_request.build_absolute_uri(),
        'name': km_user.user.get_short_name(),
        'quote': km_user.quote,
        'permissions': {
            'read': km_user.has_object_read_permission(request),
            'write': km_user.has_object_write_permission(request),
        }
    }

    assert serializer.data == expected
