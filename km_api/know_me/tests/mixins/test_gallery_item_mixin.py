from django.http import Http404

import pytest

from know_me import mixins


def test_get_items(api_rf, gallery_item_factory, profile_factory):
    """
    Only gallery items belonging to the specified profile should be
    returned.
    """
    profile = profile_factory()
    gallery_item_factory(profile=profile)
    gallery_item_factory(profile=profile)

    gallery_item_factory()

    api_rf.user = profile.user

    view = mixins.GalleryItemMixin()
    view.kwargs = {'profile_pk': profile.pk}
    view.request = api_rf.get('/')

    assert list(view.get_queryset()) == list(profile.gallery_items.all())


def test_get_non_existent_profile(api_rf, user_factory):
    """
    If there is no profile with the given primary key, the view should
    raise an ``Http404`` exception.
    """
    api_rf.user = user_factory()

    view = mixins.GalleryItemMixin()
    view.kwargs = {'profile_pk': 1}
    view.request = api_rf.get('/')

    with pytest.raises(Http404):
        view.get_queryset()


def test_get_other_user_profile(api_rf, profile_factory, user_factory):
    """
    Users should not be able to access another user's gallery.
    """
    profile = profile_factory()
    api_rf.user = user_factory()

    view = mixins.GalleryItemMixin()
    view.kwargs = {'profile_pk': profile.pk}
    view.request = api_rf.get('/')

    with pytest.raises(Http404):
        view.get_queryset()
