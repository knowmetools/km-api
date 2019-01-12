from rest_framework import status

from know_me import serializers, views


km_user_detail_view = views.KMUserDetailView.as_view()


def test_get_own_km_user(api_rf, km_user_factory, user_factory):
    """
    A user should be able to get the details of their own Know Me user
    account.
    """
    user = user_factory()
    api_rf.user = user

    km_user = km_user_factory(user=user)

    request = api_rf.get(km_user.get_absolute_url())
    response = km_user_detail_view(request, pk=km_user.pk)

    serializer = serializers.KMUserDetailSerializer(
        km_user, context={"request": request}
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data


def test_update(api_rf, km_user_factory, user_factory):
    """
    Sending a PATCH request to the view should update the specified
    Know Me user.
    """
    user = user_factory()
    api_rf.user = user

    km_user = km_user_factory(quote="Old Quote.", user=user)
    data = {"quote": "New Quote."}

    request = api_rf.patch(km_user.get_absolute_url(), data)
    response = km_user_detail_view(request, pk=km_user.pk)

    assert response.status_code == status.HTTP_200_OK

    km_user.refresh_from_db()
    serializer = serializers.KMUserDetailSerializer(
        km_user, context={"request": request}
    )

    assert response.data == serializer.data
