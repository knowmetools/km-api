from know_me import filters, models


def test_filter_list_owner(api_rf, km_user_factory):
    """
    The filter should exclude km_users not owned by the requesting user.
    """
    km_user = km_user_factory()
    km_user_factory()

    api_rf.user = km_user.user
    request = api_rf.get('/')

    backend = filters.KMUserFilterBackend()
    filtered = backend.filter_list_queryset(
        request,
        models.KMUser.objects.all(),
        None)

    expected = models.KMUser.objects.filter(user=km_user.user)

    assert list(filtered) == list(expected)


def test_filter_list_shared(
        api_rf,
        km_user_accessor_factory,
        km_user_factory,
        user_factory):
    """
    If there is a ``KMUserAccessor`` that gives the requesting user
    access to a ``KMUser``, that Know Me user should be included in the
    results.
    """
    km_user = km_user_factory()
    user = user_factory()

    km_user_accessor_factory(km_user=km_user, user_with_access=user)

    api_rf.user = user
    request = api_rf.get('/')

    backend = filters.KMUserFilterBackend()
    filtered = backend.filter_list_queryset(
        request,
        models.KMUser.objects.all(),
        None)

    expected = models.KMUser.objects.filter(
        km_user_accessor__user_with_access=user)

    assert list(filtered) == list(expected)
