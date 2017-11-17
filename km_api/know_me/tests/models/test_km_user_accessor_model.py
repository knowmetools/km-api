from rest_framework.reverse import reverse

from know_me import models


def test_create(km_user_factory, user_factory):
    """
    Test creating a KMUserAccessor.
    """
    user = user_factory()

    models.KMUserAccessor.objects.create(
        accepted=False,
        can_write=False,
        email=user.email,
        has_private_profile_access=False,
        km_user=km_user_factory(),
        user_with_access=user)


def test_get_absolute_url(km_user_accessor_factory):
    """
    This method should return the URL of the accessor's detail view.
    """
    accessor = km_user_accessor_factory()
    expected = reverse('know-me:accessor-detail', kwargs={'pk': accessor.pk})

    assert accessor.get_absolute_url() == expected


def test_get_absolute_url_with_request(api_rf, km_user_accessor_factory):
    """
    If a request is provided, the result should be a full URI.
    """
    accessor = km_user_accessor_factory()
    absolute = reverse('know-me:accessor-detail', kwargs={'pk': accessor.pk})
    request = api_rf.get(absolute)
    expected = request.build_absolute_uri()

    assert accessor.get_absolute_url(request) == expected


def test_string_conversion(km_user_accessor_factory):
    """
    Converting a km user accessor to a string should return the kmuser accessor
    factory's name.
    """
    accessor = km_user_accessor_factory()

    expected = 'Accessor for {user}'.format(user=accessor.km_user.name)
    assert str(accessor) == expected
