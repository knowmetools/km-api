from know_me import models


def test_create(km_user_factory, user_factory):
    """
    Test creating a KMUserAccessor.
    """
    models.KMUserAccessor.objects.create(
        accepted=False,
        can_write_everywhere=False,
        km_user=km_user_factory(),
        user_with_access=user_factory())


def test_string_conversion(km_user_accessor_factory):
    """
    Converting a km user accessor to a string should return the kmuser accessor
    factory's name.
    """
    accessor = km_user_accessor_factory()

    expected = 'Accessor for {user}'.format(user=accessor.km_user.name)
    assert str(accessor) == expected
