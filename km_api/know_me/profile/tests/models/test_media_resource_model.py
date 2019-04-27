from unittest import mock

from rest_framework.reverse import reverse

from know_me.profile import models


def test_create(file, km_user_factory):
    """
    Test creating a media resource.
    """
    km_user = km_user_factory()

    models.MediaResource.objects.create(
        file=file,
        km_user=km_user,
        link="https://example.com",
        name="Test Media Resource",
    )


def test_get_absolute_url(media_resource_factory):
    """
    The absolute URL of a media resource should be the URL of its detail
    view.
    """
    resource = media_resource_factory()
    expected = reverse(
        "know-me:profile:media-resource-detail", kwargs={"pk": resource.pk}
    )

    assert resource.get_absolute_url() == expected


@mock.patch(
    "know_me.models.KMUser.has_object_read_permission",
    autospec=True,
    return_value=True,
)
def test_has_object_read_permission(
    mock_parent_permission, api_rf, media_resource_factory
):
    """
    The permissions on a media resource should be dictated by the
    permissions on the Know Me user who owns the resource.
    """
    resource = media_resource_factory()
    request = api_rf.get("/")

    mock_func = resource.km_user.has_object_read_permission
    expected = mock_func.return_value

    assert resource.has_object_read_permission(request) == expected

    assert mock_func.call_count == 1
    assert mock_func.call_args[0][1] == request


@mock.patch(
    "know_me.models.KMUser.has_object_write_permission",
    autospec=True,
    return_value=True,
)
def test_has_object_write_permission(
    mock_parent_permission, api_rf, media_resource_factory
):
    """
    The permissions on a media resource should be dictated by the
    permissions on the Know Me user who owns the resource.
    """
    resource = media_resource_factory()
    request = api_rf.get("/")

    mock_func = resource.km_user.has_object_write_permission
    expected = mock_func.return_value

    assert resource.has_object_write_permission(request) == expected

    assert mock_func.call_count == 1
    assert mock_func.call_args[0][1] == request


def test_string_conversion(media_resource_factory):
    """
    Converting a media resource to a string should return the resource's
    name.
    """
    resource = media_resource_factory()

    assert str(resource) == resource.name
