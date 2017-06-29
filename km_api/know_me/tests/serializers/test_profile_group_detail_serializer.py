from rest_framework.reverse import reverse

from know_me import serializers


def test_serialize(
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
    row_serializer = serializers.ProfileRowListSerializer(
        group.rows,
        many=True)

    expected = {
        'id': group.id,
        'url': reverse(
            'know-me:profile-group-detail',
            kwargs={
                'group_pk': group.pk,
                'profile_pk': group.profile.pk,
            },
            request=serializer_context['request']),
        'name': group.name,
        'is_default': group.is_default,
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
