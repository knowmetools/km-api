from unittest import mock

from dry_rest_permissions.generics import DRYPermissions

import test_utils
from know_me.permissions import CollectionOwnerHasPremium
from know_me.profile import serializers, views
from know_me.profile.permissions import HasProfileTopicListPermissions


def test_get_permissions():
    """
    Test the permisisons used by the view.
    """
    view = views.ProfileTopicListView()

    assert test_utils.uses_permission_class(view, DRYPermissions)
    assert test_utils.uses_permission_class(
        view, HasProfileTopicListPermissions
    )
    assert test_utils.uses_permission_class(view, CollectionOwnerHasPremium)


def test_get_queryset(profile_factory, profile_topic_factory):
    """
    The view should operate on the topics that belong to the profile
    specified in the URL.
    """
    profile = profile_factory()
    profile_topic_factory(profile=profile)
    profile_topic_factory()

    view = views.ProfileTopicListView()
    view.kwargs = {"pk": profile.pk}

    assert list(view.get_queryset()) == list(profile.topics.all())


def test_get_serializer_class_get(api_rf):
    """
    The view should use the list serializer for a GET request.
    """
    view = views.ProfileTopicListView()
    view.request = api_rf.get("/")

    expected = serializers.ProfileTopicListSerializer

    assert view.get_serializer_class() == expected


def test_get_serializer_class_missing_request():
    """
    If the view's request instance is ``None``, the detail serializer
    should be used.
    """
    view = views.ProfileTopicListView()
    view.request = None

    expected = serializers.ProfileTopicDetailSerializer

    assert view.get_serializer_class() == expected


def test_get_serializer_class_post(api_rf):
    """
    The view should use the detail serializer for a POST request.
    """
    view = views.ProfileTopicListView()
    view.request = api_rf.post("/")

    expected = serializers.ProfileTopicDetailSerializer

    assert view.get_serializer_class() == expected


def test_get_subscription_owner(profile_factory):
    """
    The subscription owner for a collection of profile topics should be
    the owner of the profile the topics belong to.
    """
    profile = profile_factory()
    view = views.ProfileTopicListView()
    view.kwargs = {"pk": profile.pk}
    request = mock.Mock()

    expected = profile.km_user.user

    assert view.get_subscription_owner(request) == expected


def test_perform_create(profile_factory):
    """
    Creating a topic should associate it with the profile referenced by
    the URL.
    """
    profile = profile_factory()

    view = views.ProfileTopicListView()
    view.kwargs = {"pk": profile.pk}

    serializer = mock.Mock(name="Mock ProfileTopicSerializer")

    result = view.perform_create(serializer)

    assert result == serializer.save.return_value
    assert serializer.save.call_count == 1
    assert serializer.save.call_args[1] == {"profile": profile}
