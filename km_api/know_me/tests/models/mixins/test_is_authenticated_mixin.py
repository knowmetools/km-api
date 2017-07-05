from know_me.models import mixins


def test_has_read_permission_authenticated(api_rf, user_factory):
    """
    Authenticated users should have read permissions on the class.
    """
    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert mixins.IsAuthenticatedMixin().has_read_permission(request)


def test_has_read_permission_unauthenticated(api_rf):
    """
    Unuthenticated users should not have read permissions on the class.
    """
    request = api_rf.get('/')

    assert not mixins.IsAuthenticatedMixin().has_read_permission(request)


def test_has_write_permission_authenticated(api_rf, user_factory):
    """
    Authenticated users should have write permissions on the class.
    """
    api_rf.user = user_factory()
    request = api_rf.get('/')

    assert mixins.IsAuthenticatedMixin().has_write_permission(request)


def test_has_write_permission_unauthenticated(api_rf):
    """
    Unuthenticated users should not have write permissions on the class.
    """
    request = api_rf.get('/')

    assert not mixins.IsAuthenticatedMixin().has_write_permission(request)
