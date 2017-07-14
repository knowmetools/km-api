from rest_framework import status
from rest_framework.reverse import reverse

from account import serializers, views


email_list_view = views.EmailListView.as_view()
url = reverse('account:email-list')


def test_create_email(api_rf, user_factory):
    """
    Sending a POST request to the view with valid data should create a
    new email address for the user.
    """
    user = user_factory()
    api_rf.user = user

    data = {
        'email': 'newemail@example.com',
    }

    request = api_rf.post(url, data)
    response = email_list_view(request)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.EmailSerializer(
        user.email_addresses.get(),
        context={'request': request})

    assert response.data == serializer.data


def test_list_emails(api_rf, email_factory, user_factory):
    """
    Sending a GET request to the view should list the requesting user's
    email addresses.
    """
    user = user_factory()
    email_factory(user=user)
    email_factory(user=user)

    api_rf.user = user

    request = api_rf.get(url)
    response = email_list_view(request)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.EmailSerializer(
        user.email_addresses.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data
