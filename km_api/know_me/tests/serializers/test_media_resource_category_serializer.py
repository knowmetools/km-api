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
        context = serializer_context,
        data = data)
    assert serializer.is_valid()

    category = serializer.save(km_user=km_user)
    
    assert category.name == data['name']
    assert category.km_user == km_user
    

def test_serialize(api_rf, media_resource_category_factory, serializer_context):
    """
    Test serializing a Media Resource Category.
    """
    media_resource_category = media_resource_category_factory()

    serializer = serializers.MediaResourceCategorySerializer(
            media_resource_category,
            context = serializer_context)

    url_request = api_rf.get(media_resource_category.get_absolute_url())
    serializer_request = serializer_context['request']

    expected = {
        'id': media_resource_category.id,
        'url': url_request.build_absolute_uri(),
        'name': media_resource_category.name,
        'permissions' : {
            'read' : media_resource_category.has_object_read_permission(serializer_request),
            'write' : media_resource_category.has_object_write_permission(serializer_request),
        }
    }

    assert serializer.data == expected
