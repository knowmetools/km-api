from know_me import models


def test_create(user_factory):
    """
    Test creating a KMUser.
    """
    models.KMUser.objects.create(
       image=None,
       quote='kuh mooz er',
       user=user_factory())


def test_name(km_user_factory):
    """
    The know me user's name property should return the associated user's
    short name.
    """
    km_user = km_user_factory()

    assert km_user.name == km_user.user.get_short_name()


def test_string_conversion(km_user_factory):
    """
    Converting a know me user to a string should return the user's name
    property.
    """
    km_user = km_user_factory()

    assert str(km_user) == km_user.name
