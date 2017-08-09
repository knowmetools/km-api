from know_me import models


def test_create(km_user_accessor_factory, profile_factory):
    """
    Test creating a ProfileAccessor.
    """
    models.ProfileAccessor.objects.create(
        km_user_accessor=km_user_accessor_factory(),
        profile=profile_factory(),
        can_write=False)


def test_string_conversion(profile_accessor_factory):
    """
    Converting a profile accessor to a string should return the profile
    accessor factory's name.
    """
    accessor = profile_accessor_factory()

    expected = 'Profile accessor for {user}'.format(user=accessor.profile.name)
    assert str(accessor) == expected
