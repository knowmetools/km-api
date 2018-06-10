from rest_framework import status
from rest_framework.reverse import reverse

from know_me import serializers, views


km_user_list_view = views.KMUserListView.as_view()
url = reverse('know-me:km-user-list')


def test_get_own_km_user(api_rf, km_user_factory, user_factory):
    """
    If the requesting user has a km_user, then a GET request to this
    view should contain that km_user.
    """
    user = user_factory()
    api_rf.user = user

    km_user = km_user_factory(user=user)

    request = api_rf.get(url)
    response = km_user_list_view(request)

    serializer = serializers.KMUserListSerializer(
        [km_user],
        context={'request': request},
        many=True)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data


def test_get_queryset_duplicates(
        api_rf,
        km_user_accessor_factory,
        km_user_factory,
        user_factory):
    """
    If the user has managed to create an accessor granting access to
    their own account, there should not be a duplicate entry in the user
    list.

    Regression test for #352.
    """
    user = user_factory()
    api_rf.user = user

    km_user = km_user_factory(user=user)
    km_user_accessor_factory(
        is_accepted=True,
        km_user=km_user,
        user_with_access=user,
    )

    # Have to create another accessor for the bug to be present
    km_user_accessor_factory(km_user=km_user)

    view = views.KMUserListView()
    view.request = api_rf.get('/')

    assert list(view.get_queryset()) == [km_user]


def test_get_queryset_order(
        api_rf,
        km_user_accessor_factory,
        km_user_factory,
        user_factory):
    """
    The list of Know Me users should have the requesting user's Know Me
    user listed first, followed by any shared users.
    """
    user = user_factory()
    api_rf.user = user

    k1 = km_user_factory()
    km_user_accessor_factory(
        is_accepted=True,
        km_user=k1,
        user_with_access=user)

    k2 = km_user_factory(user=user)

    k3 = km_user_factory()
    km_user_accessor_factory(
        is_accepted=True,
        km_user=k3,
        user_with_access=user)

    view = views.KMUserListView()
    view.request = api_rf.get(url)

    expected = [k2, k1, k3]

    assert list(view.get_queryset()) == expected


def test_get_shared(api_rf, km_user_accessor_factory, user_factory):
    """
    The list should include the users that the requesting user has
    access to through accessors.
    """
    user = user_factory()
    accessor = km_user_accessor_factory(
        is_accepted=True,
        user_with_access=user)

    api_rf.user = user

    expected = [accessor.km_user]

    request = api_rf.get(url)
    response = km_user_list_view(request)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.KMUserListSerializer(
        expected,
        context={'request': request},
        many=True)

    assert response.data == serializer.data


def test_get_shared_not_accepted(
        api_rf,
        km_user_accessor_factory,
        user_factory):
    """
    The list should not include the users where access is granted by an
    accessor that has not been accepted.
    """
    user = user_factory()
    km_user_accessor_factory(is_accepted=False, user_with_access=user)

    api_rf.user = user

    expected = []

    request = api_rf.get(url)
    response = km_user_list_view(request)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.KMUserListSerializer(
        expected,
        context={'request': request},
        many=True)

    assert response.data == serializer.data
