from know_me import models


def test_create_image_content(
        image,
        media_resource_factory,
        profile_item_factory):
    """
    Test creating image content for a profile item.
    """
    image_gallery_item = media_resource_factory(file=image)

    models.ImageContent.objects.create(
        description='Test item description.',
        image_resource=image_gallery_item,
        media_resource=media_resource_factory(),
        profile_item=profile_item_factory())


def test_string_conversion(image_content_factory):
    """
    Converting image content to a string should return a message
    indicating which profile item the content belongs to.
    """
    content = image_content_factory()
    expected = "Image content for profile item '{item}'".format(
        item=content.profile_item)

    assert str(content) == expected
