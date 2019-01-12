from know_me.profile import serializers


def test_serialize(api_rf, media_resource_category_factory, serialized_time):
    """
    Test serializing a media resource category.
    """
    category = media_resource_category_factory()

    api_rf.user = category.km_user.user
    request = api_rf.get(category.get_absolute_url())

    serializer = serializers.MediaResourceCategorySerializer(
        category, context={"request": request}
    )

    expected = {
        "id": category.id,
        "url": request.build_absolute_uri(),
        "created_at": serialized_time(category.created_at),
        "updated_at": serialized_time(category.updated_at),
        "km_user_id": category.km_user.id,
        "name": category.name,
        "permissions": {
            "read": category.has_object_read_permission(request),
            "write": category.has_object_write_permission(request),
        },
    }

    assert serializer.data == expected


def test_validate():
    """
    The serializer should validate any data providing all the required
    fields.
    """
    data = {"name": "Test Category"}
    serializer = serializers.MediaResourceCategorySerializer(data=data)

    assert serializer.is_valid()
