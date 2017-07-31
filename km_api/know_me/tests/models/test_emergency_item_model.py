from know_me import models


def test_create(media_resource_factory, km_user_factory):
    """
    Test creating an emergency item.
    """
    models.EmergencyItem.objects.create(
            description='This is a description.',
            media_resource=media_resource_factory(),
            km_user=km_user_factory(),
            name='Emergency Item')


def test_string_conversion(emergency_item_factory):
    """
    Converting an emergency item to a string should return the
    emergency item's name.
    """
    item = emergency_item_factory()

    assert str(item) == item.name
