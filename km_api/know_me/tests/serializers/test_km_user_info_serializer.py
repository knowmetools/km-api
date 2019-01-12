from know_me import serializers


def test_serialize(api_rf, image, km_user_factory):
    """
    Test serializing a Know Me user.
    """
    km_user = km_user_factory(image=image)
    request = api_rf.get(km_user.get_absolute_url())

    serializer = serializers.KMUserInfoSerializer(
        km_user, context={"request": request}
    )

    image_request = api_rf.get(km_user.image.url)
    image_url = image_request.build_absolute_uri()

    expected = {"image": image_url, "name": km_user.name}

    assert serializer.data == expected
