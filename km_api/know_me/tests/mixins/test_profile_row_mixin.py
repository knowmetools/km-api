from django.http import Http404

import pytest

from know_me import mixins


def test_get_inaccessible_profile(api_rf, profile_group_factory, user_factory):
    """
    Attempting to access profile groups from another user's profile
    should raise an ``Http404`` exception.
    """
    group = profile_group_factory()
    profile = group.profile

    api_rf.user = user_factory()

    view = mixins.ProfileRowMixin()
    view.kwargs = {
        'group_pk': group.pk,
        'profile_pk': profile.pk,
    }
    view.request = api_rf.get('/')

    with pytest.raises(Http404):
        view.get_queryset()


def test_get_non_existent_group(api_rf, profile_factory, user_factory):
    """
    If there is no profile group with the given primary key, the
    ``get_queryset`` method should raise an ``Http404`` exception.
    """
    profile = profile_factory()

    api_rf.user = profile.user

    view = mixins.ProfileRowMixin()
    view.kwargs = {
        'group_pk': 1,
        'profile_pk': profile.pk,
    }
    view.request = api_rf.get('/')

    with pytest.raises(Http404):
        view.get_queryset()


def test_get_non_existent_profile(api_rf, profile_group_factory, user_factory):
    """
    If there is no profile with the given primary key, the
    ``get_queryset`` method should raise an ``Http404`` exception.
    """
    group = profile_group_factory()

    api_rf.user = user_factory()

    view = mixins.ProfileRowMixin()
    view.kwargs = {
        'group_pk': group.pk,
        'profile_pk': group.profile.pk + 1,
    }
    view.request = api_rf.get('/')

    with pytest.raises(Http404):
        view.get_queryset()


def test_get_other_group_rows(
        api_rf,
        profile_group_factory,
        profile_row_factory):
    """
    Only the rows of the profile group with the given primary key should
    be returned.
    """
    group = profile_group_factory()
    profile = group.profile

    profile_row_factory(group=group)
    profile_row_factory(group=group)

    profile_row_factory()

    api_rf.user = profile.user

    view = mixins.ProfileRowMixin()
    view.kwargs = {
        'group_pk': group.pk,
        'profile_pk': profile.pk,
    }
    view.request = api_rf.get('/')

    assert list(view.get_queryset()) == list(group.rows.all())


def test_get_own_row(api_rf, profile_row_factory):
    """
    Users should be able to access rows in their own profile.
    """
    row = profile_row_factory()
    group = row.group
    profile = group.profile

    api_rf.user = profile.user

    view = mixins.ProfileRowMixin()
    view.kwargs = {
        'group_pk': group.pk,
        'profile_pk': profile.pk,
    }
    view.request = api_rf.get('/')

    assert list(view.get_queryset()) == [row]
