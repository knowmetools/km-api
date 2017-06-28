from rest_framework.reverse import reverse

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


def test_get_absolute_url(profile_factory):
    """
    This method should return the URL of the profile's detail view.
    """
    profile = profile_factory()
    expected = reverse(
        'know-me:profile-detail',
        kwargs={'profile_pk': profile.pk})

    assert profile.get_absolute_url() == expected


def test_string_conversion(profile_factory):
    """
    Converting a profile to a string should return the profile's name.
    """
    profile = profile_factory()

    assert str(profile) == profile.name
