from rest_framework.reverse import reverse

from know_me import models, serializers


def test_create(profile_group_factory):
    """
    Saving a serializer with valid data should create a new profile row.
    """
    group = profile_group_factory()
    data = {
        'name': 'Test Row',
        'row_type': models.ProfileRow.TEXT,
    }

    serializer = serializers.ProfileRowSerializer(data=data)
    assert serializer.is_valid()

    row = serializer.save(group=group)

    assert row.name == data['name']
    assert row.row_type == data['row_type']
    assert row.group == group


def test_serialize(api_rf, profile_row_factory, serializer_context):
    """
    Test serializing a profile.
    """
    row = profile_row_factory()
    serializer = serializers.ProfileRowSerializer(
        row,
        context=serializer_context)

    item_list_request = api_rf.get(row.get_item_list_url())

    expected = {
        'id': row.id,
        'url': reverse(
            'know-me:profile-row-detail',
            kwargs={
                'group_pk': row.group.pk,
                'profile_pk': row.group.profile.pk,
                'row_pk': row.pk,
            },
            request=serializer_context['request']),
        'name': row.name,
        'row_type': row.row_type,
        'items_url': item_list_request.build_absolute_uri(),
    }

    assert serializer.data == expected
