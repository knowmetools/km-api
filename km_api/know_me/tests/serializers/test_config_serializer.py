from know_me import models, serializers


def test_serialize(api_rf, config_factory):
    """
    Test serializing a config instance.
    """
    config = config_factory()
    request = api_rf.get("/")

    serializer = serializers.ConfigSerializer(
        config, context={"request": request}
    )

    expected = {
        "minimum_app_version_ios": config.minimum_app_version_ios,
        "permissions": {
            "read": models.Config.has_read_permission(request),
            "write": models.Config.has_write_permission(request),
        },
    }

    assert serializer.data == expected
