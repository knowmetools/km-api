from rest_framework import status


def test_update_attach_media_resource(
    api_client,
    enable_premium_requirement,
    media_resource_factory,
    profile_item_factory,
    user_factory,
):
    """
    If a premium user has an existing profile item, they should be able
    to attach a media resource to it.

    Regression test for #317.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    item = profile_item_factory(topic__profile__km_user__user=user)
    resource = media_resource_factory(km_user=user.km_user)

    url = f"/know-me/profile/profile-items/{item.pk}/"
    data = {"media_resource_id": resource.id}
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["media_resource"]["id"] == resource.pk


def test_update_detatch_media_resource(
    api_client,
    enable_premium_requirement,
    media_resource_factory,
    profile_item_factory,
    user_factory,
):
    """
    Premium users should be able to detach media resources from their
    profile items.

    Regression test for #321
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    resource = media_resource_factory(km_user__user=user)
    item = profile_item_factory(
        media_resource=resource, topic__profile__km_user=resource.km_user
    )

    url = f"/know-me/profile/profile-items/{item.pk}/"
    data = {"media_resource_id": ""}
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["media_resource"] is None


def test_update_profile_item(
    api_client, enable_premium_requirement, profile_item_factory, user_factory
):
    """
    Premium users should be able to update profile items that they own.
    """
    password = "password"
    user = user_factory(has_premium=True, password=password)
    api_client.log_in(user.primary_email.email, password)

    item = profile_item_factory(
        topic__profile__km_user__user=user, name="Old Name"
    )

    url = f"/know-me/profile/profile-items/{item.pk}/"
    data = {"name": "New Name"}
    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == data["name"]
