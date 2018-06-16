import pytest

from rest_framework import status


@pytest.mark.integration
def test_delete_accessor_shared(
        api_client,
        km_user_accessor_factory,
        user_factory):
    """
    Sending a DELETE request as the user granted access through an
    accessor should delete the specified accessor.

    Regression test for #358
    """
    user = user_factory()
    api_client.force_authenticate(user=user)

    accessor = km_user_accessor_factory(user_with_access=user)

    url = accessor.get_absolute_url()
    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert user.km_user_accessors.count() == 0
