from rest_email_auth.signals import user_registered


def test_register_user(image, user_factory):
    """
    When a user is registered, a Know Me user should be created for them
    automatically.
    """
    user = user_factory(image=image)
    user_registered.send(sender=None, user=user)

    assert user.km_user is not None
    assert user.km_user.image == user.image
