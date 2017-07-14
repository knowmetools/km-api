from rest_framework import status
from rest_framework.reverse import reverse

from account import models, serializers, views


email_action_list_view = views.EmailActionListView.as_view()
url = reverse('account:email-action-list')


def test_get_action_list(api_rf):
    """
    Sending a GET request to the view should return a list of the
    available actions when creating an email address.
    """
    request = api_rf.get(url)
    response = email_action_list_view(request)

    assert response.status_code == status.HTTP_200_OK, response.data

    serializer = serializers.EmailVerifiedActionSerializer(
        models.EmailAddress.VERIFIED_ACTION_CHOICES,
        many=True)

    assert response.data == serializer.data
