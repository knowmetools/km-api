from unittest import mock

from know_me.journal import models, serializers, views


@mock.patch("know_me.journal.views.DRYPermissions.has_permission")
def test_check_permissions(mock_dry_permissions):
    """
    The view should use DRYPermissions to check object permissions.
    """
    view = views.EntryCommentDetailView()

    view.check_permissions(None)

    assert mock_dry_permissions.call_count == 1


def test_get_queryset(entry_comment_factory):
    """
    The view should operate on all comments.
    """
    entry_comment_factory()
    entry_comment_factory()
    entry_comment_factory()

    view = views.EntryCommentDetailView()

    assert list(view.get_queryset()) == list(models.EntryComment.objects.all())


def test_get_serializer_class():
    """
    The view should use the serializer for entry comments.
    """
    view = views.EntryCommentDetailView()
    expected = serializers.EntryCommentSerializer

    assert view.get_serializer_class() == expected
