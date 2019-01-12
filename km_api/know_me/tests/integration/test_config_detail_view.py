import pytest

from rest_framework import status
from rest_framework.reverse import reverse

from know_me import serializers


url = reverse("know-me:config-detail")


@pytest.mark.integration
def test_get_config(api_client, api_rf, config_factory):
    """
    Sending a GET request to the view should return the serialized
    configuration.
    """
    config = config_factory()

    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.ConfigSerializer(
        config, context={"request": request}
    )

    assert response.data == serializer.data


@pytest.mark.integration
def test_patch_config(api_client, config_factory, user_factory):
    """
    Sending a PATCH request to the view should update the global config
    singleton.
    """
    config = config_factory(minimum_app_version_ios="1.0.0")
    user = user_factory(is_staff=True)
    api_client.force_authenticate(user=user)

    data = {"minimum_app_version_ios": "2.0.0"}

    response = api_client.patch(url, data)
    config.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert config.minimum_app_version_ios == data["minimum_app_version_ios"]
