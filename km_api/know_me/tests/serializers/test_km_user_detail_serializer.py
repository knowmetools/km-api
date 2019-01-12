from know_me import serializers
from know_me.profile.factories import ProfileFactory
from know_me.profile.serializers import ProfileListSerializer


def test_serialize(api_rf, image, km_user_factory):
    """
    Test serializing a km_user.
    """
    km_user = km_user_factory(image=image)
    api_rf.user = km_user.user
    request = api_rf.get("/")

    ProfileFactory(km_user=km_user)
    ProfileFactory(km_user=km_user)

    api_rf.user = km_user.user
    request = api_rf.get("/")

    serializer = serializers.KMUserDetailSerializer(
        km_user, context={"request": request}
    )
    list_serializer = serializers.KMUserListSerializer(
        km_user, context={"request": request}
    )

    profile_serializer = ProfileListSerializer(
        km_user.profiles, context={"request": request}, many=True
    )

    additional = {"profiles": profile_serializer.data}

    expected = dict(list_serializer.data.items())
    expected.update(additional)

    assert serializer.data == expected


def test_update(km_user_factory):
    """
    Saving a bound serializer with valid data should update the km_user
    the serializer is bound to.
    """
    km_user = km_user_factory(quote="Old quote.")
    data = {"quote": "New quote."}

    serializer = serializers.KMUserDetailSerializer(
        km_user, data=data, partial=True
    )
    assert serializer.is_valid()

    serializer.save()
    km_user.refresh_from_db()

    assert km_user.quote == data["quote"]
