from know_me import models


def test_create_list_content(profile_item_factory):
    """
    Test creating a list for a profile item.
    """
    models.ListContent.objects.create(
        profile_item=profile_item_factory())


def test_string_conversion(list_content_factory):
    """
    Converting a ``ListContent`` instance to a string should return a
    message indicating which profile item the list is attached to.
    """
    list_ = list_content_factory()
    expected = "List for profile item '{item}'".format(item=list_.profile_item)

    assert str(list_) == expected
