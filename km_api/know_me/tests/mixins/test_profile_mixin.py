from know_me import mixins


def test_get_inaccessible_profile(api_rf, profile_factory, user_factory):
    """
    Users should not be able to access profiles they don't own.
    """
    profile_factory()

    api_rf.user = user_factory()

    view = mixins.ProfileMixin()
    view.request = api_rf.get('/')

    assert not view.get_queryset().exists()


def test_get_own_profile(api_rf, profile_factory):
    """
    Users should be able to access their own profile.
    """
    profile = profile_factory()
    api_rf.user = profile.user

    view = mixins.ProfileMixin()
    view.request = api_rf.get('/')

    assert list(view.get_queryset()) == [profile]
