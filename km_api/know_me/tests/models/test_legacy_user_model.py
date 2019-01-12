from rest_framework.reverse import reverse

from know_me import models


def test_create(db):
    """
    Test creating a legacy user.
    """
    models.LegacyUser.objects.create(email="test@example.com")


def test_get_absolute_url(legacy_user_factory):
    """
    This method should return the absolute URL of the instance's detail
    view.
    """
    user = legacy_user_factory()
    expected = reverse("know-me:legacy-user-detail", kwargs={"pk": user.pk})

    assert user.get_absolute_url() == expected


def test_has_read_permission_staff(api_rf, user_factory):
    """
    Staff users should have read access to legacy users.
    """
    user = user_factory(is_staff=True)
    api_rf.user = user
    request = api_rf.get("/")

    assert models.LegacyUser.has_read_permission(request)


def test_has_read_permission_standard_user(api_rf, user_factory):
    """
    Standard users should not have read access to legacy users.
    """
    user = user_factory()
    api_rf.user = user
    request = api_rf.get("/")

    assert not models.LegacyUser.has_read_permission(request)


def test_has_write_permission_staff(api_rf, user_factory):
    """
    Staff users should have write access to legacy users.
    """
    user = user_factory(is_staff=True)
    api_rf.user = user
    request = api_rf.get("/")

    assert models.LegacyUser.has_write_permission(request)


def test_has_write_permission_standard_user(api_rf, user_factory):
    """
    Standard users should not have write access to legacy users.
    """
    user = user_factory()
    api_rf.user = user
    request = api_rf.get("/")

    assert not models.LegacyUser.has_write_permission(request)


def test_string_conversion(legacy_user_factory):
    """
    Converting a legacy user to a string should return the user's email.
    """
    user = legacy_user_factory()

    assert str(user) == user.email
