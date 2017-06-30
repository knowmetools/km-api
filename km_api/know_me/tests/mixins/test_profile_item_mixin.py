from django.http import Http404

import pytest

from know_me import mixins


def test_get_items(api_rf, profile_row_factory, profile_item_factory):
    """
    Only the items from the row with the given primary key should be
    returned.
    """
    row = profile_row_factory()
    profile_item_factory(row=row)
    profile_item_factory(row=row)

    profile_item_factory()

    group = row.group
    profile = group.profile

    api_rf.user = profile.user

    view = mixins.ProfileItemMixin()
    view.kwargs = {
        'group_pk': group.pk,
        'profile_pk': profile.pk,
        'row_pk': row.pk,
    }
    view.request = api_rf.get('/')

    assert list(view.get_queryset()) == list(row.items.all())


def test_get_non_existent_group(api_rf, profile_row_factory):
    """
    If there is no profile group with the given primary key, the view
    should raise an ``Http404`` exception.
    """
    row = profile_row_factory()
    group = row.group
    profile = group.profile

    api_rf.user = profile.user

    view = mixins.ProfileItemMixin()
    view.kwargs = {
        'group_pk': group.pk + 1,
        'profile_pk': profile.pk,
        'row_pk': row.pk,
    }
    view.request = api_rf.get('/')

    with pytest.raises(Http404):
        view.get_queryset()


def test_get_non_existent_profile(api_rf, profile_row_factory):
    """
    If there is no profile with the given primary key, the view should
    raise an ``Http404`` exception.
    """
    row = profile_row_factory()
    group = row.group
    profile = group.profile

    api_rf.user = profile.user

    view = mixins.ProfileItemMixin()
    view.kwargs = {
        'group_pk': group.pk,
        'profile_pk': profile.pk + 1,
        'row_pk': row.pk,
    }
    view.request = api_rf.get('/')

    with pytest.raises(Http404):
        view.get_queryset()


def test_get_non_existent_row(api_rf, profile_row_factory):
    """
    If there is no profile row with the given primary key, the view
    should raise an ``Http404`` exception.
    """
    row = profile_row_factory()
    group = row.group
    profile = group.profile

    api_rf.user = profile.user

    view = mixins.ProfileItemMixin()
    view.kwargs = {
        'group_pk': group.pk,
        'profile_pk': profile.pk,
        'row_pk': row.pk + 1,
    }
    view.request = api_rf.get('/')

    with pytest.raises(Http404):
        view.get_queryset()


def test_get_other_user_profile(api_rf, profile_row_factory, user_factory):
    """
    Users should not be able to access the items of another user's
    profile.
    """
    row = profile_row_factory()
    group = row.group
    profile = group.profile

    api_rf.user = user_factory()

    view = mixins.ProfileItemMixin()
    view.kwargs = {
        'group_pk': group.pk,
        'profile_pk': profile.pk,
        'row_pk': row.pk,
    }
    view.request = api_rf.get('/')

    with pytest.raises(Http404):
        view.get_queryset()
