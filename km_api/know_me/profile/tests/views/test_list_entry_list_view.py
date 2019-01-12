from unittest import mock

from know_me.profile import serializers, views


@mock.patch("know_me.profile.views.DRYPermissions.has_permission")
@mock.patch(
    "know_me.profile.views.permissions.HasListEntryListPermissions.has_permission"  # noqa
)
def test_check_permissions(mock_list_permissions, mock_dry_permissions):
    """
    The view should use the appropriate permissions checks.
    """
    view = views.ListEntryListView()

    view.check_permissions(None)

    assert mock_dry_permissions.call_count == 1
    assert mock_list_permissions.call_count == 1


def test_get_queryset(list_entry_factory, profile_item_factory):
    """
    The view should only operate on profile items belonging to the
    specified topic.
    """
    item = profile_item_factory()
    list_entry_factory(profile_item=item)
    list_entry_factory()

    view = views.ListEntryListView()
    view.kwargs = {"pk": item.pk}

    assert list(view.get_queryset()) == list(item.list_entries.all())


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.ListEntryListView()
    expected = serializers.ListEntrySerializer

    assert view.get_serializer_class() == expected


def test_perform_create(profile_item_factory):
    """
    Creating a new profile item with the view should associate the item
    with the topic whose ID is given in the URL.
    """
    item = profile_item_factory()

    view = views.ListEntryListView()
    view.kwargs = {"pk": item.pk}

    serializer = mock.Mock(name="Mock ListEntrySerializer")

    result = view.perform_create(serializer)

    assert result == serializer.save.return_value
    assert serializer.save.call_count == 1
    assert serializer.save.call_args[1] == {"profile_item": item}
