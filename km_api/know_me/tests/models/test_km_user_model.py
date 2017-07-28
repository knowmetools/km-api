from know_me import models


def test_create(user_factory):
    """
    Test creating a KMUser.
    """
    models.KMUser.objects.create(
       image=None,
       quote='kuh mooz er',
       user=user_factory())


def test_string_conversion(km_user_factory):
    """
    Converting a KMUser to a string should return the associated user's
    short name.
    """
    km_user = km_user_factory()

    assert str(km_user) == km_user.user.get_short_name()
