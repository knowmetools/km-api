import pytest

from rest_framework import status
from rest_framework.reverse import reverse

from know_me import models, serializers


url = reverse('know-me:legacy-user-list')


@pytest.mark.integration
def test_get_legacy_user_list(
        api_client,
        api_rf,
        legacy_user_factory,
        user_factory):
    """
    Sending a GET request to the view should return the list of legacy
    users.
    """
    user = user_factory(is_staff=True)
    api_client.force_authenticate(user=user)
    api_rf.user = user

    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.LegacyUserSerializer(
        models.LegacyUser.objects.all(),
        context={'request': request},
        many=True)

    assert response.data['results'] == serializer.data


@pytest.mark.integration
def test_post_new_legacy_user(api_client, api_rf, user_factory):
    """
    Sending a POST request to the view should create a new legacy user.
    """
    user = user_factory(is_staff=True)
    api_client.force_authenticate(user=user)
    api_rf.user = user

    data = {
        'email': 'test@example.com',
    }

    request = api_rf.post(url, data)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED

    legacy_user = models.LegacyUser.objects.get()
    serializer = serializers.LegacyUserSerializer(
        legacy_user,
        context={'request': request})

    assert response.data == serializer.data
