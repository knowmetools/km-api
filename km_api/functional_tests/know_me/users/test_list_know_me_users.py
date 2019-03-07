import pytest
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.parametrize("is_premium", [True, False])
def test_km_user_premium_flag(
    api_client, is_premium, km_user_factory, subscription_factory
):
    """
    The response from the Know Me user list should include a boolean
    property indicating if each user is a premium user.
    """
    # Given a Know Me user...
    password = "password"
    km_user = km_user_factory(user__password=password)
    api_client.log_in(km_user.user.primary_email.email, password)

    # ...who may have a subscription...
    if is_premium:
        subscription_factory(is_active=True, user=km_user.user)

    # If they list all Know Me users...
    url = reverse("know-me:km-user-list")
    response = api_client.get(url)

    # The response should indicate if the Know Me user is a premium
    # user.
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]["is_premium_user"] == is_premium
