import pytest


def test_authenticate_inactive_user(
        auth_backend,
        api_rf,
        email_factory,
        user_factory):
    """
    If the user is not active, ``None`` should be returned.
    """
    user = user_factory(is_active=False, password='password')
    email = email_factory(user=user)

    request = api_rf.get('/')

    assert auth_backend.authenticate(request, email.email, 'password') is None


def test_authenticate_invalid_password(
        auth_backend,
        api_rf,
        email_factory,
        user_factory):
    """
    If the wrong password is provided, the backend should return
    ``None``.
    """
    user = user_factory(password='password')
    email = email_factory(user=user, verified=True)

    request = api_rf.get('/')

    assert auth_backend.authenticate(
        request,
        email.email,
        'notpassword') is None


def test_authenticate_missing_email(auth_backend, api_rf, user_factory):
    """
    If the provided email address doesn't exist, ``None`` should be
    returned.
    """
    user_factory(password='password')

    request = api_rf.get('/')

    assert auth_backend.authenticate(
        request,
        'fake@test.com',
        'password') is None


def test_authenticate_username(
        auth_backend,
        api_rf,
        email_factory,
        user_factory):
    """
    If a username is given instead of an email, it should be used as the
    email to authenticate the user.
    """
    user = user_factory(password='password')
    email = email_factory(user=user, verified=True)

    request = api_rf.get('/')

    assert auth_backend.authenticate(
        request,
        password='password',
        username=email.email) == user


def test_authenticate_valid_credentials(
        auth_backend,
        api_rf,
        email_factory,
        user_factory):
    """
    Providing a verified email address and a valid password should
    successfully authenticate the user.
    """
    user = user_factory(password='password')
    email = email_factory(user=user, verified=True)

    request = api_rf.get('/')

    assert auth_backend.authenticate(request, email.email, 'password') == user


def test_get_user(auth_backend, user_factory):
    """
    The get user method should return the user with the provided ID.
    """
    user = user_factory()

    assert auth_backend.get_user(user.id) == user


@pytest.mark.django_db
def test_get_user_invalid_id(auth_backend):
    """
    If there is no user with the provided ID, ``None`` should be
    returned.
    """
    assert auth_backend.get_user(1) is None
