from unittest import mock

from know_me.journal import models


def test_create(entry_factory, user_factory):
    """
    Test creating a new comment on a journal entry.
    """
    models.EntryComment.objects.create(
        entry=entry_factory(),
        text='My comment text.',
        user=user_factory())


@mock.patch('know_me.journal.models.Entry.has_object_write_permission')
def test_has_object_destroy_permission_other(
        mock_parent_permission,
        api_rf,
        entry_comment_factory):
    """
    The permissions required to destroy a comment on a journal entry
    should be equivalent to those required to write to a journal entry.
    """
    comment = entry_comment_factory()
    request = api_rf.get('/')

    expected = mock_parent_permission.return_value

    assert comment.has_object_destroy_permission(request) == expected
    assert mock_parent_permission.call_count == 1
    assert mock_parent_permission.call_args[0] == (request,)


def test_has_object_destroy_permission_owner(api_rf, entry_comment_factory):
    """
    The owner of the comment should be able to destroy it.
    """
    comment = entry_comment_factory()
    api_rf.user = comment.user
    request = api_rf.get('/')

    assert comment.has_object_destroy_permission(request)


@mock.patch('know_me.journal.models.Entry.has_object_read_permission')
def test_has_object_read_permission(
        mock_parent_permission,
        api_rf,
        entry_comment_factory):
    """
    Journal entry comments should delegate the read permission check to
    their parent entry.
    """
    comment = entry_comment_factory()
    request = api_rf.get('/')

    expected = mock_parent_permission.return_value

    assert comment.has_object_read_permission(request) == expected
    assert mock_parent_permission.call_count == 1
    assert mock_parent_permission.call_args[0] == (request,)


def test_has_object_update_permission(api_rf, entry_comment_factory):
    """
    The user who made the comment should have permission to update it.
    """
    comment = entry_comment_factory()
    api_rf.user = comment.user
    request = api_rf.get('/')

    assert comment.has_object_update_permission(request)


def test_has_object_update_permission_other(api_rf, entry_comment_factory):
    """
    Any other user should not have permission to update a comment.
    """
    comment = entry_comment_factory()
    request = api_rf.get('/')

    assert not comment.has_object_update_permission(request)


def test_has_object_write_permission(entry_comment_factory):
    """
    No one should have write permission on a comment.
    """
    comment = entry_comment_factory()

    assert not comment.has_object_write_permission(None)
