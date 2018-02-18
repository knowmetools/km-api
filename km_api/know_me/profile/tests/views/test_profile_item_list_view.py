from unittest import mock

from know_me.profile import serializers, views


@mock.patch('know_me.profile.views.DRYPermissions.has_permission')
@mock.patch('know_me.profile.views.permissions.HasProfileItemListPermissions.has_permission')  # noqa
def test_check_permissions(mock_list_permissions, mock_dry_permissions):
    """
    The view should use the appropriate permissions checks.
    """
    view = views.ProfileItemListView()

    view.check_permissions(None)

    assert mock_dry_permissions.call_count == 1
    assert mock_list_permissions.call_count == 1


def test_get_queryset(profile_item_factory, profile_topic_factory):
    """
    The view should only operate on profile items belonging to the
    specified topic.
    """
    topic = profile_topic_factory()
    profile_item_factory(topic=topic)
    profile_item_factory()

    view = views.ProfileItemListView()
    view.kwargs = {'pk': topic.pk}

    assert list(view.get_queryset()) == list(topic.items.all())


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.ProfileItemListView()
    expected = serializers.ProfileItemSerializer

    assert view.get_serializer_class() == expected


def test_get_serializer_context(profile_topic_factory):
    """
    If the 'pk' kwarg is provided, the view should use it to lookup the
    correct Know Me user to pass to the serializer as context.
    """
    topic = profile_topic_factory()
    km_user = topic.profile.km_user

    view = views.ProfileItemListView()
    view.format_kwarg = None
    view.kwargs = {'pk': topic.pk}
    view.request = None

    context = view.get_serializer_context()

    assert context['km_user'] == km_user


def test_get_serializer_context_no_kwarg():
    """
    If no 'pk' kwarg is given to the view, the serializer context should
    have 'km_user' as None.

    This is mostly to prevent an error when the docs are constructed
    since the view's kwargs will be empty.
    """
    view = views.ProfileItemListView()
    view.format_kwarg = None
    view.kwargs = {}
    view.request = None

    context = view.get_serializer_context()

    assert context['km_user'] is None


def test_perform_create(profile_topic_factory):
    """
    Creating a new profile item with the view should associate the item
    with the topic whose ID is given in the URL.
    """
    topic = profile_topic_factory()

    view = views.ProfileItemListView()
    view.kwargs = {'pk': topic.pk}

    serializer = mock.Mock(name='Mock ProfileItemSerializer')

    result = view.perform_create(serializer)

    assert result == serializer.save.return_value
    assert serializer.save.call_count == 1
    assert serializer.save.call_args[1] == {'topic': topic}
