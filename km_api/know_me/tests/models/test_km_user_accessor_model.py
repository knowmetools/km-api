from unittest import mock

from django.conf import settings

from rest_framework.reverse import reverse

from know_me import models


def test_accept_url(km_user_accessor_factory):
    """
    This property should contain the absolute URL of the accessor's
    accept view.
    """
    accessor = km_user_accessor_factory()
    expected = reverse("know-me:accessor-accept", kwargs={"pk": accessor.pk})

    assert accessor.accept_url == expected


def test_create(km_user_factory, user_factory):
    """
    Test creating a KMUserAccessor.
    """
    user = user_factory()

    models.KMUserAccessor.objects.create(
        email=user.primary_email.email,
        is_accepted=False,
        is_admin=False,
        km_user=km_user_factory(),
        user_with_access=user,
    )


def test_get_absolute_url(km_user_accessor_factory):
    """
    This method should return the URL of the accessor's detail view.
    """
    accessor = km_user_accessor_factory()
    expected = reverse("know-me:accessor-detail", kwargs={"pk": accessor.pk})

    assert accessor.get_absolute_url() == expected


def test_get_absolute_url_with_request(api_rf, km_user_accessor_factory):
    """
    If a request is provided, the result should be a full URI.
    """
    accessor = km_user_accessor_factory()
    absolute = reverse("know-me:accessor-detail", kwargs={"pk": accessor.pk})
    request = api_rf.get(absolute)
    expected = request.build_absolute_uri()

    assert accessor.get_absolute_url(request) == expected


def test_has_object_accept_permission_accessee(
    api_rf, km_user_accessor_factory, user_factory
):
    """
    The user granted access through the accessor should have permission
    to accept the accessor.
    """
    user = user_factory()
    accessor = km_user_accessor_factory(user_with_access=user)

    api_rf.user = user
    request = api_rf.get(accessor.get_absolute_url())

    assert accessor.has_object_accept_permission(request)


def test_has_object_accept_permission_owner(api_rf, km_user_accessor_factory):
    """
    The user who created the accessor should not be able to mark the
    accessor as accepted.
    """
    accessor = km_user_accessor_factory()
    api_rf.user = accessor.km_user.user
    request = api_rf.get(accessor.get_absolute_url())

    assert not accessor.has_object_accept_permission(request)


def test_has_object_destroy_permission_accessee(
    api_rf, km_user_accessor_factory, user_factory
):
    """
    The user granted access by the accessor should be able to delete the
    accessor.
    """
    user = user_factory()
    accessor = km_user_accessor_factory(user_with_access=user)

    api_rf.user = user
    request = api_rf.get("/")

    assert accessor.has_object_destroy_permission(request)


def test_has_object_destroy_permission_other(
    api_rf, km_user_accessor_factory, user_factory
):
    """
    Other users should not be able to destroy a random accessor.
    """
    user = user_factory()
    accessor = km_user_accessor_factory()

    api_rf.user = user
    request = api_rf.get("/")

    assert not accessor.has_object_destroy_permission(request)


def test_has_object_destroy_permission_owner(api_rf, km_user_accessor_factory):
    """
    The Know Me user the accessor grants access on should be able to
    destroy the accessor.
    """
    accessor = km_user_accessor_factory()
    api_rf.user = accessor.km_user.user
    request = api_rf.get("/")

    assert accessor.has_object_destroy_permission(request)


def test_has_object_read_permission_accessee(
    api_rf, km_user_accessor_factory, user_factory
):
    """
    The user granted access through the accessor should have read
    permissions on the accessor.
    """
    user = user_factory()
    accessor = km_user_accessor_factory(user_with_access=user)

    api_rf.user = user
    request = api_rf.get(accessor.get_absolute_url())

    assert accessor.has_object_read_permission(request)


def test_has_object_read_permission_other(
    api_rf, km_user_accessor_factory, user_factory
):
    """
    Other users should not have read access to accessors.
    """
    user = user_factory()
    accessor = km_user_accessor_factory()

    api_rf.user = user
    request = api_rf.get(accessor.get_absolute_url())

    assert not accessor.has_object_read_permission(request)


def test_has_object_read_permission_owner(api_rf, km_user_accessor_factory):
    """
    The user who created the accessor should have read permissions on
    it.
    """
    accessor = km_user_accessor_factory()
    api_rf.user = accessor.km_user.user
    request = api_rf.get(accessor.get_absolute_url())

    assert accessor.has_object_read_permission(request)


def test_has_object_write_permission_accessee(
    api_rf, km_user_accessor_factory, user_factory
):
    """
    The user granted access through the accessor should not have write
    permissions on the accessor.
    """
    user = user_factory()
    accessor = km_user_accessor_factory(user_with_access=user)

    api_rf.user = user
    request = api_rf.get(accessor.get_absolute_url())

    assert not accessor.has_object_write_permission(request)


def test_has_object_write_permission_other(
    api_rf, km_user_accessor_factory, user_factory
):
    """
    Other users should not have write access to accessors.
    """
    user = user_factory()
    accessor = km_user_accessor_factory()

    api_rf.user = user
    request = api_rf.get(accessor.get_absolute_url())

    assert not accessor.has_object_write_permission(request)


def test_has_object_write_permission_owner(api_rf, km_user_accessor_factory):
    """
    The user who created the accessor should have write permissions on
    it.
    """
    accessor = km_user_accessor_factory()
    api_rf.user = accessor.km_user.user
    request = api_rf.get(accessor.get_absolute_url())

    assert accessor.has_object_write_permission(request)


@mock.patch("know_me.models.email_utils.send_email")
def test_send_invite(mock_send_email, km_user_accessor_factory):
    """
    Sending the invitation should send an email to the person granted
    access through the accessor.
    """
    accessor = km_user_accessor_factory()
    accessor.send_invite()

    context = {"name": accessor.km_user.name}

    assert mock_send_email.call_count == 1
    assert mock_send_email.call_args[1] == {
        "context": context,
        "from_email": settings.DEFAULT_FROM_EMAIL,
        "recipient_list": [accessor.email],
        "subject": "You Have Been Invited to Follow Someone on Know Me",
        "template_name": "know_me/emails/invite",
    }


def test_string_conversion(km_user_accessor_factory):
    """
    Converting a km user accessor to a string should return the kmuser accessor
    factory's name.
    """
    accessor = km_user_accessor_factory()

    expected = "Accessor for {user}".format(user=accessor.km_user.name)
    assert str(accessor) == expected
