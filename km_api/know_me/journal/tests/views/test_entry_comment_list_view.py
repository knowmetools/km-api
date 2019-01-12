from unittest import mock

from know_me.journal import serializers, views


@mock.patch("know_me.journal.views.DRYPermissions.has_permission")
@mock.patch(
    "know_me.journal.views.permissions.HasEntryCommentListPermissions.has_permission"  # noqa
)
def test_check_permissions(mock_list_permissions, mock_dry_permissions):
    """
    The view should use the appropriate permissions checks.
    """
    view = views.EntryCommentListView()

    view.check_permissions(None)

    assert mock_dry_permissions.call_count == 1
    assert mock_list_permissions.call_count == 1


def test_get_queryset(entry_comment_factory, entry_factory):
    """
    The view should operate on the comments that belong to the journal
    entry specified in the URL.
    """
    entry = entry_factory()
    entry_comment_factory(entry=entry)
    entry_comment_factory()

    view = views.EntryCommentListView()
    view.kwargs = {"pk": entry.pk}

    assert list(view.get_queryset()) == list(entry.comments.all())


def test_get_serializer_class():
    """
    The view should use the serializer for entry comments.
    """
    view = views.EntryCommentListView()
    expected = serializers.EntryCommentSerializer

    assert view.get_serializer_class() == expected


def test_perform_create(api_rf, entry_factory, user_factory):
    """
    Creating a comment should attach it to the journal entry specified
    in the URL.
    """
    entry = entry_factory()
    user = user_factory()
    api_rf.user = user

    view = views.EntryCommentListView()
    view.kwargs = {"pk": entry.pk}
    view.request = api_rf.get("/")

    serializer = mock.Mock(name="Mock EntryCommentSerializer")

    result = view.perform_create(serializer)

    assert result == serializer.save.return_value
    assert serializer.save.call_count == 1
    assert serializer.save.call_args[1] == {"entry": entry, "user": user}
