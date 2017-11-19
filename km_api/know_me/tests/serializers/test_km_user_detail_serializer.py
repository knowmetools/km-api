from know_me import serializers


def test_serialize(
        api_rf,
        image,
        km_user_factory,
        profile_factory,
        serializer_context):
    """
    Test serializing a km_user.
    """
    km_user = km_user_factory(image=image)
    profile_factory(km_user=km_user)
    profile_factory(km_user=km_user)

    serializer = serializers.KMUserDetailSerializer(
        km_user,
        context=serializer_context)
    profile_serializer = serializers.ProfileListSerializer(
        km_user.profiles,
        context=serializer_context,
        many=True)

    request = serializer_context['request']

    url = api_rf.get(km_user.get_absolute_url()).build_absolute_uri()
    image_url = api_rf.get(km_user.image.url).build_absolute_uri()
    gallery_url = km_user.get_gallery_url(request)
    profile_list_url = km_user.get_profile_list_url(request)

    expected = {
        'id': km_user.id,
        'url': url,
        'name': km_user.name,
        'quote': km_user.quote,
        'image': image_url,
        'gallery_url': gallery_url,
        'profiles_url': profile_list_url,
        'profiles': profile_serializer.data,
    }

    assert serializer.data == expected


def test_update(km_user_factory):
    """
    Saving a bound serializer with valid data should update the km_user
    the serializer is bound to.
    """
    km_user = km_user_factory(quote='Old quote.')
    data = {
        'quote': 'New quote.',
    }

    serializer = serializers.KMUserDetailSerializer(
        km_user,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    km_user.refresh_from_db()

    assert km_user.quote == data['quote']
