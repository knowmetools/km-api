from know_me import serializers


def test_serialize(
        api_rf,
        profile_group_factory,
        profile_row_factory,
        serializer_context):
    """
    Test serializing a profile group.
    """
    group = profile_group_factory()
    profile_row_factory(group=group)
    profile_row_factory(group=group)

    serializer = serializers.ProfileGroupDetailSerializer(
        group,
        context=serializer_context)
    row_serializer = serializers.ProfileRowSerializer(
        group.rows,
        context=serializer_context,
        many=True)

    url_request = api_rf.get(group.get_absolute_url())
    row_list_request = api_rf.get(group.get_row_list_url())

    expected = {
        'id': group.id,
        'url': url_request.build_absolute_uri(),
        'name': group.name,
        'is_default': group.is_default,
        'rows_url': row_list_request.build_absolute_uri(),
        'rows': row_serializer.data,
    }

    assert serializer.data == expected


def test_update(profile_group_factory):
    """
    Saving a bound serializer with valid data should update the profile
    group bound to the serializer.
    """
    group = profile_group_factory(name='Old Group')
    data = {
        'name': 'New Group',
    }

    serializer = serializers.ProfileGroupDetailSerializer(
        group,
        data=data,
        partial=True)
    assert serializer.is_valid()

    serializer.save()
    group.refresh_from_db()

    assert group.name == data['name']
