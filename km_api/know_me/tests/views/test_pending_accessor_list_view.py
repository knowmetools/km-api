from rest_framework import status
from rest_framework.reverse import reverse

from know_me import serializers


url = reverse('know-me:pending-accessor-list')


def test_get_pending_accessors(
        api_client,
        api_rf,
        km_user_accessor_factory,
        user_factory):
    """
    Sending a GET request to the view should return a list of the
    accessors that the requesting user can accept.
    """
    user = user_factory()
    api_client.force_authenticate(user=user)

    km_user_accessor_factory(accepted=False, user_with_access=user)
    km_user_accessor_factory(accepted=True, user_with_access=user)

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.KMUserAccessorSerializer(
        user.km_user_accessors.filter(accepted=False),
        context={'request': api_rf.get(url)},
        many=True)

    assert response.data == serializer.data
