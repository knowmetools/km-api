from rest_framework import status

from account import serializers, views


email_detail_view = views.EmailDetailView.as_view()


def test_delete_email(api_rf, email_factory, user_factory):
    """
    Sending a DELETE request to the view should delete the email address
    with the given ID.
    """
    user = user_factory()

    # Create a dummy email for the user because the first email is
    # always made a primary email.
    email_factory(user=user, primary=True)
    email = email_factory(primary=False, user=user)

    api_rf.user = user

    request = api_rf.delete(email.get_absolute_url())
    response = email_detail_view(request, pk=email.pk)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.email_addresses.filter(pk=email.pk).count() == 0


def test_delete_primary_email(api_rf, email_factory):
    """
    Sending a DELETE request to the view with the ID of a primary email
    address should fail to delete the email.
    """
    email = email_factory(primary=True)
    user = email.user

    api_rf.user = user

    request = api_rf.delete(email.get_absolute_url())
    response = email_detail_view(request, pk=email.pk)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert user.email_addresses.get() == email


def test_get_email_details(api_rf, email_factory):
    """
    Sending a GET request to the view should return the serialized
    details of the email address with the given ID.
    """
    email = email_factory()
    api_rf.user = email.user

    request = api_rf.get(email.get_absolute_url())
    response = email_detail_view(request, pk=email.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.EmailSerializer(
        email,
        context={'request': request})

    assert response.data == serializer.data


def test_update_email_details(api_rf, email_factory):
    """
    Sending a PATCH request to the view should update the email address
    with the given ID using the given data.
    """
    email = email_factory(verified=True)
    api_rf.user = email.user

    data = {
        'primary': True,
    }

    request = api_rf.patch(email.get_absolute_url(), data)
    response = email_detail_view(request, pk=email.pk)

    assert response.status_code == status.HTTP_200_OK

    email.refresh_from_db()
    serializer = serializers.EmailSerializer(
        email,
        context={'request': request})

    assert response.data == serializer.data
