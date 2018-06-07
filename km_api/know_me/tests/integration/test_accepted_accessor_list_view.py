import pytest

from rest_framework import status
from rest_framework.reverse import reverse

from know_me import serializers


url = reverse('know-me:accepted-accessor-list')


@pytest.mark.integration
def test_get_accepted_accessor_list(
        api_client,
        api_rf,
        km_user_accessor_factory,
        user_factory):
    """
    Sending a GET request to this view should return a list of the
    accessors accepted by the requesting user.
    """
    user = user_factory()
    api_client.force_authenticate(user=user)
    api_rf.user = user

    km_user_accessor_factory(is_accepted=True)
    km_user_accessor_factory(is_accepted=False, user_with_access=user)
    km_user_accessor_factory(is_accepted=True, user_with_access=user)
    km_user_accessor_factory(is_accepted=True, user_with_access=user)

    request = api_rf.get(url)
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.KMUserAccessorSerializer(
        user.km_user_accessors.filter(is_accepted=True),
        context={'request': request},
        many=True,
    )

    assert response.data == serializer.data
