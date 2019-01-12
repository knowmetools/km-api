from unittest import mock

from rest_framework.reverse import reverse

from know_me.profile import models


def test_create(profile_item_factory):
    """
    Test creating a list entry for a profile item.
    """
    models.ListEntry.objects.create(
        profile_item=profile_item_factory(), text="Test Profile Item"
    )


def test_get_absolute_url(list_entry_factory):
    """
    This method should return the absolute URL of the instance's detail
    view.
    """
    entry = list_entry_factory()
    expected = reverse(
        "know-me:profile:list-entry-detail", kwargs={"pk": entry.pk}
    )

    assert entry.get_absolute_url() == expected


@mock.patch("know_me.profile.models.ProfileItem.has_object_read_permission")
def test_has_object_read_permission(
    mock_parent_permission, api_rf, list_entry_factory
):
    """
    List entries should delegate the read permission check to their
    parent profile item.
    """
    entry = list_entry_factory()
    request = api_rf.get("/")

    expected = mock_parent_permission.return_value

    assert entry.has_object_read_permission(request) == expected
    assert mock_parent_permission.call_count == 1
    assert mock_parent_permission.call_args[0] == (request,)


@mock.patch("know_me.profile.models.ProfileItem.has_object_write_permission")
def test_has_object_write_permission(
    mock_parent_permission, api_rf, list_entry_factory
):
    """
    List entries should delegate the write permission check to their
    parent profile item.
    """
    entry = list_entry_factory()
    request = api_rf.get("/")

    expected = mock_parent_permission.return_value

    assert entry.has_object_write_permission(request) == expected
    assert mock_parent_permission.call_count == 1
    assert mock_parent_permission.call_args[0] == (request,)


def test_ordering(list_entry_factory, profile_item_factory):
    """
    List entries should be ordered with respect to their parent profile
    item.
    """
    item = profile_item_factory()

    l1 = list_entry_factory(profile_item=item)
    l2 = list_entry_factory(profile_item=item)
    l3 = list_entry_factory(profile_item=item)

    item.set_listentry_order([l3.id, l1.id, l2.id])

    assert list(item.list_entries.all()) == [l3, l1, l2]


def test_string_conversion(list_entry_factory):
    """
    Converting a list entry to a string should return the entry's text.
    """
    entry = list_entry_factory()

    assert str(entry) == entry.text
