

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
