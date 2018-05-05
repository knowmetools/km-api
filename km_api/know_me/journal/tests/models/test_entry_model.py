from unittest import mock

from rest_framework.reverse import reverse

from know_me.journal import models


def test_create(file, km_user_factory):
    """
    Test creating a new journal entry.
    """
    models.Entry.objects.create(
        attachment=file,
        km_user=km_user_factory(),
        text='My sample entry text.')


def test_get_absolute_url(entry_factory):
    """
    This method should return the absolute URL of the instance's detail
    view.
    """
    entry = entry_factory()
    expected = reverse(
        'know-me:journal:entry-detail',
        kwargs={'pk': entry.pk})

    assert entry.get_absolute_url() == expected


def test_get_comments_url(entry_factory):
    """
    This method should return the URL of the instance's comment list
    view.
    """
    entry = entry_factory()
    expected = reverse(
        'know-me:journal:entry-comment-list',
        kwargs={'pk': entry.pk})

    assert entry.get_comments_url() == expected


@mock.patch('know_me.models.KMUser.has_object_read_permission')
def test_has_object_read_permission(
        mock_parent_permission,
        api_rf,
        entry_factory):
    """
    Journal entries should delegate the read permission check to their
    parent Know Me user.
    """
    entry = entry_factory()
    request = api_rf.get('/')

    expected = mock_parent_permission.return_value

    assert entry.has_object_read_permission(request) == expected
    assert mock_parent_permission.call_count == 1
    assert mock_parent_permission.call_args[0] == (request,)


@mock.patch('know_me.models.KMUser.has_object_write_permission')
def test_has_object_write_permission(
        mock_parent_permission,
        api_rf,
        entry_factory):
    """
    Journal entries should delegate the write permission check to their
    parent Know Me user.
    """
    entry = entry_factory()
    request = api_rf.get('/')

    expected = mock_parent_permission.return_value

    assert entry.has_object_write_permission(request) == expected
    assert mock_parent_permission.call_count == 1
    assert mock_parent_permission.call_args[0] == (request,)


def test_ordering(entry_factory):
    """
    Journal entries should be ordered by most recently created.
    """
    e1 = entry_factory()
    e2 = entry_factory()
    e3 = entry_factory()

    assert list(models.Entry.objects.all()) == [e3, e2, e1]


def test_string_conversion(entry_factory):
    """
    Converting an entry to a string should return the time it was
    published.
    """
    entry = entry_factory()
    expected = 'Entry for {}'.format(entry.created_at)

    assert str(entry) == expected
