from unittest import mock

from rest_framework.reverse import reverse

from know_me.profile import models


def test_create(profile_factory):
    """
    Test creating a profile topic.
    """
    models.ProfileTopic.objects.create(
        is_detailed=True,
        name='Test Topic',
        profile=profile_factory())


def test_get_absolute_url(profile_topic_factory):
    """
    The method should return the absolute URL of the instance's detail
    view.
    """
    topic = profile_topic_factory()
    expected = reverse(
        'know-me:profile:profile-topic-detail',
        kwargs={'pk': topic.pk})

    assert topic.get_absolute_url() == expected


def test_get_item_list_url(profile_topic_factory):
    """
    The method should return the absolute URL of the instance's item
    list view.
    """
    topic = profile_topic_factory()
    expected = reverse(
        'know-me:profile:profile-item-list',
        kwargs={'pk': topic.pk})

    assert topic.get_item_list_url() == expected


@mock.patch('know_me.profile.models.Profile.has_object_read_permission')
def test_has_object_read_permission(
        mock_parent_permission,
        api_rf,
        profile_topic_factory):
    """
    Profile topics should delegate the read permission check to their
    parent profile.
    """
    topic = profile_topic_factory()
    request = api_rf.get('/')

    expected = mock_parent_permission.return_value

    assert topic.has_object_read_permission(request) == expected
    assert mock_parent_permission.call_count == 1
    assert mock_parent_permission.call_args[0] == (request,)


@mock.patch('know_me.profile.models.Profile.has_object_write_permission')
def test_has_object_write_permission(
        mock_parent_permission,
        api_rf,
        profile_topic_factory):
    """
    Profile topics should delegate the write permission check to their
    parent profile.
    """
    topic = profile_topic_factory()
    request = api_rf.get('/')

    expected = mock_parent_permission.return_value

    assert topic.has_object_write_permission(request) == expected
    assert mock_parent_permission.call_count == 1
    assert mock_parent_permission.call_args[0] == (request,)


def test_string_conversion(profile_topic_factory):
    """
    Converting a profile topic to a string should return the topic's
    name.
    """
    topic = profile_topic_factory()

    assert str(topic) == topic.name
