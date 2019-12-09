from know_me.profile import serializers


def test_serialize(
    api_rf,
    km_user_factory,
    media_resource_cover_style_factory,
    serialized_time,
):
    """
    Test serializing a media resource cover style.
    """
    # Note that it is not intended for a resource to have both a file
    # and link defined at the same time. This is enforced by serializer
    # validation. We do it here for testing purposes.
    km_user = km_user_factory()
    resource = media_resource_cover_style_factory(km_user=km_user)

    api_rf.user = km_user.user
    request = api_rf.get(resource.get_absolute_url())

    serializer = serializers.MediaResourceCoverStyleSerializer(
        resource, context={"request": request}
    )

    expected = {
        "id": resource.id,
        "url": request.build_absolute_uri(),
        "created_at": serialized_time(resource.created_at),
        "updated_at": serialized_time(resource.updated_at),
        "cover_style_override": resource.cover_style_override,
        "name": resource.name,
        "permissions": {
            "read": resource.has_object_read_permission(request),
            "write": resource.has_object_write_permission(request),
        },
    }

    assert serializer.data == expected


def test_validate_serializer():
    """
    The serializer should validate when provided a file and name.
    """
    data = {"name": "Bob"}
    serializer = serializers.MediaResourceCoverStyleSerializer(data=data)

    assert serializer.is_valid()
