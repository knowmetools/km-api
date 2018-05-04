import pytest

from rest_framework import status

from know_me import models, serializers


@pytest.mark.integration
def test_delete_legacy_user(api_client, legacy_user_factory, user_factory):
    """
    Sending a DELETE request to the view should delete the specified
    legacy user.
    """
    legacy_user = legacy_user_factory()
    user = user_factory(is_staff=True)
    api_client.force_authenticate(user=user)

    url = legacy_user.get_absolute_url()
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.LegacyUser.objects.count() == 0


@pytest.mark.integration
def test_get_legacy_user(
        api_client,
        api_rf,
        legacy_user_factory,
        user_factory):
    """
    Sending a GET request to the view should return the information of
    the specified legacy user.
    """
    legacy_user = legacy_user_factory()
    user = user_factory(is_staff=True)
    api_client.force_authenticate(user=user)
    api_rf.user = user

    url = legacy_user.get_absolute_url()
    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.LegacyUserSerializer(
        legacy_user,
        context={'request': request})

    assert response.data == serializer.data


@pytest.mark.integration
def test_patch_legacy_user(api_client, legacy_user_factory, user_factory):
    """
    Sending a PATCH request to the view should update the specified
    legacy user's information.
    """
    user = user_factory(is_staff=True)
    api_client.force_authenticate(user=user)

    legacy_user = legacy_user_factory(email='old@example.com')
    data = {'email': 'new@example.com'}

    url = legacy_user.get_absolute_url()
    response = api_client.patch(url, data)

    legacy_user.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert legacy_user.email == data['email']
