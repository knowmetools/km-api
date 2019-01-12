from rest_framework import status
from rest_framework.reverse import reverse

from account import serializers, views


user_detail_view = views.UserDetailView.as_view()
url = reverse("account:profile")


def test_anonymous(api_rf):
    """
    Anonymous users should not be able to access the view.
    """
    request = api_rf.get(url)
    response = user_detail_view(request)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_get_user_details(api_rf, user_factory):
    """
    Sending an authenticated GET request to the view should return the
    serialized details of the requesting user.
    """
    user = user_factory()
    api_rf.user = user

    request = api_rf.get(url)
    response = user_detail_view(request)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.UserSerializer(user, context={"request": request})

    assert response.data == serializer.data


def test_update_user_details(api_rf, user_factory):
    """
    Sending a PATCH request to the view should update the requesting
    user's information.
    """
    user = user_factory(first_name="Bob")
    api_rf.user = user

    data = {"first_name": "John"}

    request = api_rf.patch(url, data)
    response = user_detail_view(request)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.UserSerializer(
        user, context={"request": request}, data=data, partial=True
    )
    assert serializer.is_valid()

    assert response.data == serializer.data
