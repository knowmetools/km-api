from rest_framework import status


def test_delete_media_resource(
    api_client,
    enable_premium_requirement,
    media_resource_factory,
    user_factory,
):
    """
    Premium users should be able to delete their own media resources.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    resource = media_resource_factory(km_user__user=user)

    url = f"/know-me/profile/media-resources/{resource.pk}/"
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
