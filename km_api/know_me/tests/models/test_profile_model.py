from know_me import models


def test_create(user_factory):
    """
    Test creating a profile.
    """
    models.Profile.objects.create(
        name='John',
        quote='Life is like a box of chocolates.',
        user=user_factory(),
        welcome_message="Hi, I'm John")


def test_string_conversion(profile_factory):
    """
    Converting a profile to a string should return the profile's name.
    """
    profile = profile_factory()

    assert str(profile) == profile.name
