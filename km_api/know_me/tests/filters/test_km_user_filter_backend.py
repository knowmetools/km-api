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
