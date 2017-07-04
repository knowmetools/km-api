from rest_framework import status
from rest_framework.reverse import reverse

from km_auth import serializers, views


user_detail_view = views.UserDetailView.as_view()
url = reverse('auth:user-detail')


def test_get(api_rf, user_factory):
    """
    Sending a GET request to the view should return the currently
    authenticated user's details.
    """
    user = user_factory()
    api_rf.user = user

    request = api_rf.get(url)
    response = user_detail_view(request)

    serializer = serializers.UserDetailSerializer(user)

    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data


def test_get_anonymous(api_rf):
    """
    Anonymous users should not be able to access this view.
    """
    request = api_rf.get(url)
    response = user_detail_view(request)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_update(api_rf, user_factory):
    """
    Sending a PATCH request with valid data should update the current
    user's details.
    """
    user = user_factory()
    api_rf.user = user

    data = {
        'first_name': 'Billy',
    }

    request = api_rf.patch(url, data)
    response = user_detail_view(request)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.UserDetailSerializer(
        user,
        data=data,
        partial=True)
    assert serializer.is_valid()

    assert response.data == serializer.data
