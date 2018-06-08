import pytest

from push_notifications.api.rest_framework import APNSDeviceSerializer

from rest_framework import status
from rest_framework.reverse import reverse


url = reverse('notifications:apns-device-list')


@pytest.mark.integration
def test_get_apns_device_list(
        api_client,
        api_rf,
        apns_device_factory,
        user_factory):
    """
    Sending a GET request to the view should return a list of the user's
    registered APNS devices.
    """
    user = user_factory()
    api_client.force_authenticate(user=user)
    api_rf.user = user

    apns_device_factory(user=user)
    apns_device_factory(user=user)

    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = APNSDeviceSerializer(
        user.apnsdevice_set.all(),
        context={'request': request},
        many=True,
    )

    assert response.data == serializer.data


@pytest.mark.integration
def test_post_new_apns_device(api_client, api_rf, user_factory):
    """
    Sending a POST request to the view should create a new APNS device
    attached to the requesting user.
    """
    user = user_factory()
    api_client.force_authenticate(user=user)
    api_rf.user = user

    data = {
        # The registration ID must be 64 or 200 characters
        'registration_id': '1' * 64,
    }

    request = api_rf.post(url, data)
    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = APNSDeviceSerializer(
        user.apnsdevice_set.get(),
        context={'request': request},
    )

    assert response.data == serializer.data
