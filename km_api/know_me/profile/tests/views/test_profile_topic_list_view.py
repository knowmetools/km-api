from unittest import mock

from know_me.profile import serializers, views


@mock.patch('know_me.profile.views.DRYPermissions.has_permission')
@mock.patch('know_me.profile.views.permissions.HasProfileTopicListPermissions.has_permission')  # noqa
def test_check_permissions(mock_list_permissions, mock_dry_permissions):
    """
    The view should use the appropriate permissions checks.
    """
    view = views.ProfileTopicListView()

    view.check_permissions(None)

    assert mock_dry_permissions.call_count == 1
    assert mock_list_permissions.call_count == 1


def test_get_queryset(profile_factory, profile_topic_factory):
    """
    The view should operate on the topics that belong to the profile
    specified in the URL.
    """
    profile = profile_factory()
    profile_topic_factory(profile=profile)
    profile_topic_factory()

    view = views.ProfileTopicListView()
    view.kwargs = {'pk': profile.pk}

    assert list(view.get_queryset()) == list(profile.topics.all())


def test_get_serializer_class():
    """
    Test the serializer class used by the view.
    """
    view = views.ProfileTopicListView()
    expected = serializers.ProfileTopicSerializer

    assert view.get_serializer_class() == expected


def test_perform_create(profile_factory):
    """
    Creating a topic should associate it with the profile referenced by
    the URL.
    """
    profile = profile_factory()

    view = views.ProfileTopicListView()
    view.kwargs = {'pk': profile.pk}

    serializer = mock.Mock(name='Mock ProfileTopicSerializer')

    result = view.perform_create(serializer)

    assert result == serializer.save.return_value
    assert serializer.save.call_count == 1
    assert serializer.save.call_args[1] == {'profile': profile}
