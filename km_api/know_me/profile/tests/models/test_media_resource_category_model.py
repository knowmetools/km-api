from unittest import mock

from know_me.profile import models


def test_create(km_user_factory):
    """
    Test creating a media resource.
    """
    models.MediaResourceCategory.objects.create(
        km_user=km_user_factory(), name="Test Category"
    )


@mock.patch(
    "know_me.models.KMUser.has_object_read_permission",
    autospec=True,
    return_value=True,
)
def test_has_object_read_permission(
    mock_parent_permission, api_rf, media_resource_category_factory
):
    """
    The permissions on a media resource category should be dictated by
    the permissions on the Know Me user who owns the category.
    """
    category = media_resource_category_factory()
    request = api_rf.get("/")

    mock_func = category.km_user.has_object_read_permission
    expected = mock_func.return_value

    assert category.has_object_read_permission(request) == expected

    assert mock_func.call_count == 1
    assert mock_func.call_args[0][1] == request


@mock.patch(
    "know_me.models.KMUser.has_object_write_permission",
    autospec=True,
    return_value=True,
)
def test_has_object_write_permission(
    mock_parent_permission, api_rf, media_resource_category_factory
):
    """
    The permissions on a media resource category should be dictated by
    the permissions on the Know Me user who owns the category.
    """
    category = media_resource_category_factory()
    request = api_rf.get("/")

    mock_func = category.km_user.has_object_write_permission
    expected = mock_func.return_value

    assert category.has_object_write_permission(request) == expected

    assert mock_func.call_count == 1
    assert mock_func.call_args[0][1] == request


def test_string_conversion(media_resource_category_factory):
    """
    Converting a media resource category to a string should return the
    category's name.
    """
    category = media_resource_category_factory()

    assert str(category) == category.name
