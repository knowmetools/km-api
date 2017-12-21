from know_me import models


def test_create(km_user_factory):
    """
    Test creating a media resource.
    """
    models.MediaResourceCategory.objects.create(
        km_user=km_user_factory(),
        name='Test Category')


def test_string_conversion(media_resource_category_factory):
    """
    Converting a media resource category to a string should return the
    category's name.
    """
    category = media_resource_category_factory()

    assert str(category) == category.name
