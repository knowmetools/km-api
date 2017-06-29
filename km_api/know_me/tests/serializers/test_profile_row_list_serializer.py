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

    serializer = serializers.ProfileRowListSerializer(data=data)
    assert serializer.is_valid()

    row = serializer.save(group=group)

    assert row.name == data['name']
    assert row.row_type == data['row_type']
    assert row.group == group


def test_serialize(profile_row_factory):
    """
    Test serializing a profile.
    """
    row = profile_row_factory()
    serializer = serializers.ProfileRowListSerializer(row)

    expected = {
        'id': row.id,
        'name': row.name,
        'row_type': row.row_type,
    }

    assert serializer.data == expected
