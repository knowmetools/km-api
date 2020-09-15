from rest_framework import status

from test_utils import serialized_time


def test_list_media_resources(
    api_client,
    enable_premium_requirement,
    media_resource_factory,
    user_factory,
):
    """
    Premium users should be able to list their own media resources.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    resource = media_resource_factory(km_user__user=user)

    url = f"/know-me/users/{user.km_user.pk}/media-resources/"
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": resource.pk,
            "url": api_client.build_full_url(
                f"/know-me/profile/media-resources/{resource.pk}/"
            ),
            "created_at": serialized_time(resource.created_at),
            "updated_at": serialized_time(resource.updated_at),
            "cover_art": resource.cover_art,
            "cover_style": resource.cover_style,
            "file": api_client.build_full_url(resource.file.url),
            "link": resource.link,
            "name": resource.name,
            "permissions": {"read": True, "write": True},
        }
    ]
