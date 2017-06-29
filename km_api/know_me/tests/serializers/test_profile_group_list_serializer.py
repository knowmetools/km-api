from rest_framework.reverse import reverse

from know_me import serializers


def test_create(profile_factory, serializer_context):
    """
    Saving a serializer instance with valid data should create a new
    profile group.
    """
    profile = profile_factory()
    data = {
        'name': 'Profile Group',
        'is_default': True,
    }

    serializer = serializers.ProfileGroupListSerializer(
        context=serializer_context,
        data=data)
    assert serializer.is_valid()

    group = serializer.save(profile=profile)

    assert group.name == data['name']
    assert group.profile == profile
    assert group.is_default == data['is_default']


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

    serializer = serializers.ProfileGroupListSerializer(
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
