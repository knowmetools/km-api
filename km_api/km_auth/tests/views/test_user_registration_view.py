from django.contrib.auth import get_user_model

import pytest

from rest_framework import status
from rest_framework.reverse import reverse

from km_auth import serializers, views


user_registration_view = views.UserRegistrationView.as_view()


@pytest.mark.django_db
def test_register(api_rf):
    """
    Submitting a POST request with valid data should create a new user.
    """
    data = {
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'p455w0rd',
    }

    url = reverse('auth:register')
    request = api_rf.post(url, data)

    response = user_registration_view(request)

    assert response.status_code == status.HTTP_201_CREATED
    assert get_user_model().objects.count() == 1

    serializer = serializers.UserRegistrationSerializer(
        get_user_model().objects.get())

    assert response.data == serializer.data


def test_register_authenticated(admin_api_rf):
    """
    Authenticated users should receive a permission error if they try to
    register.
    """
    data = {
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'password': 'p455w0rd',
    }

    url = reverse('auth:register')
    request = admin_api_rf.post(url, data)

    response = user_registration_view(request)

    assert response.status_code == status.HTTP_403_FORBIDDEN
