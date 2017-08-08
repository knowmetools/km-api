from know_me import models


def test_create_list_content(profile_item_factory):
    """
    Test creating list content for a profile item.
    """
    models.ListContent.objects.create(profile_item=profile_item_factory())


def test_string_conversion(list_content_factory):
    """
    Converting a list content instance to a string should return a
    message indicating which profile item the list content belongs to.
    """
    content = list_content_factory()
    expected = "List content for profile item '{item}'".format(
        item=content.profile_item)

    assert str(content) == expected
