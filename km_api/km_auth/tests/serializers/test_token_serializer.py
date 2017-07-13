from km_auth import serializers


def test_validate_unverified_email(email_factory, user_factory):
    """
    If the requesting user has an unverified email, the token serializer
    should not be valid.
    """
    user = user_factory(password='password')
    email = email_factory(user=user)

    data = {
        'email': email.email,
        'password': 'password',
    }

    serializer = serializers.TokenSerializer(data=data)

    assert not serializer.is_valid()


def test_validate_verified_email(email_factory, user_factory):
    """
    A user with a verified email should be able to obtain a token from
    the serializer.
    """
    user = user_factory(password='password')
    email = email_factory(user=user, verified=True)

    data = {
        'email': email.email,
        'password': 'password',
    }

    serializer = serializers.TokenSerializer(data=data)

    assert serializer.is_valid()
