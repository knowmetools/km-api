from unittest import mock

from know_me.journal import models, serializers, views


@mock.patch(
    'know_me.journal.views.DRYPermissions.has_permission',
    autospec=True)
@mock.patch(
    'know_me.journal.views.HasKMUserAccess.has_permission',
    autospec=True)
def test_check_permissions(mock_km_user_permission, mock_dry_permissions):
    """
    The view should check for model permissions as well as if the
    requesting user has access to the parent Know Me user.
    """
    view = views.EntryListView()

    view.check_permissions(None)

    assert mock_km_user_permission.call_count == 1
    assert mock_dry_permissions.call_count == 1


@mock.patch(
    'know_me.journal.views.KMUserAccessFilterBackend.filter_queryset',
    autospec=True)
def test_filter_queryset(mock_filter):
    """
    The queryset returned by the view should be passed through a filter
    to restrict access.
    """
    view = views.EntryListView()
    view.request = None

    queryset = models.Entry.objects.none()

    view.filter_queryset(queryset)

    assert mock_filter.call_count == 1


def test_get_queryset(api_rf, entry_factory):
    """
    The view should act on all journal entries.
    """
    entry_factory()
    entry_factory()
    entry_factory()

    view = views.EntryListView()
    view.request = api_rf.get('/')

    expected = models.Entry.objects.all()

    assert list(view.get_queryset()) == list(expected)


def test_get_serializer_class_get(api_rf):
    """
    The view should use the entry list serializer for a GET request.
    """
    view = views.EntryListView()
    view.request = api_rf.get('/')

    expected = serializers.EntryListSerializer

    assert view.get_serializer_class() == expected


def test_get_serializer_class_post(api_rf):
    """
    The view should use the entry detail serializer for a POST request.
    """
    view = views.EntryListView()
    view.request = api_rf.post('/')

    expected = serializers.EntryDetailSerializer

    assert view.get_serializer_class() == expected


def test_perform_create(km_user_factory):
    """
    The view should pass the Know Me user specified in the URL to the
    serializer when creating a new Journal Entry.
    """
    km_user = km_user_factory()
    serializer = mock.Mock(name='Mock EntryDetailSerializer')

    view = views.EntryListView()
    view.kwargs = {'pk': km_user.pk}

    assert view.perform_create(serializer) == serializer.save.return_value
    assert serializer.save.call_count == 1
    assert serializer.save.call_args[1] == {'km_user': km_user}
