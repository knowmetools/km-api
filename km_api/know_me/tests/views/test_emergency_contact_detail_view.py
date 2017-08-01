from rest_framework import status

from know_me import serializers, views, models


emergency_contact_detail_view = views.EmergencyContactDetailView.as_view()


def test_delete(api_rf, emergency_contact_factory):
    """
    Sending a DELETE request to the view should delete the item with the
    given ID.
    """
    ec = emergency_contact_factory()
    api_rf.user = ec.km_user.user

    request = api_rf.delete(ec)
    response = emergency_contact_detail_view(request, pk=ec.pk)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert models.EmergencyContact.objects.count() == 0


def test_update(api_rf, emergency_contact_factory):
    """
    Sending a PATCH request to the view with valid data should update
    the emergency contact.
    """
    e_contact = emergency_contact_factory(name='Old Name')
    km_user = e_contact.km_user

    api_rf.user = km_user.user

    data = {
        'name': 'New Name',
    }

    request = api_rf.patch(e_contact.get_absolute_url(), data)
    response = emergency_contact_detail_view(request, pk=e_contact.pk)

    assert response.status_code == status.HTTP_200_OK

    e_contact.refresh_from_db()
    serializer = serializers.EmergencyContactSerializer(
        e_contact,
        context={'request': request})

    assert response.data == serializer.data
