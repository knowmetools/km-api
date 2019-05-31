from rest_framework import status


def test_update_media_resource(
    api_client,
    enable_premium_requirement,
    media_resource_factory,
    user_factory,
):
    """
    Premium users should be able to update their own media resources.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    resource = media_resource_factory(km_user__user=user, name="Old Name")

    url = f"/know-me/profile/media-resources/{resource.pk}/"
    data = {"name": "New Name"}
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == data["name"]
