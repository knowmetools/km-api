from rest_framework.reverse import reverse

from know_me import models


def test_create(profile_factory):
    """
    Test creating a profile topic.
    """
    models.ProfileTopic.objects.create(
        profile=profile_factory(),
        name='Test profile topic',
        topic_type=models.ProfileTopic.TEXT)


def test_get_absolute_url(profile_topic_factory):
    """
    This method should return the URL of the topic's detail view.
    """
    topic = profile_topic_factory()
    expected = reverse('know-me:profile-topic-detail', kwargs={'pk': topic.pk})

    assert topic.get_absolute_url() == expected


def test_get_item_list_url(profile_topic_factory):
    """
    This method should return the URL of the topic's item list view.
    """
    topic = profile_topic_factory()
    expected = reverse('know-me:profile-item-list', kwargs={'pk': topic.pk})

    assert topic.get_item_list_url() == expected


def test_has_object_read_permission_other(
        api_rf,
        profile_topic_factory,
        user_factory):
    """
    Users should not have read permissions on profile topics that belong
    to a km_user they don't have access to.
    """
    topic = profile_topic_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not topic.has_object_read_permission(request)


def test_has_object_read_permission_owner(api_rf, profile_topic_factory):
    """
    Users should have read permissions on profile topics that belong to
    their own km_user.
    """
    topic = profile_topic_factory()
    profile = topic.profile
    km_user = profile.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    assert topic.has_object_read_permission(request)


def test_has_object_write_permission_other(
        api_rf,
        profile_topic_factory,
        user_factory):
    """
    Users should not have write permissions on profile topics that
    belong to a km_user they don't have access to.
    """
    topic = profile_topic_factory()

    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert not topic.has_object_write_permission(request)


def test_has_object_write_permission_owner(api_rf, profile_topic_factory):
    """
    Users should have write permissions on profile topics that belong
    to their own km_user.
    """
    topic = profile_topic_factory()
    profile = topic.profile
    km_user = profile.km_user

    api_rf.user = km_user.user
    request = api_rf.get('/')

    assert topic.has_object_write_permission(request)


def test_string_conversion(profile_topic_factory):
    """
    Converting a profile topic to a string should return the topic's
    name.
    """
    topic = profile_topic_factory()

    assert str(topic) == topic.name
