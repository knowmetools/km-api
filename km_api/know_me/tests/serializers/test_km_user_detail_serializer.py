from know_me import serializers


def test_serialize(
        api_rf,
        km_user_factory,
        profile_group_factory,
        serializer_context):
    """
    Test serializing a km_user.
    """
    km_user = km_user_factory()
    profile_group_factory(km_user=km_user)
    profile_group_factory(km_user=km_user)

    serializer = serializers.KMUserDetailSerializer(
        km_user,
        context=serializer_context)
    group_serializer = serializers.ProfileGroupListSerializer(
        km_user.groups,
        context=serializer_context,
        many=True)

    url_request = api_rf.get(km_user.get_absolute_url())
    gallery_request = api_rf.get(km_user.get_gallery_url())
    group_list_request = api_rf.get(km_user.get_group_list_url())

    expected = {
        'id': km_user.id,
        'url': url_request.build_absolute_uri(),
        'name': km_user.name,
        'quote': km_user.quote,
        'gallery_url': gallery_request.build_absolute_uri(),
        'groups_url': group_list_request.build_absolute_uri(),
        'groups': group_serializer.data
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
