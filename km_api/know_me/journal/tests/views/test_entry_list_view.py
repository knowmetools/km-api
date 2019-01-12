import datetime
from unittest import mock

from django.utils import timezone

from know_me.journal import models, serializers, views


@mock.patch(
    "know_me.journal.views.DRYPermissions.has_permission", autospec=True
)
@mock.patch(
    "know_me.journal.views.HasKMUserAccess.has_permission", autospec=True
)
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
    "know_me.journal.views.KMUserAccessFilterBackend.filter_queryset",
    autospec=True,
    return_value=models.Entry.objects.none(),
)
def test_filter_queryset(mock_filter, api_rf):
    """
    The queryset returned by the view should be passed through a filter
    to restrict access.
    """
    view = views.EntryListView()
    view.request = view.initialize_request(api_rf.get("/"))

    queryset = models.Entry.objects.none()

    view.filter_queryset(queryset)

    assert mock_filter.call_count == 1


def test_filter_queryset_created_after(api_rf, entry_factory, km_user_factory):
    """
    The client should be able to use GET parameters to provide a
    start timestamp for the result set.
    """
    km_user = km_user_factory()
    api_rf.user = km_user.user

    new = entry_factory(km_user=km_user)

    now = timezone.now()
    earlier = now - datetime.timedelta(hours=1)
    earliest = earlier - datetime.timedelta(hours=1)

    with mock.patch("django.utils.timezone.now", return_value=earliest):
        entry_factory()

    view = views.EntryListView()
    view.kwargs = {"pk": km_user.pk}
    view.request = view.initialize_request(
        api_rf.get("/", {"created_at__gte": earlier})
    )

    query = models.Entry.objects.all()

    assert list(view.filter_queryset(query)) == [new]


def test_filter_queryset_created_before(
    api_rf, entry_factory, km_user_factory
):
    """
    The client should be able to use GET parameters to provide a max
    'created_at' value.
    """
    km_user = km_user_factory()
    api_rf.user = km_user.user

    old_entry = entry_factory(km_user=km_user)

    now = timezone.now()
    later = now + datetime.timedelta(hours=1)
    latest = later + datetime.timedelta(hours=1)

    with mock.patch("django.utils.timezone.now", return_value=latest):
        entry_factory()

    view = views.EntryListView()
    view.kwargs = {"pk": km_user.pk}
    view.request = view.initialize_request(
        api_rf.get("/", {"created_at__lte": later})
    )

    query = models.Entry.objects.all()

    assert list(view.filter_queryset(query)) == [old_entry]


def test_filter_queryset_keyword(api_rf, entry_factory, km_user_factory):
    """
    The client should be able to perform a keyword search on the journal
    entries.
    """
    km_user = km_user_factory()
    api_rf.user = km_user.user

    foo_entry = entry_factory(
        km_user=km_user, text="This is an entry about foo only."
    )
    entry_factory(km_user=km_user, text="This is an entry about bar only.")

    view = views.EntryListView()
    view.kwargs = {"pk": km_user.pk}
    view.request = view.initialize_request(api_rf.get("/", {"q": "foo"}))

    query = models.Entry.objects.all()

    assert list(view.filter_queryset(query)) == [foo_entry]


def test_get_queryset(api_rf, entry_factory):
    """
    The view should act on all journal entries.
    """
    entry_factory()
    entry_factory()
    entry_factory()

    view = views.EntryListView()
    view.request = api_rf.get("/")

    expected = models.Entry.objects.all()

    assert list(view.get_queryset()) == list(expected)


def test_get_serializer_class_get(api_rf):
    """
    The view should use the entry list serializer for a GET request.
    """
    view = views.EntryListView()
    view.request = api_rf.get("/")

    expected = serializers.EntryListSerializer

    assert view.get_serializer_class() == expected


def test_get_serializer_class_missing_request(api_rf):
    """
    When the documentation is generated, no request is provided to the
    view. In this case we should return the detail serializer.
    """
    view = views.EntryListView()
    view.request = None

    expected = serializers.EntryDetailSerializer

    assert view.get_serializer_class() == expected


def test_get_serializer_class_post(api_rf):
    """
    The view should use the entry detail serializer for a POST request.
    """
    view = views.EntryListView()
    view.request = api_rf.post("/")

    expected = serializers.EntryDetailSerializer

    assert view.get_serializer_class() == expected


def test_perform_create(km_user_factory):
    """
    The view should pass the Know Me user specified in the URL to the
    serializer when creating a new Journal Entry.
    """
    km_user = km_user_factory()
    serializer = mock.Mock(name="Mock EntryDetailSerializer")

    view = views.EntryListView()
    view.kwargs = {"pk": km_user.pk}

    assert view.perform_create(serializer) == serializer.save.return_value
    assert serializer.save.call_count == 1
    assert serializer.save.call_args[1] == {"km_user": km_user}
