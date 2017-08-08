from rest_framework import status

from know_me import serializers, views


emergency_contact_list_view = views.EmergencyContactListView.as_view()


def test_create(api_rf, km_user_factory):
    """
    Sending a POST request to the view containing valid data should
    create a new emergency contact.
    """
    km_user = km_user_factory()
    api_rf.user = km_user.user

    data = {
        'name': 'My Name',
        'relation': 'My relation',
        'phone_number': '19199911919',
        'alt_phone_number': '18008008000',
        'email': 'email@gmail.com'
    }

    request = api_rf.post(km_user.get_emergency_contact_list_url(), data)
    response = emergency_contact_list_view(request, pk=km_user.pk)

    assert response.status_code == status.HTTP_201_CREATED

    serializer = serializers.EmergencyContactSerializer(
        km_user.emergency_contacts.get(),
        context={'request': request})

    assert response.data == serializer.data


def test_get(api_rf, emergency_contact_factory, km_user_factory):
    """
    Sending a GET request to the view should return a list of all the
    emergency items owned by Know Me user specified.
    """
    km_user = km_user_factory()
    emergency_contact_factory(km_user=km_user)
    emergency_contact_factory(km_user=km_user)

    api_rf.user = km_user.user

    request = api_rf.get(km_user.get_emergency_contact_list_url())
    response = emergency_contact_list_view(request, pk=km_user.pk)

    assert response.status_code == status.HTTP_200_OK

    serializer = serializers.EmergencyContactSerializer(
        km_user.emergency_contacts.all(),
        context={'request': request},
        many=True)

    assert response.data == serializer.data
