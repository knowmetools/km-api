from know_me import serializers


def test_serialize(media_resource_category_factory):
    """
    Test serializing a media resource category.
    """
    category = media_resource_category_factory()
    serializer = serializers.MediaResourceCategorySerializer(category)

    expected = {
        'id': category.id,
        'km_user': category.km_user.id,
        'name': category.name,
    }

    assert serializer.data == expected


def test_validate():
    """
    The serializer should validate any data providing all the required
    fields.
    """
    data = {
        'name': 'Test Category',
    }
    serializer = serializers.MediaResourceCategorySerializer(data=data)

    assert serializer.is_valid()
