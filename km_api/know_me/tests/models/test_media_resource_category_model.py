from django.utils.text import slugify

from know_me import models


def test_create(db):
    """
    Creating a media resource category should slugify its name and use
    it as the category's slug.
    """
    name = 'The quick brown fox jumped over the lazy dog. ' * 2
    expected_slug = slugify(name)[:50]

    category = models.MediaResourceCategory.objects.create(name=name)

    assert category.slug == expected_slug


def test_string_conversion(media_resource_category_factory):
    """
    Converting a media resource category to a string should return the
    category's name.
    """
    category = media_resource_category_factory()

    assert str(category) == category.name
