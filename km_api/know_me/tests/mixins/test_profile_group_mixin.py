from django.http import Http404

import pytest

from know_me import mixins


def test_get_inaccessible_profile(api_rf, profile_factory, user_factory):
    """
    Attempting to access profile groups from another user's profile
    should raise an ``Http404`` exception.
    """
    profile = profile_factory()

    api_rf.user = user_factory()

    view = mixins.ProfileGroupMixin()
    view.kwargs = {
        'profile_pk': profile.pk,
    }
    view.request = api_rf.get('/')

    with pytest.raises(Http404):
        view.get_queryset()


def test_get_non_existent_profile(api_rf, user_factory):
    """
    If there is no profile with the given primary key, the
    ``get_queryset`` method should raise an ``Http404`` exception.
    """
    api_rf.user = user_factory()

    view = mixins.ProfileGroupMixin()
    view.kwargs = {
        'profile_pk': 1,
    }
    view.request = api_rf.get('/')

    with pytest.raises(Http404):
        view.get_queryset()


def test_get_other_profile_groups(
        api_rf,
        profile_factory,
        profile_group_factory):
    """
    Only the groups of the profile with the given primary key should be
    returned.
    """
    profile = profile_factory()
    profile_group_factory(profile=profile)
    profile_group_factory(profile=profile)

    profile_group_factory()

    api_rf.user = profile.user

    view = mixins.ProfileGroupMixin()
    view.kwargs = {
        'profile_pk': profile.pk,
    }
    view.request = api_rf.get('/')

    assert list(view.get_queryset()) == list(profile.groups.all())


def test_get_own_group(api_rf, profile_group_factory):
    """
    Users should be able to access groups in their own profile.
    """
    group = profile_group_factory()
    profile = group.profile

    api_rf.user = profile.user

    view = mixins.ProfileGroupMixin()
    view.kwargs = {
        'profile_pk': profile.pk,
    }
    view.request = api_rf.get('/')

    assert list(view.get_queryset()) == [group]
