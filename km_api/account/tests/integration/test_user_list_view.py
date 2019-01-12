from django.contrib.auth import get_user_model

import pytest

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings

from account import serializers


url = reverse("account:user-list")


@pytest.mark.integration
def test_get_user_list(api_client, user_factory):
    """
    Sending a GET request to the view should return a paginated list of
    users.
    """
    user = user_factory(is_staff=True)
    api_client.force_authenticate(user=user)

    # Create enough users to test pagination
    for _ in range(api_settings.PAGE_SIZE + 1):
        user_factory()

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.UserListSerializer(
        get_user_model().objects.all()[: api_settings.PAGE_SIZE], many=True
    )

    assert response.data["results"] == serializer.data
