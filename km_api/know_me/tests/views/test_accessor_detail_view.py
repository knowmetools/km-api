from rest_framework import status

from know_me import serializers, views


accessor_detail_view = views.AccessorDetailView.as_view()


def test_delete_accessor(api_rf, km_user_accessor_factory):
    """
    Sending a DELETE request to the endpoint should delete the accessor
    with the given ID.
    """
    accessor = km_user_accessor_factory()
    km_user = accessor.km_user

    api_rf.user = km_user.user

    request = api_rf.delete('/')
    response = accessor_detail_view(request, pk=accessor.pk)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not km_user.km_user_accessors.exists()


def test_get_accessor(api_rf, km_user_accessor_factory):
    """
    Sending a GET request to the view should return the details of the
    accessor with the given ID.
    """
    accessor = km_user_accessor_factory()
    api_rf.user = accessor.km_user.user

    request = api_rf.get('/')
    response = accessor_detail_view(request, pk=accessor.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.KMUserAccessorSerializer(
        accessor,
        context={'request': request})

    assert response.data == serializer.data


def test_get_accessor_other_user(
        api_rf,
        km_user_accessor_factory,
        user_factory):
    """
    Attempting to access an accessor that the requesting user doesn't
    own should raises a 404.
    """
    accessor = km_user_accessor_factory()
    api_rf.user = user_factory()

    request = api_rf.get('/')
    response = accessor_detail_view(request, pk=accessor.pk)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_accessor_shared(api_rf, km_user_accessor_factory, user_factory):
    """
    Users should be able to access an accessor that grants them access
    to an account.
    """
    accessor = km_user_accessor_factory(user_with_access=user_factory())
    api_rf.user = accessor.user_with_access

    request = api_rf.get('/')
    response = accessor_detail_view(request, pk=accessor.pk)

    assert response.status_code == status.HTTP_200_OK


def test_get_accessor_unauthenticated(api_client, km_user_accessor_factory):
    """
    An unauthenticated GET request should result in a 403 response.

    Regression test for #201.
    """
    accessor = km_user_accessor_factory()

    url = accessor.get_absolute_url()
    response = api_client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_patch_accessor(api_rf, km_user_accessor_factory):
    """
    Sending a PATCH request to the view should update the accessor with
    the given ID.
    """
    accessor = km_user_accessor_factory(is_admin=False)
    data = {
        'is_admin': True,
    }

    api_rf.user = accessor.km_user.user

    request = api_rf.patch('/', data)
    response = accessor_detail_view(request, pk=accessor.pk)

    assert response.status_code == status.HTTP_200_OK

    accessor.refresh_from_db()

    assert accessor.is_admin == data['is_admin']
