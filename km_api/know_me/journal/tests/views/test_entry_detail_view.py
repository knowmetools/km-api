from unittest import mock

from know_me.journal import models, serializers, views


@mock.patch(
    "know_me.journal.views.DRYPermissions.has_object_permission", autospec=True
)
def test_check_object_permissions(mock_dry_permissions, api_rf):
    """
    The view should check the permissions on the model.
    """
    view = views.EntryDetailView()

    view.check_object_permissions(None, None)

    assert mock_dry_permissions.call_count == 1


def test_get_queryset(entry_factory):
    """
    The view should operate on all journal entries.
    """
    entry_factory()
    entry_factory()
    entry_factory()

    view = views.EntryDetailView()
    expected = models.Entry.objects.all()

    assert list(view.get_queryset()) == list(expected)


def test_get_serializer_class():
    """
    The view should utilize the detail serializer for journal entries.
    """
    view = views.EntryDetailView()
    expected = serializers.EntryDetailSerializer

    assert view.get_serializer_class() == expected


def test_get_subscription_owner():
    """
    The view's method to get the owner of a subscription should return
    the owner of the journal the entry was made on.
    """
    entry = mock.MagicMock(name="Mock Journal Entry")
    request = mock.MagicMock(name="Mock Request")
    expected = entry.km_user.user

    view = views.EntryDetailView()

    assert view.get_subscription_owner(request, entry) == expected
