from know_me import models


def test_create(db):
    """
    Test creating a new config instance.
    """
    models.Config.objects.create(minimum_app_version_ios='1.2.3')


def test_has_read_permission(db):
    """
    All users should be able to read the config object.
    """
    assert models.Config.has_read_permission(None)


def test_has_write_permission(api_rf, user_factory):
    """
    Staff users should have write access to the config object.
    """
    user = user_factory(is_staff=True)
    api_rf.user = user
    request = api_rf.get('/')

    assert models.Config.has_write_permission(request)


def test_has_write_permission_anonymous(api_rf):
    """
    Anonymous users should not have write access to the config object.
    """
    request = api_rf.get('/')

    assert not models.Config.has_write_permission(request)


def test_has_write_permission_non_staff(api_rf, user_factory):
    """
    Non-staff users should not have write permissions on the config
    object.
    """
    user = user_factory()
    api_rf.user = user
    request = api_rf.get('/')

    assert not models.Config.has_write_permission(request)


def test_string_conversion(db):
    """
    Converting the config instance to a string should just return the
    string 'Config'.
    """
    assert str(models.Config.get_solo()) == 'Config'
