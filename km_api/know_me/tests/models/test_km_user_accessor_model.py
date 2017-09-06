from know_me import models


def test_create(km_user_factory, user_factory):
    """
    Test creating a KMUserAccessor.
    """
    user = user_factory()

    models.KMUserAccessor.objects.create(
        accepted=False,
        can_write=False,
        email=user.email,
        has_private_profile_access=False,
        km_user=km_user_factory(),
        user_with_access=user)


def test_string_conversion(km_user_accessor_factory):
    """
    Converting a km user accessor to a string should return the kmuser accessor
    factory's name.
    """
    accessor = km_user_accessor_factory()

    expected = 'Accessor for {user}'.format(user=accessor.km_user.name)
    assert str(accessor) == expected
