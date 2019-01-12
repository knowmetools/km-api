from unittest import mock

from know_me.profile import models, serializers, views


@mock.patch("know_me.profile.views.DRYPermissions.has_permission")
def test_check_permissions(mock_dry_permissions):
    """
    The view should use DRYPermissions to check object permissions.
    """
    view = views.ProfileTopicDetailView()

    view.check_permissions(None)

    assert mock_dry_permissions.call_count == 1


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
