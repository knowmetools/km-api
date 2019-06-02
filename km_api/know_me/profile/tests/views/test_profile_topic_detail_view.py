from unittest import mock

from dry_rest_permissions.generics import DRYPermissions

import test_utils
from know_me.permissions import ObjectOwnerHasPremium
from know_me.profile import models, serializers, views


def test_get_permissions():
    """
    Test the permissions used by the view.
    """
    view = views.ProfileTopicDetailView()

    assert test_utils.uses_permission_class(view, DRYPermissions)
    assert test_utils.uses_permission_class(view, ObjectOwnerHasPremium)


def test_get_queryset(profile_topic_factory):
    """
    The view should operate on all profile topics.
    """
    profile_topic_factory()
    profile_topic_factory()
    profile_topic_factory()

    view = views.ProfileTopicDetailView()

    assert list(view.get_queryset()) == list(models.ProfileTopic.objects.all())


def test_get_serializer_class():
    """
    Test the serializer class the view uses.
    """
    view = views.ProfileTopicDetailView()
    expected = serializers.ProfileTopicListSerializer

    assert view.get_serializer_class() == expected


def test_get_subscription_owner():
    """
    The subscription owner for a profile topic should be the owner of
    the whole profile.
    """
    view = views.ProfileTopicDetailView()
    request = mock.Mock()
    topic = mock.Mock()

    expected = topic.profile.km_user.user

    assert view.get_subscription_owner(request, topic) == expected
