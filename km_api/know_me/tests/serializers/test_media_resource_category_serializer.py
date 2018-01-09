from know_me import serializers


def test_create(km_user_factory, serializer_context):
    """
    Saving a serializer containing valid data should create a new
    media resource attached to the given km_user.
    """
    km_user = km_user_factory()

    data = {
            'name': 'Test Media Resource Category',
    }

    serializer = serializers.MediaResourceCategorySerializer(
        context=serializer_context,
        data=data)
    assert serializer.is_valid()

    category = serializer.save(km_user=km_user)

    assert category.name == data['name']
    assert category.km_user == km_user


def test_serialize(api_rf,
                   media_resource_category_factory,
                   serializer_context):
    """
    Test serializing a Media Resource Category.
    """
    category = media_resource_category_factory()

    serializer = serializers.MediaResourceCategorySerializer(
            category,
            context=serializer_context)

    url_request = api_rf.get(category.get_absolute_url())
    serializer_request = serializer_context['request']

    hr = category.has_object_read_permission(serializer_request)
    hw = category.has_object_write_permission(serializer_request)

    expected = {
        'id': category.id,
        'url': url_request.build_absolute_uri(),
        'name': category.name,
        'permissions': {
            'read': hr,
            'write': hw,
        }
    }

    assert serializer.data == expected
