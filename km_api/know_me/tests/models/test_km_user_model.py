from know_me import models


def test_create(user_factory):
    """
    Test creating a KMUser.
    """
    models.KMUser.objects.create(
       image=None,
       quote='kuh mooz er',
       user=user_factory())
