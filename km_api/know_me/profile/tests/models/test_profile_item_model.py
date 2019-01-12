from unittest import mock

from rest_framework.reverse import reverse

from know_me.profile import models


def test_create(image, media_resource_factory, profile_topic_factory):
    """
    Test creating a profile item.
    """
    media_resource = media_resource_factory()
    topic = profile_topic_factory(profile__km_user=media_resource.km_user)

    models.ProfileItem.objects.create(
        description="My test item.",
        image=image,
        media_resource=media_resource,
        name="Test Item",
        topic=topic,
    )


def test_get_absolute_url(profile_item_factory):
    """
    This method should return the absolute URL of the instance's detail
    view.
    """
    item = profile_item_factory()
    expected = reverse(
        "know-me:profile:profile-item-detail", kwargs={"pk": item.pk}
    )

    assert item.get_absolute_url() == expected


def test_get_list_entries_url(profile_item_factory):
    """
    This method should return the absolute URL of the instance's list
    entry list view.
    """
    item = profile_item_factory()
    expected = reverse(
        "know-me:profile:list-entry-list", kwargs={"pk": item.pk}
    )

    assert item.get_list_entries_url() == expected


@mock.patch("know_me.profile.models.ProfileTopic.has_object_read_permission")
def test_has_object_read_permission(
    mock_parent_permission, api_rf, profile_item_factory
):
    """
    Profile items should delegate the read permission check to their
    parent profile topic.
    """
    item = profile_item_factory()
    request = api_rf.get("/")

    expected = mock_parent_permission.return_value

    assert item.has_object_read_permission(request) == expected
    assert mock_parent_permission.call_count == 1
    assert mock_parent_permission.call_args[0] == (request,)


@mock.patch("know_me.profile.models.ProfileTopic.has_object_write_permission")
def test_has_object_write_permission(
    mock_parent_permission, api_rf, profile_item_factory
):
    """
    Profile items should delegate the write permission check to their
    parent profile topic.
    """
    item = profile_item_factory()
    request = api_rf.get("/")

    expected = mock_parent_permission.return_value

    assert item.has_object_write_permission(request) == expected
    assert mock_parent_permission.call_count == 1
    assert mock_parent_permission.call_args[0] == (request,)


def test_string_conversion(profile_item_factory):
    """
    Converting a profile item to a string should return the item's name.
    """
    item = profile_item_factory()

    assert str(item) == item.name
