from account import filters, models


def test_filter_list_owned(api_rf, email_factory, user_factory):
    """
    Email addresses should be filtered to only those owned by the
    requesting user.
    """
    user = user_factory()
    email_factory(user=user)
    email_factory(user=user)

    email_factory()

    api_rf.user = user
    request = api_rf.get('/')

    backend = filters.EmailFilterBackend()
    results = backend.filter_list_queryset(
        request,
        models.EmailAddress.objects.all(),
        None)

    expected = user.email_addresses.all()

    assert list(results) == list(expected)
