from know_me import filters, models


def test_filter_list_owner(api_rf, profile_factory):
    """
    The filter should exclude profiles not owned by the requesting user.
    """
    profile = profile_factory()
    profile_factory()

    api_rf.user = profile.user
    request = api_rf.get('/')

    backend = filters.ProfileFilterBackend()
    filtered = backend.filter_list_queryset(
        request,
        models.Profile.objects.all(),
        None)

    expected = models.Profile.objects.filter(user=profile.user)

    assert list(filtered) == list(expected)
